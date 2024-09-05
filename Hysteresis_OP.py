import pandas as pd
import matplotlib.pyplot as plt
import os

directory = 'AGM_measurement/Computing/'
files = os.listdir(directory)
files.sort()
print(files)

subtitle = '3136_Ms_Check'
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(10, 10))  # Adjust figsize to your needs
fig.suptitle(subtitle, y=0.95, fontsize = 15)  # Overall title
axes = axes.flatten()
len = len(files)
i=0
#parameters = [f.split('_')[0] for f in files]
parameters = ['3136A_G','3136B_G','3136C_G','3136D_G']
height = [0.8,0.9,1.0,1.1]
length1 = [4.02, 3.26,3.3,4]
length2 = [4.26, 4.26,3.76,3.84]
#print(full_parameters)

while i<len:
    # Load the CSV file into a DataFrame
#i=0
#if True:
    #parameters = pd.read_csv(files[i], header=None, nrows=1, skiprows=86)
    df = pd.read_csv(directory + files[i], header=None, skiprows=90)

    """
    # Constants
    Length1 = float(parameters[0])*1e-1
    Length2 = float(parameters[1])*1e-1
    CoThickness = float(parameters[2])*1e-7
    """
    #Height = (0.2e-7 + height[i])*3 #in cm
    
    #Volume = length1[i] * length2[i] * Height
    
    Volume = length1[i]*length2[i]*(height[i]+0.2)*3*1e-9
    # Process the data
    df[3] = df[3] / Volume * 1e3
    df[2] = df[2] / 10

    #Find the Ms
    filtered_df = df[df[2] > 500]
    Ms = filtered_df[3].mean()
    print(Ms/1e6)

    '''
    # Extract column for x and y
    narrow_df = df[abs(df[2])<200]
    x = narrow_df[2]
    y = narrow_df[3]/Ms
    label_value = str(parameters[i])
    # Plot the data in mz
    #plt.plot(x, y/1e6, label = label_value)
    '''
    narrow_df = df[abs(df[2])<200]
    x = narrow_df[2]
    y = narrow_df[3]/Ms
    label_value = str(parameters[i])
    

    # Plot the data in scaled Ms
    #plt.plot(x, y, label = label_value)
    #plt.plot(x, y, label = f'Co: {thickness[i]} nm')
    ax = axes[i]
    ax.plot(x, y, label = label_value)
    ax.set_title(label_value)
    ax.set_xlabel('B_extz (mT)')
    ax.set_ylabel('M_scaled')
    ax.grid(True)
    i+=1

    # Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect if the suptitle overlaps

# Show the plot

plt.savefig(subtitle+'.png', dpi=300)
plt.show()
    
"""
# Customize the plot
plt.xlabel('B_extz (mT)')
plt.ylabel('M_scaled')
#plt.ylabel('M_z (MA/m)')
plt.title('IrFeCo(x)')
plt.grid(True)
plt.legend()
plt.savefig('3267.png', dpi=300)
plt.show()
"""
