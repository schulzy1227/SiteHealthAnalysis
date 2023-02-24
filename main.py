import pandas as pd
import re
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
from datetime import datetime
import os
import shutil

parent_directory = "C:\\data_pull_downloads\\"
date = datetime.today().strftime('%m:%d:%Y')
month_year = input("What is the month and year for this inventory? (format: JAN2023)")
path = os.path.join(parent_directory, month_year + '\\')

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
print(len(model_list))
analog_serials = []
# digital_serials = []
digital_counts = []
analog_count = []
counts = []
gaming_serial = []
boh_serial = []
gaming_cams = []
boh_cams = []
encoders = []
encoder_list = []
balun_list = []
no_balun_list = []
total_no_baluns = int(len(no_balun_list))
total_baluns = int(len(balun_list))
total_gaming_cams = len(set(gaming_cams))
total_boh = len(set(boh_cams))
number_path = path + 'device_totals.csv'

# logic to make new folder for all generated files
path = os.path.join(parent_directory, month_year + '\\')
# if path already exists, delete and make new
if os.path.exists(path):
    shutil.rmtree(path)
os.mkdir(path)


# SIPHON is the main filtering function
def siphon(current_model):
    data = pd.read_csv(parent_directory + 'IslandView.csv', skiprows=198)
    df = pd.DataFrame(data)

    id_list = []
    ip_list = []
    rows = []

    for index, row in df.iterrows():
        server = row[0]
        serial_num = row[12]
        model_num = row[3]
        ip_add = str(row[8])
        logic_id = str(row[5])
        # Regex
        ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', ip_add)
        logicalID_match = re.match(r'.*Logical ID:(\d*)', logic_id)
        # Skip rows that start with Island View 13
        if server != "IslandView13":
            # logic for finding missing model numbers
            if model_num not in model_list:
                print(
                    f"{model_num} is not in your list of models. Please consider adding it before running the program again.")
        # logic for finding AMOUNT of encoders using serial numbers
        if model_num == 'ENC-4P-H264' and serial_num not in encoder_list:
            encoder_list.append(serial_num)

        # logic for matching models and stripping their ID and IP
        if model_num == current_model:
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
                    ' IP Address ': ip_str,
                    ' Serial Number ': serial_num}
                rows.append(row)
        else:
            continue

    # find amount of ID's in list
    count = len(set(id_list))
    # convert to int
    count = int(count)

    # find totals for devices with multiple heads
    if current_model == "6.0C-H5DH-DO1-IR":  # 2 cams per device
        digital_counts.append(count)
        count = count / 2
    elif current_model == "24C-H4A-3MH-180" or current_model == "15C-H4A-3MH-180":  # 3 cams/device
        digital_counts.append(count)
        count = count / 3
    # replace ENC with analog cameras
    elif current_model == "ENC-4P-H264":
        current_model = "Analog Cameras"
        analog_count.append(count)
    if current_model != "Analog Cameras":
        digital_counts.append(count)
    counts.append(count)

    # logic to make dataframe out of ROWS and create new file
    df2 = pd.DataFrame(rows)
    df2.to_csv(path + 'device_list.csv', index=False, mode="a")

    # logic to make file showing all models and their totals
    with open(path + "device_totals.csv", "a") as final:
        final.writelines(f"{current_model}: {count}\n")

    csv = pd.read_csv(number_path, delimiter=':', header=None, names=['Model', 'Count'])
    model_data = csv['Model']
    count_data = csv['Count']
    # print(sum(count_data))
    # find cameras that are/ are not on balun
    for index, row in df.iterrows():
        server = row[0]
        model_num = row[3]

        if server != "IslandView13" and model_num != 'ENC-4P-H264':
            ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', str(row[8]))
            if ip_match:
                ip_str = ip_match.group(1).strip()
                octets = ip_str.split('.')
                if int(octets[3]) <= 199 and model_num != 'ENC-4P-H264' and ip_str not in balun_list:
                    balun_list.append(ip_str)
                elif int(octets[3]) >= 200 and model_num != 'ENC-4P-H264' and ip_str not in no_balun_list:
                    no_balun_list.append(ip_str)
        # elif ip_str not in no_balun_list:
        #         no_balun_list.append(ip_str)
        else:
            continue

    with open(path + "baluns.csv", "a") as baluns:
        baluns.write(f"There are {total_baluns} devices on baluns.\n\n")
        for balun in balun_list:
            baluns.writelines(f"{balun}\n")

    with open(path + "no_baluns.csv", "a") as no_baluns:
        no_baluns.write(f"There are {total_no_baluns} devices not on baluns.\n\n")
        for item in no_balun_list:
            no_baluns.writelines(f"{item}\n")
    # count gaming/non-gaming regulated cameras and make pie chart
    df4 = pd.DataFrame(data)
    for index, row in df4.iterrows():
        server = row[0]
        model_num = row[3]
        location = row[4]
        log_id = str(row[5])
        log_id = log_id.split(':')[-1].strip()
        if server == "IslandView13":
            continue

        # if location matches gaming check if that serial number is in gaming_cams list
        if location != "GAMING":
            if log_id not in boh_cams:
                boh_cams.append(log_id)
        elif location == "GAMING" and model_num == "ENC-4P-H264":
            gaming_cams.append(log_id)

        elif location == "GAMING":
            if log_id not in gaming_cams:
                gaming_cams.append(log_id)
            else:
                continue
        else:
            if log_id not in boh_cams:
                boh_cams.append(log_id)

    with open(path + 'gaming_cam_list.csv', "w") as gaming_list:
        for item in gaming_cams:
            gaming_list.writelines(f"{item}\n")

    with open(path + 'boh_cam_list.csv', 'w') as boh_list:
        for item in boh_cams:
            boh_list.write(f"{item}\n")

    with open(path + "gaming_cam_totals.txt", "a") as gaming_breakdown:
        gaming_breakdown.write(
            f"\nDATE: {date}\n________________\nTOTAL GAMING CAMERAS : {total_gaming_cams}\nTOTAL BOH CAMERAS : {total_boh}")


def chart_gen():
    csv = pd.read_csv(number_path, delimiter=':', header=None, names=['Model', 'Count'])
    model_data = csv['Model']
    count_data = csv['Count']

    for i in count_data:
        model_percentage = (i / sum(count_data) * 100)
        print(round(model_percentage),2)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, subplot_kw={'aspect': 'equal'}, figsize=(7, 7))
    ax1.pie(balun_data, autopct='%1.1f%%', textprops={'fontsize': 8}, colors=['red', 'blue'], shadow=True)
    ax1.legend(['With Balun', 'Without Balun'], loc='right', bbox_to_anchor=(2.0, 0.5))
    ax2.pie(gaming_data, autopct='%1.1f%%', textprops={'fontsize': 8}, colors=['grey', 'orange'], shadow=True)
    ax2.legend(['Gaming Cameras', 'Back of House'], loc='right', bbox_to_anchor=(2.1, 0.5))
    ax3.pie(type_data, autopct='%1.1f%%', textprops={'fontsize': 8}, colors=['purple', 'pink'], shadow=True)
    ax3.legend(['Digital Cameras', 'Analog Cameras'], loc='right', bbox_to_anchor=(2.1, 0.5))
    # title customization
    ax1.title.set_text('Cameras With/Without Baluns')
    ax1.title.set_size(12)
    ax2.title.set_text('Gaming Regulated Cameras vs BOH')
    ax2.title.set_size(12)
    ax3.title.set_text('Analog vs Digital Cameras')
    ax3.title.set_size(12)
    plt.savefig(path + 'pie_charts.png')

    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b", "#191970", "#F0F8FF", "#00FFFF", "#8A2BE2",
              "#5F9EA0",
              "#7FFF00", "#DC143C", "#006400", "#008B8B", "#B8860B", "#556B2F", "#BDB76B", "#ADFF2F", "#CD5C5C",
              "#E3CF57", "#8B2323",
              "#76EE00", "#CD2626", "#8B5742", "#FF34B3", "#FF8000", "#8B0000", "#71C671"]

    fig, ax = plt.subplots(figsize=(8, 8))
    plt.bar(model_data, count_data, color=colors, width=1.0)
    plt.xticks(fontsize=7, rotation=90)
    plt.yticks(np.arange(min(count_data) - 1, max(count_data) + 10, 20.0), fontsize=8)
    plt.xlabel('Camera Model')
    plt.ylabel('Number of Devices')
    plt.title("Number of Devices by Model Number")
    plt.subplots_adjust(bottom=.25)
    plt.savefig(path + 'bar_chart.png')

    plt.show()


def main():
    print("Scanning Site Health Report...")
    for current_model in tqdm(model_list, ascii=False, colour='green', desc='Scanning: ', miniters=1, unit='',
                              bar_format='{desc}{percentage:3.0f}%|{bar:20}'):
        siphon(current_model)


# run main function
main()

'''Below is collected data for further comparisons'''
print(digital_counts)
print(counts)
total_analog = str(analog_count[0])
total_analog = int(total_analog)
total_digital = (sum(digital_counts))
total_digital = int(total_digital)
total_cameras = (total_analog + total_digital)
total_cameras = int(total_cameras)
total_devices = int(sum(counts))
total_encoders = len(encoder_list)
total_ports = total_encoders * 4
available_ports = total_ports - total_analog
percentage_ports = round((total_analog / total_ports) * 100, 2)
type_data = total_digital, total_analog
total_no_baluns = int(len(no_balun_list))
total_baluns = int(len(balun_list))
total_gaming_cams = len(set(gaming_cams))
total_boh = len(set(boh_cams))
gaming_data = total_gaming_cams, total_boh
balun_data = total_baluns, total_no_baluns

chart_gen()


print(total_analog, ' total analog')
print(total_digital, ' total digital')
print(total_cameras, 'total cameras')
print(total_devices, ' total devices\n')

print(total_encoders, ' total encoders')
print(total_ports, ' total ports')
print(available_ports, ' available ports')
print(percentage_ports, ' percentage ports\n')

print(total_gaming_cams, " Gaming Cameras")
print(total_boh, ' total BOH')
print(total_baluns, ' total baluns')
print(total_no_baluns, ' no baluns')

with open(path + 'numbers_x', 'a') as num_x:
    num_x.writelines(
        f'{total_analog}, total analog\n'
        f'{total_digital}, total digital\n'
        f'{total_cameras}, total cameras\n'
        f'{total_devices}, total devices\n'
        f'{total_encoders}, total encoders\n'
        f'{total_ports}, total ports\n'
        f'{available_ports}, available ports\n'
        f'{percentage_ports}%, ports in use\n'
        f'{total_gaming_cams}, total gaming cameras\n'
        f'{total_boh}, total back of house\n'
        f'{total_baluns}, total cams with baluns.\n'
        f'{total_no_baluns}, total no baluns\n')
