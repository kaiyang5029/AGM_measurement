import pandas as pd
import tkinter, os, re
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np

def UI_load_files():
    """
    load input files, and detect accompanying json options file (which has the same name, but with .json extension).
    """
    root = tkinter.Tk()
    filenames = filedialog.askopenfilenames(title='Select input data files...')
	# close the Tkinter window
    root.destroy()
	# if user cancelled
    if filenames == '':
        return None, None
    # assume all files are from the same common path
    path, _ = os.path.split(filenames[0])
    files = [file for file in filenames]    
     
    return path, files

path, files = UI_load_files()
files.sort()
print(files)

len = len(files)
i=0
Ms_list=[]
name = []

fig, axs = plt.subplots(len, 1, figsize=(10, 10), sharex=True, gridspec_kw={'hspace': 0, 'wspace': 0.4})
fig.suptitle("3355 AN IP", fontsize = 16)

while i<len:
    # read the magnetic volume in cc
    name.append(files[i].split("/")[-1])
    """length_re = r'(\d+\.\d+)x(\d+\.\d+)x(\d+\.\d+)'
    re_search = re.search(length_re, files[i])
    if re_search:
        length_x = float(re_search.group(1))    #mm
        length_y = float(re_search.group(2))    #mm
        length_z = float(re_search.group(3))    #nm
    mag_vol_cc = length_x*length_y*length_z*1e-9    #cc"""
    
    # Skip the headers and metadata
    start_line_re = r'\s+\(Oe\)\s+\(emu\)'
	# search for number for header lines
    with open(files[i], 'r') as text_file:
        header_line_count = 0
        for line_str in text_file:
            header_line_count += 1
            re_search = re.search(start_line_re, line_str)
            if re_search:
                break
	
    # Read the data
    df = pd.read_csv(files[i], skip_blank_lines=False, header=header_line_count, sep=',').to_numpy()
    df = (df[:-2,:]).astype(float)
	# Filter the data from NaN
    not_nan_mask = ~np.isnan(df[:,0]) &  ~np.isnan(df[:,1])
    df = df[not_nan_mask]
    # Process the data
    #df[:,3] = df[:,3] / mag_vol_cc * 1e3
    df[:,2] = df[:,2] / 10

    #Find the Ms
    filtered_df = df[-20:,3]
    print(filtered_df)
    Ms = filtered_df[:].mean()
    df[:,3] = df[:,3]/Ms
    df = df[abs(df[:,2])<200]
    Ms_list.append(Ms/1e6)
    ax = axs[i]
    ax.plot(df[:,2], df[:,3], label=name[i].split("_")[0])
    ax.legend()
    ax.grid()
    ax.set_ylim(-1.1,1.1)
    i+=1
        
# Spit out the Ms data
with open(os.path.join(path, f'Ms_data.txt'), 'w') as text_file:
        text_file.write('Filename Ms (MA/m)\n')
        for j in range(len):
            text_file.write(f"{name[j]} {Ms_list[j]}\n")
plt.xlabel("field (mT)")
fig.subplots_adjust(top=0.95)  # Adjust the top spacing to fit the title
plt.savefig('3355_ANN.png', dpi=600)
plt.show()
