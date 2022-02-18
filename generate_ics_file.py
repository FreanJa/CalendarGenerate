import json
import re

# 文件
ics_path = "./generated_file/ics/"

# 文本模版
Event = '''
BEGIN:VEVENT
LOCATION:$(Location)
DESCRIPTION:$(Description)
X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:DISABLED
DTSTART;TZID=Asia/Shanghai:$(StartDate)T$(StartTime)
DTEND;TZID=Asia/Shanghai:$(StartDate)T$(EndTime)
SUMMARY:$(Course)
RRULE:FREQ=WEEKLY;INTERVAL=$(Frequency);UNTIL=$(EndDate)T235959Z
$(VALARM)
END:VEVENT
'''

# 正则
patt_replace = "\$\(\S+?\)"
patt_key = "\$\((\S+?)\)"


def json_to_ics(json_data, save=ics_path, flag=""):

    if isinstance(json_data, str):
        with open(json_data, "r", encoding="utf-8") as f:
            dict_data = json.load(f)
    elif isinstance(json_data, dict):
        dict_data = json_data
    else:
        print("[Error] Wrong input")
        return

    with open("./data/iCal_format.ics", "r", encoding="utf8") as fo:
        save_file = save + "{}{}.ics".format(dict_data["Semester"], flag)

        alarm = ""
        for item in dict_data["VALARM"]:
            alarm += item
        P_Event = Event.replace("$(VALARM)", alarm)

        with open(save_file, "w", encoding="utf-8") as fi:
            for line in fo.readlines():
                w_line = line
                if re.search("\$\(Semester\)", w_line):
                    w_line = w_line.replace("$(Semester)", dict_data["Semester"])
                elif re.search("\$\(Courses\)", w_line):
                    EVENT = ""
                    for week, day in dict_data.get("Courses").items():
                        for time, course in day.items():
                            VEVENT = P_Event
                            for rep in re.findall(patt_replace, P_Event):
                                if rep:
                                    VEVENT = VEVENT.replace(rep, course.get(re.findall(patt_key, rep)[0]))
                            EVENT += VEVENT
                    w_line = w_line.replace("$(Courses)", EVENT)
                fi.write(w_line)
        print('[Success] Generate "{}"'.format(save_file))

    return


def generate_ics():
    path = input("JSON文件路径:\n")
    ics_save = input("保存ics文件的路径: (可选项, 默认: ./generated_file/ics/)\n")
    if ics_save:
        json_to_ics(path, ics_save, flag="_personal")
    else:
        json_to_ics(path, flag="_personal")


if __name__ == '__main__':
    json_to_ics("./generated_file/json/2019-2020-2.json", "./generated_file/ics/")
