import functions


def generate():
    path = input("PDF file path:\n")
    start_date = input("Date of Commencement of Courses:\n")
    alarm = input("Alarm:\n").split(',')
    functions.json_format(path, start_date, alarm)


if __name__ == '__main__':
    generate()
