import functions


def generate():
    path = input("PDF file path:\n")
    start_date = input("Date of Commencement of Courses:\n")
    alarm = input("Alarm:(Optional, Default:[-15M, -30M])\n").split(',')
    functions.json_format(path, start_date, alarm)


if __name__ == '__main__':
    generate()
