import copy
import datetime
import os

import pdfplumber
import json
import re

Week = {"星期一": "Mon", "星期二": "Tue", "星期三": "Wed", "星期四": "Thur", "星期五": "Fri", "星期六": "Sat", "星期日": "Sun"}
Offset = {"Mon": 0, "Tue": 1, "Wed": 2, "Thur": 3, "Fri": 4, "Sat": 5, "Sun": 6}
Time_N = {"1": ["081000", "085500"], "2": ["090000", "094500"], "3": ["100000", "104500"], "4": ["104500", "113000"],
          "5": ["113500", "122000"], "6": ["133000", "141500"], "7": ["142000", "150500"], "8": ["151500", "160000"],
          "9": ["160500", "165000"], "10": ["183000", "191500"], "11": ["192000", "200500"], "12": ["201000", "205500"]}
Time_S = {"1": ["082000", "090500"], "2": ["090500", "094500"], "3": ["101500", "110000"], "4": ["110500", "115000"],
          "5": ["115000", "123500"], "6": ["133000", "141500"], "7": ["142000", "150500"], "8": ["151500", "160000"],
          "9": ["160500", "165000"], "10": ["183000", "191500"], "11": ["192000", "200500"], "12": ["201000", "205500"]}
patt1 = "[0-9]+"
patt2 = r"\n(.*)\n"
patt3 = r"\n(.*)"
patt4 = "\$\(\S+?\)"
patt5 = "\$\((\S+?)\)"
patt6 = "\(.*\)"

Alarm = '''
BEGIN:VALARM
ACTION:AUDIO
TRIGGER:-PT{}M
END:VALARM
'''

path = "./data/"
json_path = "./generated_file/json/"
ics_path = "./generated_file/ics/"
default_alarm = ["15", "30"]


def read_pdf(full_path):
    pdf = pdfplumber.open(full_path)
    if pdf is not None:
        schedule = []
        for page in pdf.pages:
            table = page.extract_table()
            for line in table:
                course = []
                for elem in line:
                    if elem is not None:
                        tmp = elem.split(" ")
                        for t in tmp:
                            if t == '':
                                continue
                            if re.match("教学班:", t) or re.match("周数:", t) or re.match("地点:", t) \
                                    or re.match("教师:", t):
                                continue
                            course.append(t)
                    else:
                        course.append(elem)
                schedule.append(course)
        return schedule
    return None


def json_format(full_path, start_time, alarm=None, save=json_path, ):
    if alarm is None:
        alarm = default_alarm
    VALARM = []
    if alarm:
        for item in alarm:
            if item:
                VALARM.append(Alarm.format(item))

    calender = {}
    day_sche = {}
    courses = {}
    course = {"Course": "", "StartTime": "", "EndTime": "", "StartDate": "",
              "EndDate": "", "Location": "", "Description": "", "Frequency": "1"}
    week = ""
    time = ""
    last = ""
    standby = ""
    get_course_name = False
    info = read_pdf(full_path)
    practical_courses = []
    other_courses = []

    for i in range(len(info) - 1):
        if i == 0:
            semester = "{}-{}-{}".format(
                re.findall(patt1, info[i][0])[0],
                re.findall(patt1, info[i][0])[1],
                re.findall(patt1, info[i][0])[2]
            )
            calender["Semester"] = semester
        else:
            # print(info[i])
            if info[i][0]:
                if re.match("实践课程：", info[i][0]):
                    for item in info[i]:
                        if item:
                            item = item.replace('\n', '').strip()
                            if re.match("实践课程：", item):
                                practical_courses.append(re.findall(r"实践课程：(.*)", item)[0])
                            else:
                                practical_courses.append(item)
                    continue
                elif re.match("其它课程：", info[i][0]):
                    for item in info[i]:
                        if item:
                            item = item.replace('\n', '').strip()
                            if re.match("其它课程：", item):
                                other_courses.append(re.findall(r"其它课程：(.*)", item)[0])
                            else:
                                other_courses.append(item)
                    continue

            for j in range(len(info[i])):
                if j == 0:
                    last = week
                    if info[i][j]:
                        week = Week[info[i][j]]

                if j == 1:
                    if info[i][j]:
                        time = info[i][j]
                    else:
                        time += "（{}）".format(info[i][2])

                if not info[i][j]:
                    continue

                get = re.search(patt2, info[i][j])
                if get:
                    get_course_name = True
                    course["Course"] = get.group(1)
                elif standby == "" and re.search(patt3, info[i][j]):
                    standby = re.search(patt3, info[i][j]).group(1)

            course["Location"] = info[i][3]
            course["Description"] = info[i][4]

            if last != "" and last != week:
                courses[last] = copy.deepcopy(day_sche)
                day_sche.clear()

            if not get_course_name:
                course["Course"] = standby
                standby = ""
            else:
                get_course_name = False

            if re.search(patt6, info[i][2]):
                course["Frequency"] = "2"
            else:
                course["Frequency"] = "1"

            week_during = re.findall(patt1, info[i][2])
            course["StartDate"] = cal_date(start_time, int(week_during[0]), week)
            course["EndDate"] = cal_date(start_time, int(week_during[1]), week)

            s_section, e_section = re.findall(r"[0-9]+", time)[:2]

            if re.match("3", course["Location"]) or re.match("2-S", course["Location"]):
                course["StartTime"] = Time_S[s_section][0]
                course["EndTime"] = Time_S[e_section][1]
            else:
                course["StartTime"] = Time_N[s_section][0]
                course["EndTime"] = Time_N[e_section][1]

            day_sche[time] = copy.deepcopy(course)

    courses[week] = copy.deepcopy(day_sche)
    calender["Courses"] = courses
    calender["Practical_courses"] = practical_courses
    calender["Other_courses"] = other_courses
    calender["VALARM"] = VALARM

    generate_file = "{}{}.json".format(save, calender["Semester"])
    with open(generate_file, "w", encoding='utf-8') as f:
        json.dump(calender, f, ensure_ascii=False)
        print('[Success] Save json data in "{}"'.format(generate_file))

    return calender


def cal_date(start, during, week):
    first = datetime.datetime.strptime(start, "%Y%m%d")
    during_time = datetime.timedelta(days=7 * (during - 1) + Offset[week])
    first += during_time
    return first.strftime("%Y%m%d")


def json_to_ics(json_data, save=ics_path):

    if isinstance(json_data, str):
        with open(json_data, "r", encoding="utf-8") as f:
            dict_data = json.load(f)
    elif isinstance(json_data, dict):
        dict_data = json_data
    else:
        print("[Error] Wrong input")
        return

    with open("./data/iCal_test.ics", "r", encoding="utf8") as fo:
        save_dir = save + "{}/".format(dict_data["Semester"])
        VALARM = dict_data["VALARM"]
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for week, day in dict_data.get("Courses").items():

            for time, course in day.items():

                class_name = course["Course"]

                full_file_path = "{}{}({} {}).ics".format(
                    save_dir,
                    class_name,
                    week,
                    time
                )

                with open(full_file_path, "w", encoding="utf8") as fi:
                    for line in fo.readlines():
                        w_line = line
                        findall = re.findall(patt4, w_line)
                        if findall:
                            for elem in findall:
                                if elem == "$(VALARM)":
                                    alarm = ""
                                    for item in VALARM:
                                        alarm += item
                                    w_line = w_line.replace(elem, alarm)
                                    continue
                                w_line = w_line.replace(elem, course.get(re.findall(patt5, elem)[0]))
                        fi.write(w_line)
                    print('[Success] Generate "{}"'.format(full_file_path))
                    fo.seek(0, 0)
    return


if __name__ == '__main__':
    filename = "2021-2022-1.pdf"
    start_date = "20210906"
    data = json_format("{}personal_data/{}".format(path, filename), start_date)
    # json_to_ics("./generated_file/json/2020-2021-2.json")
