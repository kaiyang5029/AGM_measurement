import pandas as pd
import matplotlib.pyplot as plt

def process_data(files, length1, length2, height):
    length1 = [x * 1e-1 for x in length1]
    length2 = [x * 1e-1 for x in length2]
    height = [x * 1e-7 for x in height]
    
    averages = []  # List to store average values

    for i in range(len(files)):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(files[i], header=None, skiprows=4)
        # Constants
        Length1 = length1[i]
        Length2 = length2[i]
        CoThickness = height[i]
        Height = (0.2e-7 + CoThickness) * 3
        Volume = Length1 * Length2 * Height
        
        # Process the data
        df[3] = df[3] / Volume * 1e3
        df[2] = df[2] / 10

        # Filter df where df[2] > 750 and calculate the average of df[3]
        filtered_df = df[df[2] > 750]
        average_mz = filtered_df[3].mean()
        averages.append(average_mz)  # Append the average to the list

    return [h * 1e7 for h in height], averages

# New data
files_new = ['FF3253_0.8nm.csv', 'FF3253_0.9nm.csv', 'FF3253_1.0nm.csv', 'FF3253_1.1nm.csv', 'FF3253_1.2nm.csv', 'FF3253_1.3nm.csv']
length1_new = [4.02, 3.26, 3.30, 4.00, 4.26, 4.00]
length2_new = [4.26, 4.26, 3.76, 3.84, 4.10, 4.28]
height_new = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

# Old data
files_old = ['FP3136A_AD_3.3x3.3.csv','FP3136B_AD_3x3.csv','FP3136C_AD_3.8x3.8.csv','FP3136D_AD_3.5x4.csv','FP3136E_AD_3.8x3.9.csv','FP3136F_AD_2.7x3.2.csv']
length1_old = [3.3, 3.0, 3.8, 3.5, 3.8, 2.7]
length2_old = [3.3, 3.0, 3.8, 4.0, 3.9, 3.2]
height_old = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

# Process both sets of data
height_new_plot, averages_new = process_data(files_new, length1_new, length2_new, height_new)
height_old_plot, averages_old = process_data(files_old, length1_old, length2_old, height_old)

# Customize the plot
plt.plot(height_new_plot, averages_new, marker='o', linestyle='-', label='New Data')
plt.plot(height_old_plot, averages_old, marker='x', linestyle='-', label='Old Data')
plt.xlabel('Co_thickness (nm)')
plt.ylabel('Ms (A/m)')
plt.title('Ms Fluctuation (previous and new data)')
plt.grid(True)
plt.legend()
plt.savefig('Ms Fluctuation comparison.png', dpi=300)
plt.show()