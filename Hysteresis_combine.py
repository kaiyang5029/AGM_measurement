import pandas as pd
import matplotlib.pyplot as plt
import os
"""
files = ['FF3253_0.8nm.csv', 'FF3253_0.9nm.csv', 'FF3253_1.0nm.csv', 'FF3253_1.1nm.csv', 'FF3253_1.2nm.csv', 'FF3253_1.3nm.csv']
length1 = [4.02, 3.26, 3.30, 4.00, 4.26, 4.00]
length2 = [4.26, 4.26, 3.76, 3.84, 4.10, 4.28]
height = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

length1 = [x * 1e-1 for x in length1]
length2 = [x * 1e-1 for x in length2]
height = [x * 1e-7 for x in height]
"""
directory = 'AGM_measurement/24-8-2024/'
files = [
        directory + '3276C2',
        directory + '3277A',
        directory + '3277B2',
        directory + '3278',
        directory + '3280',
        ]

len = len(files)

for i in range(len):
    # Load the CSV file into a DataFrame
    parameters = pd.read_csv(files[i], header=None, nrows=1, skiprows=86)
    df = pd.read_csv(files[i], header=None, skiprows=91)
    # Constants
    Length1 = float(parameters[0])*1e-1
    Length2 = float(parameters[1])*1e-1
    CoThickness = float(parameters[2])*1e-7
    Height = (0.2e-7 + CoThickness)*3 #in cm
    Volume = Length1 * Length2 * Height
    
    # Process the data
    df[3] = df[3] / Volume * 1e3
    df[2] = df[2] / 10

    #Find the Ms
    filtered_df = df[df[2] > 750]
    Ms = filtered_df[3].mean()
    
    # Extract column for x and y
    narrow_df = df[abs(df[2])<250]
    x = narrow_df[2]
    y = narrow_df[3]/Ms
    label_value = str(parameters.iloc[0, 3])
    # Plot the data in mz
    #plt.plot(x, y/1e6, label = label_value)

    # Plot the data in scaled Ms
    plt.plot(x, y, label = label_value)

# Customize the plot
plt.xlabel('B_extz (mT)')
plt.ylabel('M_scaled')
#plt.ylabel('M_z (MA/m)')
plt.title('AGM hysteresis')
plt.grid(True)
plt.legend()
plt.savefig('new.png', dpi=300)
plt.show()