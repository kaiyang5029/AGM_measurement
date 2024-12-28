import pandas as pd
import matplotlib.pyplot as plt
import os

directory = 'AGM_measurement/Computing/'
files = os.listdir(directory)
code_order = [ "3411A", "3355D","3411B","3355E","3411C","3355F"]
files.sort()
print(files)

# Function to extract the first part (code) of the filename
def extract_code(filename):
    # Split the filename by either "_" or " "
    if "_" in filename:
        return filename.split("_")[0]
    elif " " in filename:
        return filename.split(" ")[0]
    return filename  # Return the full name if no separator is found

# Sort the files based on the order of the codes in the list
files = sorted(files, key=lambda x: code_order.index(extract_code(x)) if extract_code(x) in code_order else len(code_order))

"""
length1 = [4.02, 3.26, 3.30, 4.00, 4.26, 4.00]
length2 = [4.26, 4.26, 3.76, 3.84, 4.10, 4.28]
height = [0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

length1 = [x * 1e-1 for x in length1]
length2 = [x * 1e-1 for x in length2]
height = [x * 1e-7 for x in height]
"""
suptitle = 'Cu comp'
fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 15))  # Adjust figsize to your needs
fig.suptitle(suptitle,y=0.95, fontsize = 15)  # Overall title
axes = axes.flatten()
len = len(files)
i=0
j=0
k=0
split = []
for f in files:
    if "_" in f:
        split.append(f.split("_"))
    else:
        split.append(f.split(" "))
print(len)
# Filter to include only even indices
#parameters = [full_parameters[i] for i in range(len) if i % 2 == 0]

while i<len/2:
    # Load the CSV file into a DataFrame
#i=0
#if True:
    #parameters = pd.read_csv(files[i], header=None, nrows=1, skiprows=86)
    print(i)
    df1 = pd.read_csv(directory + files[i], header=None, skiprows=91)
    df2 = pd.read_csv(directory + files[i+3], header=None, skiprows=91)
    #df3 = pd.read_csv(directory + files[i+2], header=None, skiprows=91)
    #print(i)
    """
    # Constants
    Length1 = float(parameters[0])*1e-1
    Length2 = float(parameters[1])*1e-1
    CoThickness = float(parameters[2])*1e-7
    """
    #Height = (0.2e-7 + height[i])*3 #in cm
    
    #Volume = length1[i] * length2[i] * Height
    
    Volume = 1
    # Process the data
    df1[3] = df1[3] / Volume * 1e3
    df1[2] = df1[2] / 10

    df2[3] = df2[3] / Volume * 1e3
    df2[2] = df2[2] / 10

    #df3[3] = df3[3] / Volume * 1e3
    #df3[2] = df3[2] / 10

    #Find the Ms
    filtered_df1 = df1[df1[2] > 180]
    Ms1 = filtered_df1[3].mean()
    filtered_df2 = df2[df2[2] > 180]
    Ms2 = filtered_df2[3].mean()
    #filtered_df3 = df3[df3[2] > 350]
    #Ms3 = filtered_df3[3].mean()

    '''
    # Extract column for x and y
    narrow_df = df[abs(df[2])<200]
    x = narrow_df[2]
    y = narrow_df[3]/Ms
    label_value = str(parameters[i])
    # Plot the data in mz
    #plt.plot(x, y/1e6, label = label_value)
    '''
    narrow_df1 = df1[abs(df1[2])<150]
    narrow_df2 = df2[abs(df2[2])<150]
    #narrow_df3 = df3[abs(df3[2])<120]
    x1 = narrow_df1[2]
    y1 = narrow_df1[3]/Ms1
    x2 = narrow_df2[2]
    y2 = narrow_df2[3]/Ms2
    #x3 = narrow_df3[2]
    #y3 = narrow_df3[3]/Ms3
    #label_value = str(parameters[j])
    label_value1 = split[i][0]+" "+split[i][1]
    label_value2 = split[i+3][0]+" "+split[i+3][1]
    #label_value3 = parameters[i+2]
    # Plot the data in scaled Ms
    #plt.plot(x, y, label = label_value)
    #plt.plot(x, y, label = f'Co: {thickness[i]} nm')
    ax = axes[j]
    ax.plot(x1, y1, label = label_value1)
    ax.plot(x2, y2, label = label_value2)
    #ax.plot(x3, y3, label = label_value3)
    ax.set_xlabel('B_extz (mT)')
    ax.set_ylabel('M_scaled')
    ax.legend()
    ax.grid(True)
    i+=1
    j+=1

    # Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust the rect if the suptitle overlaps

# Show the plot

plt.savefig(suptitle+'.png', dpi=300)
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
