# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 03:22:59 2024

@author: hp
"""

"""
This script is modified from one written by Viriya.
Calculates Keff from pairs of OP and IP measurement data.

Usage
-----
1. Prepare raw OP and IP data files. Ensure that the filename contains either 'OP' or 'IP'. The OP files must also contain the magnetic volume
in the correct format e.g. '33d OP vol2.24e-7cc.txt'
2. Run script
3. Select data files. Ensure that OP and IP are correctly matched.
4. See generated results.

Dependencies
------------
Tested on Python 3.7. All non-standard dependencies can be install using:
pip install numpy pandas matplotlib scipy

Good luck and code well!
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simps
from scipy.interpolate import interp1d
import tkinter, os, re
from copy import deepcopy
from tkinter import filedialog, Label, Button
import pandas as pd
import multiprocessing
from multiprocessing import Pool

class Analysis:

	level_region: int = 20 # region at the begining and end of data set, where the MH loop is assumed to be level (M=Ms)
	interpolation_multiple:int = 10
	remove_background: bool = False
	parser:str = 'agm' #'vsm', 'agm'

	def __init__(self, path):
		self.path = path

	@staticmethod
	def normalize(base_data, normalize_data):
		average_normalized = np.mean(normalize_data[0:10])
		average_base = np.mean(base_data[0:10])

		return average_normalized / average_base * base_data

	def interp_and_calc_area(self, x_basis, x, y):
		# flip basis if needed
		if x[-1] < x [0]:
			x_basis2 = x_basis[::-1]
			fill_val = (np.mean(y[-self.level_region:]), np.mean(y[:self.level_region]))
		else:
			x_basis2 = x_basis
			fill_val = (np.mean(y[:self.level_region]), np.mean(y[-self.level_region:]))

		# interpolate onto common basis, then calculate area using numerical integration
		y_interp = interp1d(x, y, fill_value=fill_val, bounds_error=False)(x_basis2)
		y_interp_abs = np.abs(y_interp)
		area = np.abs(simps(y_interp_abs, x_basis2))
		# y_interp = np.interp(x_basis, x, y, left=np.mean(y[:self.level_region]), right=np.mean(y[-self.level_region:]))
		return x_basis2, y_interp, area
    
	def interp_only(self, x_basis, x, y):
		# flip basis if needed
		if x[-1] < x [0]:
			x_basis2 = x_basis[::-1]
			fill_val = (np.mean(y[-self.level_region:]), np.mean(y[:self.level_region]))
		else:
			x_basis2 = x_basis
			fill_val = (np.mean(y[:self.level_region]), np.mean(y[-self.level_region:]))

		# interpolate onto common basis, then calculate area using numerical integration
		y_interp = interp1d(x, y, fill_value=fill_val, bounds_error=False)(x_basis2)
		# y_interp = np.interp(x_basis, x, y, left=np.mean(y[:self.level_region]), right=np.mean(y[-self.level_region:]))
		return x_basis2, y_interp

	def background_removal(self, data):
		IND_FIELD = 0
		IND_MOMENT = 1
		data_out = deepcopy(data)
		bg_slope = np.polyfit(data[0:self.level_region, IND_FIELD], data_out[0:self.level_region, IND_MOMENT], 1)[0]
		data_out[:, IND_MOMENT] = data[:, IND_MOMENT] - bg_slope * data[:, IND_FIELD]
		return data_out

	def proc_MH_loop(self, data, y_normalisation, x_basis):
		# MH loop is assumed to be a LOOP, i.e. contains both forward half and return half
		x, y = data[:, 0], data[:, 1]

		# normalise if needed
		if not y_normalisation is None:
			y_self = (np.mean(np.abs([y[:self.level_region], y[-self.level_region:]])))
			y = y * y_normalisation / y_self

		# x is assumed to be continuously increasing, peak at flip_ind, then continously decreasing (or the other way round)
		extrema_ind = np.array([np.argmax(x), np.argmin(x)])
		# turning_pt is assumed to be the one closest to the middle to the array
		turning_ind = extrema_ind[np.argmin(np.abs(extrema_ind - len(x)/2))]

		# split data
		x1, x2 = x[:turning_ind], x[turning_ind:]
		y1, y2 = y[:turning_ind], y[turning_ind:]

# 		x1_interp, y1_interp, area1 = self.interp_and_calc_area(x_basis, x1, y1)
# 		x2_interp, y2_interp, area2 = self.interp_and_calc_area(x_basis, x2, y2)
		x1_interp, y1_interp = self.interp_only(x_basis, x1, y1)
		x2_interp, y2_interp = self.interp_only(x_basis, x2, y2)
# 		# remove background
# 		if self.remove_background:
# 			OP_data = self.background_removal([x1_interp, y1_interp])
# 			IP_data = self.background_removal([x2_interp, y2_interp])

		if not y_normalisation is None:
			y1_self = (np.mean(np.abs([y1_interp[:self.level_region], y1_interp[-self.level_region:]])))
			y1_interp = y1_interp * y_normalisation / y1_self
			y2_self = (np.mean(np.abs([y2_interp[:self.level_region], y2_interp[-self.level_region:]])))
			y2_interp = y2_interp * y_normalisation / y2_self
		y1_interp_abs = np.abs(y1_interp)
		area1 = np.abs(simps(y1_interp_abs, x1_interp))
		y2_interp_abs = np.abs(y2_interp)
		area2 = np.abs(simps(y2_interp_abs, x2_interp))

            
		return x1_interp, y1_interp, area1, x2_interp, y2_interp, area2

	def execute(self, OP_file, IP_file):
		# read in IP, OP files
		_, OP_file2 =  os.path.split(OP_file)
		_, IP_file2 =  os.path.split(IP_file)
		label = f'{OP_file2}_{IP_file2}'

		if self.parser == 'agm':
			OP_data, mag_vol_cc = AGM_MH_parser(OP_file)
			IP_data, _ = AGM_MH_parser(IP_file)
		elif self.parser == 'vsm':
			OP_data, mag_vol_cc = VSM_MH_parser(OP_file)
			IP_data, _ = VSM_MH_parser(IP_file)
		else:
			raise ValueError('Unknown parser option.')

		if mag_vol_cc is None: mag_vol_cc = (2e-7*0.2*0.2);
        
            # continue;
# 			raise Exception('Magnetic volume not found in OP filename! Example: vol2.24e-7cc')

		# remove background
		if self.remove_background:
			OP_data = self.background_removal(OP_data)
			IP_data = self.background_removal(IP_data)
# 		y_corr_OP= (1.538e-9*OP_data[:,0]) #subtracts slope
# 		y_corr_IP= (1.538e-9*IP_data[:,0]) #subtracts slope

# 		OP_data[:,1]=OP_data[:,1]- y_corr_OP/2;
# 		IP_data[:,1]=OP_data[:,1]- y_corr_IP/2;

		# convert to magnetisation
		OP_data[:,1] /= mag_vol_cc
		IP_data[:,1] /= mag_vol_cc
		x_min, x_max = np.min(np.concatenate(([OP_data[:, 0], IP_data[:, 0]]))), np.max(np.concatenate(([OP_data[:, 0], IP_data[:, 0]])))
		B_frac= 1
        
		# interp/ extrapolate to 10x the number of data points of the max of OP or IP loop
		x_basis = np.linspace(x_min*B_frac, x_max*B_frac, self.interpolation_multiple*np.max([len(OP_data[:, 0]), len(IP_data[:, 0])]))
        
		# normalise IP to OP
# 		tmp = np.concatenate(([OP_data[:self.level_region,1], OP_data[-self.level_region:,1]]))
		tmp = np.concatenate(([OP_data[:self.level_region,1], OP_data[-self.level_region:,1],IP_data[:self.level_region,1], IP_data[-self.level_region:,1]]))

		M_sat = np.mean(np.abs(tmp)); #print(tmp)
		M_sat_MAm = M_sat/1000

		OP_x1_interp, OP_y1_interp, OP_area1, OP_x2_interp, OP_y2_interp, OP_area2 = self.proc_MH_loop(OP_data, M_sat, x_basis)
		IP_x1_interp, IP_y1_interp, IP_area1, IP_x2_interp, IP_y2_interp, IP_area2 = self.proc_MH_loop(IP_data, M_sat, x_basis)

		# calc area
		erg_cc_to_MJ_m3: float = 1e-7  # 1 erg/cc to MJ/m^3
		Keff_erg_cc = (OP_area1 + OP_area2 - IP_area1 - IP_area2)/4 # in erg/cc
# 		Keff_erg_cc = (OP_area1 + OP_area2)/4 # in erg/cc

		Keff_MJ_m3 = Keff_erg_cc * erg_cc_to_MJ_m3
		print(f'{label}: Ms = {M_sat_MAm:3g} MA/m, Keff = {Keff_MJ_m3:3g} MJ/m^3.')

		# plotting
		fig = plt.figure(figsize=(10, 5))
		ax1, ax2 = fig.subplots(1, 2, sharex='all', sharey='all')
		# original
		ax1.plot(OP_data[:,0], OP_data[:, 1], '-', color='k', label='OP')
		ax1.plot(IP_data[:,0], IP_data[:, 1], '-', color='r', label='IP')
		ax1.legend()
		ax1.set_xlabel('Field (Oe)')
		ax1.set_ylabel('Magnetisation (emu/cc)')
		ax1.set_title(f'Original')
		ax1.set_xlim(-5000, 5000)
		# extrapolated and normalised
		ax2.plot(OP_x1_interp, OP_y1_interp, '-', color='k', label='OP1')
		ax2.plot(OP_x2_interp, OP_y2_interp, '--', color='k', label='OP2')
		ax2.plot(IP_x1_interp, IP_y1_interp, '-', color='r', label='IP1')
		ax2.plot(IP_x2_interp, IP_y2_interp, '--', color='r', label='IP2')
		ax2.set_xlabel('Field (Oe)')
		ax2.set_xlim(-5000, 5000)
		# ax2.set_ylabel('Magnetisation (emu/cc)')
		ax2.set_title(f'Corrected\nMs = {M_sat_MAm:3g} MA/m\nKeff = {Keff_MJ_m3:3g} MJ/m^3.')

		fig.savefig(os.path.join(self.path, f'{label} plot.png'), dpi=300)
		plt.close('all')

		return label, M_sat_MAm, Keff_MJ_m3


def main():

	path, OP_IP_files = UI_load_files()

    
	if path is None:
		return

	output_path = os.path.join(path,'output')
	if not os.path.exists(output_path):
		os.mkdir(output_path)
	analysis = Analysis(output_path)
    
    
	# update plot style
	style_dict = {'figure.dpi': 300, 'font.sans-serif': 'Arial', 'font.size': 18, 'legend.fontsize': 'x-small', 'savefig.bbox': 'tight',
				  'savefig.pad_inches': 0.0, 'savefig.transparent': False}
	plt.rcParams.update(style_dict)

	# save Keff results
	num_procs = multiprocessing.cpu_count()
	with Pool(processes=num_procs) as p:
		# read in all these files as one dataset
		calc_results = p.starmap(analysis.execute, OP_IP_files)

	# write result to file
	with open(os.path.join(output_path, f'Keff_data.txt'), 'w') as text_file:
		text_file.write('Filename (OP_IP)\tMs (MA/m)\tKeff (MJ/m^3)\n')
		for calc_result in calc_results:
			text_file.write(f'{calc_result[0]}\t{calc_result[1]}\t{calc_result[2]}\n')

def AGM_MH_parser(path_and_filename):

	_, filename = os.path.split(path_and_filename)

	# Try to read volume from filename
	mag_vol_cc = None
	mag_vol_cc_re = r'vol(.+)cc'
	re_search = re.search(mag_vol_cc_re, filename)
	if re_search:
		mag_vol_cc = float(re_search.group(1))

	# Hard coded to AGM format!
	start_line_re = r'\s+\(Oe\)\s+\(emu\)'
	# search for number for header lines
	with open(path_and_filename, 'r') as text_file:
		header_line_count = 0
		for line_str in text_file:
			header_line_count += 1
			re_search = re.search(start_line_re, line_str)
			if re_search:
				break
	# read in data. pandas is FAST!
	data_in = pd.read_csv(path_and_filename, skip_blank_lines=False, header=header_line_count, sep=',').to_numpy()
	# remove last two rows
	data_in = (data_in[:-2,2:]).astype(float)
	# Filter the data from NaN
	not_nan_mask = ~np.isnan(data_in[:,0]) &  ~np.isnan(data_in[:,1])
	data_in = data_in[not_nan_mask]

	# return data and magnetic volume
	return data_in, mag_vol_cc

def VSM_MH_parser(path_and_filename):

	_, filename = os.path.split(path_and_filename)

	# Try to read volume from filename
	mag_vol_cc = None
	mag_vol_cc_re = r'vol(.+)cc'
	re_search = re.search(mag_vol_cc_re, filename)
	if re_search:
		mag_vol_cc = float(re_search.group(1))

	# Hard coded to VSM format!
	start_line_re = r'New Section: Section (\d+):'
	end_line_re = r'@@END Data.'
	separator = r'   '
	reading_data = False
	data_in = []
	field_col = 5
	moment_col = 11
	# search for number for header lines
	with open(path_and_filename, 'r') as text_file:
		header_line_count = 0
		for line_str in text_file:
			header_line_count += 1
			if reading_data is False:
				re_search = re.search(start_line_re, line_str)
				if re_search:
					reading_data = True
			else:
				re_search = re.search(end_line_re, line_str)
				if re_search:
					break
				else:
					data_in.append(np.fromstring(line_str, dtype=float, sep=separator))

	# return data and magnetic volume
	return np.array(data_in)[:, [field_col, moment_col]], mag_vol_cc

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

	OP_files = [file for file in filenames if 'OP' in file  ]
	IP_files = [file for file in filenames if 'IP' in file]

	assert len(OP_files) == len(IP_files)

	OP_IP_files = list(zip(OP_files, IP_files))

	# print for user to check
	padding = {'ipadx': 5, 'ipady': 5, 'padx': 5, 'pady': 5}
	window = tkinter.Tk()
	window.option_add('*Font', '20')
	window.title('Check OP/IP files match')  # .geometry('400x400')
	selected_option = [None]

	def clicked(selection, option):
		def callback():
			selection[0] = option
			# print(f'Button {i} clicked')
			window.destroy()
		return callback

	Label(window, text='Please check that the following OP/IP files are correctly matched.').grid(column=0, columnspan=3, row=0, **padding)
	for i, files in enumerate(OP_IP_files):
		Label(window, text=os.path.split(files[0])[1]).grid(column=0, row=i+1, **padding)
		Label(window, text='<===>').grid(column=1, row=i+1, **padding)
		Label(window, text=os.path.split(files[1])[1]).grid(column=2, row=i+1, **padding)

	Button(window, text='Yes', command=clicked(selected_option, True)).grid(column=0, row=len(OP_IP_files)+1, **padding)
	Button(window, text='No', command=clicked(selected_option, False)).grid(column=2, row=len(OP_IP_files)+1, **padding)

	window.mainloop()

	if selected_option[0]:
		return path, OP_IP_files
	else:
		return None, None

# run the main function
if __name__ == '__main__':
	main()