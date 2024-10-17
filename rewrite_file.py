import pandas as pd
import matplotlib.pyplot as plt
import os
import re

directory = '/Users/kaiyangtan/Documents/GitHub/AGM_measurement/3276-3280/'
os.chdir(directory)
files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
files.sort()
print(files)

len = len(files)
i=0

while i<len:
    #parameters = pd.read_csv(files[i], header=None, nrows=1, skiprows=86)
    file_path = files[i]
    # Read the file line by line
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # Extract the length1, length2, and height from row 87 (index 86)
        for j, line in enumerate(lines):
            if j == 86:  # The 87th line (index starts from 0, so 86 is 87th)
                data = line.split(", ")  # Split by comma or space if needed
                length1 = float(data[0])
                length2 = float(data[1])
                height = float(data[2])
                print(f"Length1: {length1}, Length2: {length2}, Height: {height}")

    df = pd.read_csv(files[i], header=None, skiprows=91)
	
    """length_re = r'(\d+\.\d+)x(\d+\.\d+)x(\d+\.\d+)'
    re_search = re.search(length_re, files[i])
    if re_search:
        length_x = float(re_search.group(1))
        length_y = float(re_search.group(2))
        length_z = float(re_search.group(3))
		#Msat = float(re_search.group(4))
    else:
        print("No lengths found in filename.")"""
    mag_vol_cc = length1*length2*(height+0.2)*3*1e-9
    # Process the data
    H = df[2].copy()/1000
    raw_momemt = df[3].copy()
    M = df[3].copy()
    M = M/mag_vol_cc/1000
    filtered_df = df[df[2] > 5000]
    Ms = filtered_df[3].mean()
    M_norm = df[3]/Ms
    Ms = Ms/mag_vol_cc/1000

    file_path = f'{files[i]}_OP_AD_Ph_10kOe.txt'
    with open(file_path, 'w') as file:
        file.write(f"Ms(MA/m):{Ms}\n")
        file.write("H(kOe) moment(emu) M(MA/m) M_norm()\n")
        for a, b, c, d in zip(H, raw_momemt, M, M_norm):
            file.write(f"{a} {b} {c} {d}\n")  # Columns separated by spaces
    i+=1
