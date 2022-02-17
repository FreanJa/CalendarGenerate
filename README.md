# 日历生成 CalendarGenerate ( for Zstuer )

> 根据 浙江理工大学 教务系统导出的 pdf 课表 自动生成 .json文件 以及 .ics 文件
>
> generate .ics file from pdf (zstu course scheduel format)

根据zstu教务系统下载的pdf课表，生成json和ics文件，方便批量导入到个人日历软件

A project that can let ZSTU Educational administration system exported pdf schedule file automatically generates ics files to import into the system calendar

---

## How to use

* Run **generate_json_file.py** to get json file

  ```Linux
  ## The Sample input you can use ⬇️
   ./data/personal_data/2020-2021-2.pdf
   20210301
   10,20
   
   # Output ⬇️
  [Success] Save json data in "./generated_file/json/2020-2021-2.json"
  
  ```

  <img src="https://pic.freanja.cn/images/2022/02/17/202202172222038.png" alt="截屏2022-02-17 22.21.00" style="zoom: 40%;" />



* Copy the path of the given json file like:  **./generated_file/json/2020-2021-2.json**

* Run **generate_ics_file.py** to get the folder include ics files

  ```Linux
  ## The Sample input you can use ⬇️
  ./generated_file/json/2020-2021-2.json
  
  
  ## Output ⬇️
  [Success] Generate "./generated_file/ics/2020-2021-2/概率论及数理统计A*★(Mon 3-5).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/计算机组成原理*★(Mon 6-7).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/形势与政策★(Mon 10-11).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/数据、模型与决策-管理软件实践○(Mon 10-12).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/普通物理A2★(Tue 3-5).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/英语国家文化概况★(Tue 6-7).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/创业基础★(Tue 8-9).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/计算机网络*★(Tue 10-12).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/足球(初级)★(Wed 1-2).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/C#程序设计*★(Wed 3-5).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/算法分析与设计*★(Wed 10-12).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/计算机组成原理*★(Thur 1-2).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/JAVA程序设计*★(Thur 3-5).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/职业发展与就业指导★(Thur 6-7).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/概论(2)★(Thur 8-9).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/社会实践○(Thur 10-11).ics"
  [Success] Generate "./generated_file/ics/2020-2021-2/汇编语言A*★(Fri 6-8).ics"
  
  ```

  <img src="https://pic.freanja.cn/images/2022/02/17/202202172236055.png" alt="截屏2022-02-17 22.32.45" style="zoom:40%;" />



* View the generated ics file

  <img src="https://pic.freanja.cn/images/2022/02/17/202202172240908.png" alt="截屏2022-02-17 22.40.05" style="zoom:40%;" />

* Select all and open them. *If you use macos, you can **command+a**, **command+ o***

* Add all schedules to the calendar you create

  <img src="https://pic.freanja.cn/images/2022/02/17/202202172246491.png" alt="截屏2022-02-17 22.44.36" style="zoom:40%;" />
