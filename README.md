
# Avigilon Site Health Analysis 

The code is a Python script that reads a CSV file containing information about various video devices, filters the information based on certain criteria, and generates a summary report in a new CSV file. The script uses several libraries, including Pandas, Matplotlib, Numpy, TQDM, Datetime, OS, and CSV.

The script prompts the user to input the month and year for the inventory being taken and creates a directory to store all generated files. The main filtering function in the script is called Siphon, which reads data from the IslandView CSV file, iterates over the rows, and extracts the necessary information based on certain criteria. The extracted information is stored in lists for later use in generating the summary report.

The summary report contains information about the number of devices by model, the number of analog and digital devices, the number of gaming and BOH (back of house) cameras, the number of encoders, and the number of baluns. The report also includes a list of logical IDs for each model. The script writes the summary report to a new CSV file in the directory created earlier.

The script includes several comments and logic statements that are currently commented out but could be used to extend the functionality of the script in the future. The script is designed to be run on a Windows machine, and the parent directory for the CSV file and the new directory must be updated to match the user's file structure.



## Explanation of Variables:

**total_analog**: This converts the first element of the analog_count list to a string, then back to an integer. The variable total_analog represents the total number of analog cameras.

**total_digital**: This calculates the sum of the digital_counts list and converts it to an integer. The variable total_digital represents the total number of digital cameras.

**total_cameras**: This adds total_analog and total_digital together and converts the result to an integer. The variable total_cameras represents the total number of cameras.

**total_devices**: This calculates the sum of the counts list and converts it to an integer. The variable total_devices represents the total number of devices

**total_encoders**: This calculates the length of the encoder_list and converts it to an integer. The variable total_encoders represents the total number of encoders.

**total_ports**: This multiplies total_encoders by 4 and converts the result to an integer. The variable total_ports represents the total number of available ports.

**available_ports**: This subtracts total_analog from total_ports and converts the result to an integer. The variable available_ports represents the number of available ports for analog cameras.

**percentage_ports**: This calculates the percentage of ports being used by analog cameras, rounded to two decimal places. The variable percentage_ports represents the percentage of ports being used by analog cameras.

**type_data**: This creates a tuple of total_digital and total_analog. The variable type_data represents the number of digital and analog cameras, _respectively_.

**total_no_baluns**: This calculates the length of the no_balun_list and converts it to an integer. The variable total_no_baluns represents the total number of cameras without baluns.

**total_baluns**: This calculates the length of the balun_list and converts it to an integer. The variable total_baluns represents the total number of cameras with baluns.

**total_gaming_cams**: This calculates the length of the set of gaming_cams and converts it to an integer. The variable total_gaming_cams represents the total number of gaming cameras.

**total_boh**: This calculates the length of the set of boh_cams and converts it to an integer. The variable total_boh represents the total number of BOH (back-of-house) cameras.

**gaming_data**: This creates a tuple of total_gaming_cams and total_boh. The variable gaming_data represents the number of gaming cameras and BOH cameras, _respectively_.

**balun_data**: This creates a tuple of total_baluns and total_no_baluns. The variable balun_data represents the number of cameras with baluns and without baluns, _respectively_.