import pandas as pd
import matplotlib.pyplot as plt
import os

directory = 'AGM_measurement/3267/'
files = os.listdir(directory)
files.sort()
print(files)

subtitle = '3267_Hs_Check'
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))  # Adjust figsize to your needs
fig.suptitle(subtitle, y=0.95, fontsize = 15)  # Overall title
axes = axes.flatten()
len = len(files)
i=0

#parameters = [f.split('_')[0] for f in files]
parameters = ['f390','f390.75','f392','f392_2','1k']
length1 = [4.2, 3.70, 4.04, 4.20, 3.58, 3.84]
length2 = [4.12,3.76, 4.20, 4.00, 4.00, 4.00]
"""
length1 = [3.88, 3.70, 4.10, 4.10, 4.06, 3.64, 4.10]
length2 = [4.04, 4.00, 3.90, 3.90, 4.08, 3.88, 4.10]
"""
#print(full_parameters)
output_file_path = os.path.join(directory, 'fitted_parameters.txt')
output_file = open(output_file_path, 'w') 
output_file.write("Sample Co_thickness Ms\n")

while i<len:
    # Load the CSV file into a DataFrame
#i=0
#if True:
    m = str.split(files[i],'_')
    print(m)
    height = float(m[4])
    #parameters = pd.read_csv(files[i], header=None, nrows=1, skiprows=86)
    df = pd.read_csv(directory + files[i], header=None, skiprows=90)
    index = int(round((height-0.6)*10,0))
    """
    # Constants
    Length1 = float(parameters[0])*1e-1
    Length2 = float(parameters[1])*1e-1
    CoThickness = float(parameters[2])*1e-7
    """
    #Height = (0.2e-7 + height[i])*3 #in cm
    
    #Volume = length1[i] * length2[i] * Height
    Volume = length1[index] * length2[index] * (height+0.2) * 1e-9

    # Process the data
    df[3] = df[3] / Volume * 1e3
    df[2] = df[2] / 10

    #Find the Ms
    filtered_df = df[df[2] > 500]
    Ms = filtered_df[3].mean()
    print(Ms/1e6)
    output_file.write(str(height) + " " + str(Ms/1e6) + "\n")
    '''
    # Extract column for x and y
    narrow_df = df[abs(df[2])<200]
    x = narrow_df[2]
    y = narrow_df[3]/Ms
    label_value = str(parameters[i])
    # Plot the data in mz
    #plt.plot(x, y/1e6, label = label_value)
    '''
    narrow_df = df[abs(df[2])<500]
    x = narrow_df[2]
    y = narrow_df[3]/Ms
    label_value = str(m[3])
    

    # Plot the data in scaled Ms
    #plt.plot(x, y, label = label_value)
    #plt.plot(x, y, label = f'Co: {thickness[i]} nm')
    """ax = axes[index]
    ax.plot(x, y, label = label_value)
    ax.set_title(height)
    ax.set_xlabel('B_extz (mT)')
    ax.set_ylabel('M_scaled')
    ax.grid(True)
    ax.legend()"""
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
