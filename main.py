import pandas as pd
import re
from matplotlib import pyplot as plt
import numpy as np
from time import sleep
from progress.bar import Bar

model_list = ["1.3C-H4SL-D1", "2.0C-H4A-D1-B", "2.0C-H4A-DC2", "2.0C-H4M-D1", "2.0C-H6M-D1",
              "2.0C-H4PTZ-DC30", "3.0C-H4A-D1-B", "3.0C-H4A-DC1-B",
              "3.0C-H4SL-D1", "3.0C-H4A-DO1-B", "24C-H4A-3MH-180", "2.0C-H5A-D1",
              "2.0C-H4PTZ-DP30", "2.0C-H5SL-D1", "3.0C-H5SL-D1", "4.0C-H5A-DO1",
              "6.0L-H4F-DO1-IR", "2.0C-H5A-PTZ-DC36", "5.0C-H5A-BO2-IR", "12.0W-H5A-FE-DO1-IR", "6.0C-H5DH-DO1-IR"]
month_year = "JAN2023"

def main(model):
    data = pd.read_csv("C:\\data_pull_downloads\\SiteHealth.csv", skiprows=198)
    df = pd.DataFrame(data)

    id_list = []
    ip_list = []
    rows = []

    for index, row in df.iterrows():
        if row[0] != "IslandView13":
            if row[3] == current_model:
                ip_match = re.match(r'.*(.*[0-9]{3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', str(row[8]))
                if ip_match:
                    ip_str = ip_match.group(1).strip()
                    ip_list.append(ip_str)
                else:
                    ip_str = "X"

                logicalID_match = re.match(r'.*Logical ID:(\d*)', str(row[5]))
                if logicalID_match:
                    logicalID_str = logicalID_match.group(1).strip()
                    id_list.append(logicalID_str)
                    row = {
                        ' Model ': current_model,
                        ' ID ': logicalID_str,
                        ' IP Address ': ip_str}
                    rows.append(row)
                    #for i in progress.bar(range(rows)):
                        #sleep(0.02)
        else:
            continue

    count = len(set(id_list))
    if current_model == "6.0C-H5DH-DO1-IR":
        count = count / 2
    elif current_model == "24C-H4A-3MH-180":
        count = count / 3

    df2 = pd.DataFrame(rows)
    df2.to_csv('C:\\data_pull_downloads\\Dataframes\\' + month_year + '_dataframe.csv', index=False, mode="a")

    with open("C:\\data_pull_downloads\\Numbers\\" + month_year + ".csv", "a") as final:
        final.writelines(f"{current_model}: {count}\n")

    print(f'{current_model} === DONE')

def visualize():
    number_path = 'C:\\data_pull_downloads\\Numbers\\JAN2023.csv'

    csv = pd.read_csv(number_path, delimiter=':', header=None, names=['Model', 'Count'])
    model_data = csv['Model']
    count_data = csv['Count']
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b", "#191970", "#F0F8FF", "#00FFFF", "#8A2BE2",
              "#5F9EA0",
              "#7FFF00", "#DC143C", "#006400", "#008B8B", "#B8860B", "#556B2F", "#BDB76B", "#ADFF2F", "#CD5C5C"]
    fig = plt.figure(figsize=(5, 7))
    plt.bar(model_data, count_data, color=colors, width=1.0)
    plt.xticks(fontsize=7, rotation=90)
    plt.yticks(np.arange(min(count_data) - 1, max(count_data) + 10, 10.0), fontsize=8)
    plt.xlabel('Camera Model')
    plt.ylabel('Number of Devices')
    plt.title("Number of Devices by Model Number")
    plt.subplots_adjust(bottom=.25)
    plt.savefig('C:\\data_pull_downloads\\' + month_year + ".png")
    plt.show()

for current_model in model_list:
    main(current_model)
visualize()

