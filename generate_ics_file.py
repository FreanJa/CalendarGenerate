import functions


def generate():
    path = input("JSON file path:\n")
    ics_path = input("Path to save ics folder:(Optional, Default: ./generated_file/ics/{json file name}/)\n")
    if ics_path:
        functions.json_to_ics(path, ics_path)
    else:
        functions.json_to_ics(path)


if __name__ == '__main__':
    generate()
