import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import colorcet as cc
import numpy as np

# Define image folder lists
image_folder_lists = {
    #'Complete': list(map(str, range(1, 49))),
    #'AML': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '13', '20', '21', '23', '24', '26', '27', '28', '29', '30', '31', '32', '35', '38', '41'],
    #'ALL': ['12', '14', '15', '16', '17', '18', '19', '21', '22', '23', '24', '25', '27', '28', '30', '31', '32', '33', '34', '36', '37', '39', '40','42', '43', '44', '45', '46', '47', '48'],
    #'CLL': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48'],
    #'CML': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '29', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48'],
    #'APML': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48'],
    'Test': ['2',  '4',  '6', '8',  '10','15', '16',  '21', '24', '25', '30','34','37', '42','45','46'],
    'Train':['1', '3', '5',  '7',  '9',  '11', '12', '13', '14', '17', '18', '19', '20',  '22', '23','26', '27','28', '29', '31', '32', '33', '35', '36', '38', '39', '40', '41', '43', '44', '47', '48']
    
}

# Create an empty DataFrame to store the merged data
merged_df = pd.DataFrame()

# Loop through each image folder list, merge data, and append to the merged_df DataFrame
for list_name, image_folder_list in image_folder_lists.items():
    print(f"Merging data for {list_name}...")
    print(len(image_folder_list))
    df_list = pd.DataFrame()
    for file in image_folder_list:
        excel_file = f"1000_HCM_Microscope_data/Annotation_v8/{file}_data.xlsx"
        df_1 = pd.read_excel(excel_file)
        df_list = df_list.append(df_1, ignore_index=True)
    
    # Add a column to identify the source list
    df_list['Source'] = list_name
    NS_frequency = df['Nuclear shape'].value_counts()
    total_NS_count = NS_frequency.sum()
    print(total_NS_count)
    # Append the merged data to the main DataFrame
    merged_df = merged_df.append(df_list, ignore_index=True)

# Display the first few rows of the merged DataFrame
print("Merged DataFrame:")
print(merged_df.head())

# Get the frequency of each 'Cell_type' for each list
cell_type_frequency = merged_df.groupby(['Source', 'Cell_type']).size().reset_index(name='Count')

# Display the DataFrame with counts
print("\nCell Type Count Across Lists:")
print(cell_type_frequency)

# Save the table to a CSV file
cell_type_frequency.to_csv('cell_type_counts_across_lists.csv', index=False)

# Plot bar graph
cell_type_frequency['Count'] =cell_type_frequency['Count'] / 25
# Define a custom color palette
custom_palette = sns.color_palette(cc.glasbey, n_colors=18)

# Set font size
font_size = 54

# Assuming you have a DataFrame named cell_type_frequency with columns: 'Cell_type', 'Count', 'Source'

# Plot bar graph
plt.figure(figsize=(30, 36))
ax = sns.barplot(data=cell_type_frequency, x='Count', y='Cell_type', hue='Source', palette=custom_palette, dodge=True,width=0.90)

# Add legend
ax.legend(title='Source', title_fontsize=36, prop={'size': 36}, loc='upper right')

# Annotate each bar with its count using ax.patches
for patch in ax.patches:
    width = patch.get_width()
    if not np.isnan(width):  # Skip if the value is NaN
        ax.text(width, patch.get_y() + patch.get_height() / 2, f'{int(width*25)}', va='center', fontsize=30)

# Customize the plot
plt.title('Train and Test Split Cell Count', fontsize=72)
plt.xlabel('', fontsize=font_size)
plt.ylabel('', fontsize=font_size)
plt.xticks([])
plt.tight_layout(pad=60.0)
plt.yticks(rotation=0, ha='right', fontsize=font_size)
sns.despine(left=True, bottom=True)

# Save the plot as an image file with higher DPI
plt.savefig('graph/train_test_split.png')#pdf', format='pdf')

# Show the plot
plt.show()
