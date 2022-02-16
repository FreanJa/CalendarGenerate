import copy
import datetime

import pdfplumber
import json
import re

import sys

Week = {"星期一": "Mon", "星期二": "Tue", "星期三": "Wed", "星期四": "Thur", "星期五": "Fri", "星期六": "Sat", "星期日": "Sun"}
Time_N = {1: ["081000", "085500"], 2: ["090000", "094500"], 3: ["100000", "104500"], 4: ["104500", "113000"],
          5: ["113500", "122000"], 6: ["133000", "141500"], 7: ["142000", "150500"], 8: ["151500", "160000"],
          9: ["160500", "165000"], 10: ["183000", "191500"], 11: ["192000", "200500"], 12: ["201000", "205500"]}
Time_S = {1: ["082000", "090500"], 2: ["090500", "094500"], 3: ["101500", "110000"], 4: ["110500", "115000"],
          5: ["115000", "123500"], 6: ["133000", "141500"], 7: ["142000", "150500"], 8: ["151500", "160000"],
          9: ["160500", "165000"], 10: ["183000", "191500"], 11: ["192000", "200500"], 12: ["201000", "205500"]}
patt1 = "[0-9]+"
patt2 = r"\n(.*)\n"


def read_pdf(full_path):
    pdf = pdfplumber.open(full_path)
    if pdf is not None:
        schedule = []
        for page in pdf.pages:
            table = page.extract_table()
            for line in table:
                course = []
                # print(line)
                for elem in line:
                    if elem is not None:
                        tmp = elem.split(" ")
                        for t in tmp:
                            if t == '':
                                continue
                            if re.match("教学班:", t) or re.match("周学时:", t) or re.match("周学时:", t) or \
                                    re.match("总学时:", t) or re.match("学分:", t) or re.match("周数:", t) or \
                                    re.match("地点:", t) or re.match("教师:", t):
                                continue
                            course.append(t)
                    else:
                        course.append(elem)
                schedule.append(course)
        return schedule

    return None


def json_format(full_path):
    calender = {}
    day_sche = {}
    course = {"Course": "", "StartTime": "", "EndTime": "", "StartDate": "",
              "EndDate": "", "Location": "", "Description": ""}
    week = ""
    time = ""
    last = ""
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
            print("calender:", end="\t")
            print(calender)
            # print(pdf_info[i])
        else:
            if info[i][0]:
                if re.match("实践课程：", info[i][0]):
                    for item in info[i]:
                        if item:
                            practical_courses.append(item)
                    continue
                elif re.match("其它课程：", info[i][0]):
                    for item in info[i]:
                        if item:
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
                    course["Course"] = get.group(1)

            print(last + "\t" + week)
            if last != "" and last != week:
                print("======== set =========")
                calender[last] = copy.deepcopy(day_sche)
                # print(calender)
                day_sche.clear()

            day_sche[time] = copy.deepcopy(course)
            print("=== " + week + " " + time + " ===")
            print("day_sche:", end="\t")
            print(day_sche)
            print("calender:", end="\t")
            print(calender)
            print()

            # print(calender)
        print()
    calender[week] = copy.deepcopy(day_sche)
    calender["practical_courses"] = practical_courses
    calender["other_courses"] = other_courses
    return calender


def cal_date(start, during):
    first = datetime.datetime.strptime(start, "%Y%m%d")
    during_time = datetime.timedelta(days=7 * (during - 1))
    first += during_time
    return first.strftime("%Y%m%d")


if __name__ == '__main__':
    path = "./data/"
    filename = "2020-2021-1.pdf"
    data = json_format(path + filename)
    with open("try_write.txt", "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        print("run")

