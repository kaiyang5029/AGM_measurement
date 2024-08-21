import pandas as pd
import matplotlib.pyplot as plt

files = ['FF3253_0.8nm.csv', 'FF3253_0.9nm.csv', 'FF3253_1.0nm.csv', 'FF3253_1.1nm.csv', 'FF3253_1.2nm.csv', 'FF3253_1.3nm.csv']
length1 = [4.02, 3.26, 3.30, 4.00, 4.26, 4.00]
length2 = [4.26, 4.26, 3.76, 3.84, 4.10, 4.28]
height = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

length1 = [x * 1e-1 for x in length1]
length2 = [x * 1e-1 for x in length2]
height = [x * 1e-7 for x in height]

for i in range(6):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(files[i], header=None, skiprows=4)
    # Constants
    Length1 = length1[i]
    Length2 = length2[i]
    CoThickness = height[i]
    Height = (0.2e-7 + CoThickness)*3
    Volume = Length1 * Length2 * Height
    print("Volume:", Volume)
    
    # Process the data
    df[3] = df[3] / Volume * 1e3
    df[2] = df[2] / 10
    
    # Extract column for x and y
    x = df[2]
    y = df[3]
    # Plot the data
    plt.plot(x, y, label = f'{height[i] * 1e7} nm')

# Customize the plot
plt.xlabel('B_extz (mT)')
plt.ylabel('M_z (A/m)')
plt.title('IrFeCo(x)Pt hysteresis')
plt.grid(True)
plt.legend()
plt.savefig('Hystereis_combined.png', dpi=300)
plt.show()