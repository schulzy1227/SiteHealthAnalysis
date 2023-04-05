import pandas as pd
import re
from matplotlib import pyplot as plt
import numpy as np
from tqdm import tqdm
from datetime import datetime
import os
import csv
import shutil

parent_directory = "C:\\data_pull_downloads\\"
now = datetime.now()
formatted_date = now.strftime("%m-%d-%Y (%H:%M)")
filename = parent_directory + "device_totals.csv"

date = datetime.today().strftime('%m:%d:%Y')
month_year = "FEB2023"
# month_year = input("What is the month and year for this inventory? (format: JAN2023)")
path = os.path.join(parent_directory, month_year + '\\')
if os.path.exists(path):
    shutil.rmtree(path)
os.makedirs(path, exist_ok=True)

model_list = ("1.3C-H4SL-D1", "2.0C-H4A-D1-B", "2.0C-H4A-DC2", "2.0C-H4M-D1", "2.0C-H6M-D1",
              "2.0C-H4PTZ-DC30", "3.0C-H4A-D1-B", "3.0C-H4A-DC1-B",
              "3.0C-H4SL-D1", "3.0C-H4A-DO1-B", "24C-H4A-3MH-180", "2.0C-H5A-D1",
              "2.0C-H4PTZ-DP30", "2.0C-H5SL-D1", "3.0C-H5SL-D1", "4.0C-H5A-DO1", "3.0C-H4A-DC1", "1.3C-H5SL-D1",
              "12.0-H4F-DO1-IR", "2.0C-H4A-D2-B",
              "4.0C-H5A-D1", "2.0C-H4A-D1", "2.0C-H4A-D2", "9W-H3-3MH-DO1-B", "2.0C-H5A-PTZ-DP36", "2.0C-H5A-DC1",
              "15C-H4A-3MH-180",
              "4.0C-H5A-DC1", "5.0C-H6M-D1-IR", "5.0L-H4A-D1", "2.0C-H4A-DC1-B", "IMP121",
              "6.0L-H4F-DO1-IR", "2.0C-H5A-PTZ-DC36", "5.0C-H5A-BO2-IR", "12.0W-H5A-FE-DO1-IR", "6.0C-H5DH-DO1-IR",
              "ENC-4P-H264")
analog_serials = []
digital_counts = []
analog_count = []
counts = []
gaming_cams = []
boh_cams = []
encoder_list = []
balun_list = []
no_balun_list = []
total_no_baluns = int(len(no_balun_list))
total_baluns = int(len(balun_list))
total_gaming_cams = len(set(gaming_cams))
total_boh = len(set(boh_cams))
number_path = path + 'device_totals.csv'
logical_id_list = []

data = pd.read_csv(parent_directory + 'IslandView.csv', skiprows=198)
df = pd.DataFrame(data)
df.to_csv(path + 'df.csv')

def siphon(current_model):
    id_list = []
    ip_list = []
    rows = []
    for row in df.itertuples(index=False):
        server = row[0]
        serial_num = row[12]
        model_num = row[3]
        ip_add = str(row[8])
        logic_id = str(row[5])
        # Regex
        ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', ip_add)
        logicalID_match = re.match(r'.*Logical ID:(\d*)', logic_id)

        if server != "IslandView13":
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
                    logical_id_list.append(int(logicalID_str))
                    row = {
                        ' Model ': current_model,
                        ' ID ': logicalID_str,
                        ' IP Address ': ip_str,
                        ' Serial Number ': serial_num}
                    rows.append(row)

                if server != "IslandView13" and model_num != 'ENC-4P-H264':
                    # ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', str(row[8]))
                    if ip_match:
                        ip_str = ip_match.group(1).strip()
                        octets = ip_str.split('.')
                        if int(octets[3]) <= 199 and model_num != 'ENC-4P-H264' and ip_str not in balun_list:
                            balun_list.append(ip_str)
                        elif int(octets[3]) >= 200 and model_num != 'ENC-4P-H264' and ip_str not in no_balun_list:
                            no_balun_list.append(ip_str)
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

    df3 = pd.DataFrame(rows)
    df3.to_csv(path + 'device_list.csv', index=False, mode="a")

    # logic to make file showing all models and their totals
    with open(path + "device_totals.csv", "a") as final:
        final.writelines(f"{current_model}: {count}\n")

    with open(number_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=':')
        model_data = []
        count_data = []
        for row in reader:
            model_data.append(row[0])
            count_data.append(row[1])

    with open(path + "baluns.csv", "a") as baluns:
        baluns.write(f"There are {total_baluns} devices on baluns.\n\n")
        for balun in balun_list:
            baluns.writelines(f"{balun}\n")

    with open(path + "no_baluns.csv", "a") as no_baluns:
        no_baluns.write(f"There are {total_no_baluns} devices not on baluns.\n\n")
        for item in no_balun_list:
            no_baluns.writelines(f"{item}\n")

    for row in df.itertuples(index=False):
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
    csv_two = pd.read_csv(number_path, delimiter=':', header=None, names=['Model', 'Count'])
    model_data = csv_two['Model']
    count_data = csv_two['Count']
    with open(number_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=':')
        model_data = []
        count_data = []
        for row in reader:
            county = str(row[0])
            county_2 = float(row[1])
            county_3 = int(county_2)
            model_data.append(county)
            count_data.append(county_3)
    # pie chart to show what percentage of the total devices each model is
    for i in count_data:
        model_percentage = (i / sum(count_data) * 100)
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

    colors = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b", "#191970", "#F0F8FF", "#00FFFF", "#8A2BE2",
              "#5F9EA0",
              "#7FFF00", "#DC143C", "#006400", "#008B8B", "#B8860B", "#556B2F", "#BDB76B", "#ADFF2F", "#CD5C5C",
              "#E3CF57", "#8B2323",
              "#76EE00", "#CD2626", "#8B5742", "#FF34B3", "#FF8000", "#8B0000", "#71C671")

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


def make_db():
    new_column_header = f'{formatted_date}'.format(
        len(open(filename).readline().split(",")))
    if os.path.exists(filename):
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)

            if new_column_header not in headers:
                headers.append(new_column_header)
                rows = [row for row in reader]
                rows = [[row[i] if i < len(row) else counts[j] for i in range(len(headers))] for j, row in
                        enumerate(rows)]
                with open(filename, "w", newline="") as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(headers)
                    writer.writerows(rows)
    else:
        with open(filename, "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow([new_column_header])

filepath = 'C:\\data_pull_downloads\\device_totals.csv'

df2 = pd.read_csv(filepath)
subset_df = df2.iloc[0:, 1:]
num_rows = df2.shape[0]
num_cols = df2.shape[1]

def analyze_dataframe(df):
    result = {}

    # Analyze rows
    for i, row in df.iterrows():
        row_result = {'sum': row_sum(row), 'mean': row_mean(row), 'median': row_median(row), 'diff': row_diff(row),
                      'std': row_std(row), 'var': row_var(row), 'range': row_range(row),
                      'coeff_var': row_coeff_var(row)}
        result[f'row_{i}'] = row_result

    # Analyze columns
    for column_name, column_data in df.iteritems():
        result[column_name] = {'sum': column_sum(column_data)}

    return result


def row_sum(row):
    return row.sum()


def row_mean(row):
    return round(row.mean(), 1)


def row_median(row):
    return int(row.median())


def row_diff(row):
    # if row.max() - row.min() > 5:
    return row.max() - row.min()


def row_std(row):
    return round(row.std(), 1)


def row_var(row):
    return round(row.var(), 1)


def row_range(row):
    return row.max() - row.min()


def row_coeff_var(row):
    mean = row.mean()
    std = row.std()
    if mean == 0:
        return 0
    else:
        return round((std / mean) * 100, 1)


# count total devices of each column
def column_sum(column):
    return int(sum(column))

# Apply the row-level functions to each row of the DataFrame
row_sums = subset_df.apply(row_sum, axis=1)
row_means = subset_df.apply(row_mean, axis=1)
row_medians = subset_df.apply(row_median, axis=1)
row_diffs = subset_df.apply(row_diff, axis=1)
row_stds = subset_df.apply(row_std, axis=1)
row_vars = subset_df.apply(row_var, axis=1)
row_ranges = subset_df.apply(row_range, axis=1)
row_coeff_vars: object = subset_df.apply(row_coeff_var, axis=1)

column_sums = subset_df.apply(column_sum, axis=0)

# Combine the results into a single DataFrame
results_df = pd.DataFrame({
    'row sums': row_sums,
    'row means': row_means,
    'row medians': row_medians,
    'max difference': row_diffs,
    'standard deviation': row_stds,
    'variance': row_vars,
    'range': row_ranges,
    'coefficient of variation': row_coeff_vars
})

# make dataframe that has date and column totals of devices
totals_df = pd.DataFrame({'column sums': column_sums})

# Save the results to a CSV file
results_df.to_csv('C:\\data_pull_downloads\\inv_analysis\\results.csv', index=True)
totals_df.to_csv('C:\\data_pull_downloads\\inv_analysis\\totals.csv', index=True)

# run main function
main()
make_db()

'''Below is collected data for further comparisons'''
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

with open(path + 'numbers_x', 'a') as num_x:
    num_x.writelines(
        f'Total Analog: {total_analog}\n'
        f'Total Digital: {total_digital}\n'
        f'Total Cameras: {total_cameras}\n'
        f'Total Devices: {total_devices}\n'
        f'Total Encoders: {total_encoders}\n'
        f'Total Ports: {total_ports}\n'
        f'Available Ports: {available_ports}\n'
        f'Percentage of Ports in Use: {percentage_ports}%\n'
        f'Total Gaming Cameras: {total_gaming_cams}\n'
        f'Total Back-of-House Cameras: {total_boh}\n'
        f'Total Cameras Utilizing Baluns: {total_baluns}\n'
        f'Total Cameras Not Utilizing Baluns: {total_no_baluns}\n')

chart_gen()
