import generate_json_file
import generate_ics_file


def run():
    json = input("已经有JSON文件了?(y/n)\n")
    if json == 'n':
        path = generate_json_file.generate_json(f="_personal")
        go_on = input("继续生成ICS文件?(y/n)\n")
        if go_on == 'y':
            ics_save = input("保存ics文件的路径: (可选项, 默认: ./generated_file/ics/)\n")
            if ics_save:
                # generate_ics_file.json_to_ics(path, ics_save, flag="_personal")
                generate_ics_file.json_to_ics(path, ics_save, flag="_personal")
            else:
                # generate_ics_file.json_to_ics(path, flag="_personal")
                generate_ics_file.json_to_ics(path, flag="_personal")
    elif json == 'y':
        generate_ics_file.generate_ics()
    else:
        print("[Error] Invalid Input :(\n")
    return


if __name__ == '__main__':
    run()
