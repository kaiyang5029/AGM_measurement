with open(OP_file_path, 'w') as file:
			file.write(f"Keff: {Keff_MJ_m3}\tMs:{M_sat_MAm}\n")
			file.write("H(kOe) moment(emu) M(MA/m) M_norm()\n")
			for a, b, c, d in zip(H_OP, raw_OP, OP_data[:,1]/1000, M_norm_OP):
				file.write(f"{a} {b} {c} {d}\n")  # Columns separated by spaces