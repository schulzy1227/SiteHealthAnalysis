import pandas as pd
import re
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
import time
import os
import shutil

parent_directory = "C:\\data_pull_downloads\\"

model_list = ["1.3C-H4SL-D1", "2.0C-H4A-D1-B", "2.0C-H4A-DC2", "2.0C-H4M-D1", "2.0C-H6M-D1",
              "2.0C-H4PTZ-DC30", "3.0C-H4A-D1-B", "3.0C-H4A-DC1-B",
              "3.0C-H4SL-D1", "3.0C-H4A-DO1-B", "24C-H4A-3MH-180", "2.0C-H5A-D1",
              "2.0C-H4PTZ-DP30", "2.0C-H5SL-D1", "3.0C-H5SL-D1", "4.0C-H5A-DO1", "3.0C-H4A-DC1", "1.3C-H5SL-D1",
              "12.0-H4F-DO1-IR", "2.0C-H4A-D2-B",
              "4.0C-H5A-D1", "2.0C-H4A-D1", "2.0C-H4A-D2", "9W-H3-3MH-DO1-B", "2.0C-H5A-PTZ-DP36", "2.0C-H5A-DC1",
              "15C-H4A-3MH-180",
              "4.0C-H5A-DC1", "5.0C-H6M-D1-IR", "5.0L-H4A-D1", "2.0C-H4A-DC1-B", "IMP121",
              "6.0L-H4F-DO1-IR", "2.0C-H5A-PTZ-DC36", "5.0C-H5A-BO2-IR", "12.0W-H5A-FE-DO1-IR", "6.0C-H5DH-DO1-IR",
              "ENC-4P-H264"]
logo = """%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@&&&@@@@@@@@@*,,,,,,,,,,,*@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@&&&&@@,,################(,%%%%%,,@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@,((######################,%%%%%%%(,@@@@@@@@@@@@@@@@@
@@@@@%@@@@@&@@@,############################,%%%%%%%%%%,@@@@@@@@@@@@@@
@@&%&@@@@@@@/*###(#(((###((##################,%%%%%%%%%%%*/@@@@@@@@@@@
@@@@&&@@@@(,/#%%%%%%%%%%%%%##,,,##############,%%%%%%%%%%%%*#@@@@@@@@@
@@@&@@@@&,#%%%%%%%%%%%%%%%%%%%#%%,,%,,#########,%%%%%%%%%%%%%,@@@@@@@@
@@@@@@@@,#%%%%%%#%%%%%%%%%%%*,@@@@&@@@@@@,*####/#%%%%%%%%%%%%%,@@@@@@@
@@@@@@@,%##%%%%%%%%%%%%%*,@@@@@@@@@@@@@@%@@@@,*#,%%%%%%%%%%%%((,@@@@@@
@@@@@@,%%%%%%%%%%%%%%,,@@@@@@@@@@@&&@@@@@@@@@@@@,%%%%%%%%%%%%,#(,@@@@@
@@@@@@/%%%####%%%%,(#((@@@@@@&**@@@@@@@&/*#@@&@&/#%%%%%%%%%(*(((/@@@@@
@@@@&,########%**((((/@@@@@@@@@&**%@@@**@@@@@@@@&/#%%%%%%%,((((((,@@@@
@@@&&,#######,(((((((*@@@@@@@&@@@@**@*/@@@@@@@@@@*#%%%%#,((((((((,@@@@
@&&&&*#####*/(((((((((&&&@&&&@@@@@@**/@@@@@@@@@@%(###/,((((((((((*@@@@
&&&%&%,###,(((((((((((*@@@@@@&@@@@@%*&@@@@@@@@&&*##,((((((((((((,@@@@@
%&&%%%,##,((((((((((((,/@@@@&&@@@@@@@@@@@@@@&@@/,(((((((((((((((,@@@@@
%%%%&&&,*(((((((((((((,##(,&@@@@@@@@@@@@@@&%,((((((((((((((((((,@@@@@@
&&@%&&&&,((((((((((((((,######,*@@@@@@@*,(((((((((((((((((((((,&@@@@@@
&@&&&@@&&//((((((((((((*#(#########,,(((((((((((((((((((((((*(@@@@@@@@
&%&@&%@@&@@,((((((((((((,################(,,,/((((((((((*,*,@&@@@@@@@@
&&&&&@&&@@&@@,(((((((((((,##(######((###################(,@@%@@@@@@@@@
&%@@@@&@%@&@&@&&,(((((((((,(#(####(((#######((########,@@&&@@@@@%@@@@@
&&&&&@@&&&&&&&%&&&@,,(((((((,#(##################(,,@@@&&%%%@@@@@@@@&@
@@@@@&&@%&&&&&&@&&&&&&&%,,/(((,/###(########/,,@@@&%@@@@@@&&%@@@@@@@@@
&&&&@&&&&&@&&&@&&&&&&&@&&@@&&@&%%%&&@@@@@@@@@@@@@@@@@@@@&&&%%@@@@@@@@@"""
title_art = ("""
   _____                       _ ____                    
  / ___/__  ________   _____  (_) / /___ _____  ________ 
  \__ \/ / / / ___/ | / / _ \/ / / / __ `/ __ \/ ___/ _ \.
 ___/ / /_/ / /   | |/ /  __/ / / / /_/ / / / / /__/  __/
/____/\__,_/_/    |___/\___/_/_/_/\__,_/_/ /_/\___/\___/ 
                                                         
""")
opening_msg = """\nThis program is going to open up the CSV file that YOU downloaded and added to the 'C:/data_pull_downloads' folder. 
After the program is finished, you will have five(5) new files being: 
1)A dataframe used for further analyses.
2)A list of camera models and their total quantities.
3)A file with the amount of devices using baluns and a list of their IP Address'.
4)Lastly, a file for a bar graph will be generated.\n\n"""
digital_counts = []
total_digital = sum(digital_counts)
counts = []
analog_count = []


# print(logo)
# print(title_art)
# time.sleep(2.0)
# print(opening_msg)
# time.sleep(1.0)
# month_year = input("What is the month and year for this inventory? (format: JAN2023)")
month_year = 'Jan2023'

# logic to make new folder for all generated files
path = os.path.join(parent_directory, month_year + '\\')
# if path already exists, delete and make new
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)

# SIPHON is the main filtering function
def siphon(current_model):

    data = pd.read_csv(parent_directory + 'SiteHealth.csv', skiprows=198)
    df = pd.DataFrame(data)

    encoders = []
    id_list = []
    ip_list = []
    rows = []

    for index, row in df.iterrows():
        # Regex
        ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', str(row[8]))
        logicalID_match = re.match(r'.*Logical ID:(\d*)', str(row[5]))
        # Skip rows that start with Island View 13
        if row[0] != "IslandView13":
            # logic for finding missing model numbers
            if row[3] not in model_list:
                print(f"{row[3]} is not in your list of models. Please consider adding it before running the program again.")
            # logic for finding AMOUNT of encoders
            if row[3] == 'ENC-4P-H264':
                if ip_match:
                    ip_str = ip_match.group(1).strip()
                    if ip_str not in encoders:
                        encoders.append(ip_str)
                else:
                    continue

            # logic for matching models and stripping their ID and IP
            if row[3] == current_model:
                if ip_match:
                    ip_str = ip_match.group(1).strip()
                    ip_list.append(ip_str)
                else:
                    ip_str = "X"
                if logicalID_match:
                    logicalID_str = logicalID_match.group(1).strip()
                    id_list.append(logicalID_str)
                    row = {
                        ' Model ': current_model,
                        ' ID ': logicalID_str,
                        ' IP Address ': ip_str}
                    rows.append(row)
        else:
            continue

    # find amount of ID's in list
    count = len(set(id_list))

    # find totals for devices with multiple heads
    if current_model == "6.0C-H5DH-DO1-IR": # 2 cams per device
        digital_counts.append(count)
        count = count/2
    elif current_model == "24C-H4A-3MH-180": # 3 cams/device
        digital_counts.append(count)
        count = count/3
    elif current_model == "15C-H4A-3MH-180": # 3 cams/device
        digital_counts.append(count)
        count = count/3
    # replace ENC with analog cameras
    elif current_model == "ENC-4P-H264":
        current_model = "Analog Cameras"
        analog_count.append(count)

    if current_model != "Analog Cameras":
        digital_counts.append(count)
    counts.append(count)

    # logic to make dataframe out of ROWS and create new file
    df2 = pd.DataFrame(rows)
    df2.to_csv(path + 'dataframe.csv', index=False, mode="a")

    # logic to make file showing all models and their totals
    with open(path + "device_totals.csv", "a") as final:
        final.writelines(f"{current_model}: {count}\n")

def baluns_piechart():
    global total_no_baluns, total_baluns
    data = pd.read_csv(parent_directory + 'SiteHealth.csv', skiprows=198)
    df = pd.DataFrame(data)
    balun_list = []
    no_balun_list = []
    final_baluns_list = []
    final_no_baluns = []

    for index, row in df.iterrows():
        if row[0] != "IslandView13" and row[3] != 'ENC-4P-H264':
            ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', str(row[8]))
            if ip_match:
                ip_str = ip_match.group(1).strip()
                octets = ip_str.split('.')
                if int(octets[3]) < 200:
                    balun_list.append(ip_str)
                else:
                    no_balun_list.append(ip_str)
            else:
                continue

    for item in balun_list:
        if item not in final_baluns_list:
            final_baluns_list.append(item)
            total_baluns = int(len(final_baluns_list))

    for item in no_balun_list:
        if item not in final_no_baluns:
            final_no_baluns.append(item)
            total_no_baluns = int(len(no_balun_list))

    with open(path + "baluns.csv", "a") as baluns:
        baluns.write(f"There are {total_baluns} devices on baluns.\n\n")
        for balun in final_baluns_list:
            baluns.writelines(f"{balun}\n")

    with open(path + "no_baluns.csv", "a") as no_baluns:
        no_baluns.write(f"There are {total_no_baluns} devices not on baluns.\n\n")
        for item in final_no_baluns:
            no_baluns.writelines(f"{item}\n")

    balun_data = total_baluns, total_no_baluns

    plt.figure(figsize=(5, 5))
    plt.title('Cameras With/Without Baluns')
    plt.pie(balun_data, autopct='%.1f%%')
    plt.legend(['Baluns', 'No Baluns'], loc='upper right')
    plt.savefig(path + "baluns.png")
    plt.show()


def models_bargraph():
    number_path = path + 'device_totals.csv'
    csv = pd.read_csv(number_path, delimiter=':', header=None, names=['Model', 'Count'])
    model_data = csv['Model']
    count_data = csv['Count']
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b", "#191970", "#F0F8FF", "#00FFFF", "#8A2BE2",
              "#5F9EA0",
              "#7FFF00", "#DC143C", "#006400", "#008B8B", "#B8860B", "#556B2F", "#BDB76B", "#ADFF2F", "#CD5C5C",
              "#E3CF57", "#8B2323",
              "#76EE00", "#CD2626", "#8B5742", "#FF34B3", "#FF8000", "#8B0000", "#71C671"]
    fig = plt.figure(figsize=(7, 9))
    plt.bar(model_data, count_data, color=colors, width=1.0)
    plt.xticks(fontsize=7, rotation=90)
    plt.yticks(np.arange(min(count_data) - 1, max(count_data) + 10, 20.0), fontsize=8)
    plt.xlabel('Camera Model')
    plt.ylabel('Number of Devices')
    plt.title("Number of Devices by Model Number")
    plt.subplots_adjust(bottom=.25)
    plt.savefig(path + "models_barplot.png")
    plt.show()

# def find_gaming_cams():
    # future function using location column in main dataframe to decide whether a camera is gaming regulated
def compare_types():
    print(total_digital,"digital")
    print(total_analog,"analog")
def main():
    print("Scanning Site Health Report..")
    for current_model in tqdm(model_list, ascii=False, colour='green', desc='Scanning: ', miniters=1, unit='',
                              bar_format='{desc}{percentage:3.0f}%|{bar:20}'):
        siphon(current_model)
# run main function
main()
# make variables out of collected data
total_analog = int((sum(analog_count)))
total_digital = int((sum(digital_counts)))
total_devices = int(total_analog + total_digital)
# print data to screen
print(f"There are {total_analog} analogs and {total_digital} digitals")
print(f"There are {total_devices} total cameras and {sum(counts)} total devices")
compare_types()
# write total data to end of file
# with open(path + "device_totals.csv", "a") as final:
#     final.writelines(f"\nThere are {total_devices} total cameras and {sum(counts)} total devices")


# print("Dataframe File Created!")
# time.sleep(0.5)
# print("Totals File Created!")
# time.sleep(0.5)
# print("Baluns File Created!")
# time.sleep(1.0)
# print("\nLOADING Baluns Pie Chart...")
# time.sleep(2.5)
# baluns_piechart()
# print("This window will close after you close the graph.")
# print("LOADING Camera Model Bar Graph...")
# models_bargraph()

# time.sleep(3.0)
