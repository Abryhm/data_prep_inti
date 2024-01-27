import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import colorcet as cc


# Load the merged Excel file into a DataFrame
#file_path = '1000_HCM_Microscope_data/Annotation/merge_data.xlsx'  # Replace with the path to your merged Excel file
#df = pd.read_excel(file_path)
#print(df.head)
folder_path = '1000_HCM_Microscope_data/Annotation_v8/'

# Get a list of all Excel files in the folder
image_folder_list_Complete = list(map(str, range(1, 49)))
image_folder_list_AML=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '13', '20', '21', '23', '24', '26', '27', '28', '29', '30', '31', '32', '35',  '38', '41']
image_folder_list_ALL=[ '12', '14', '15', '16', '17', '18', '19', '21', '22', '23', '24', '25', '27', '28', '30', '31', '32', '33', '34', '36', '37', '39', '40','42', '43', '44', '45', '46', '47', '48']
image_folder_list_CLL=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48']
image_folder_list_CML=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '29', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48']
image_folder_list_APML=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48']
image_folder_list_train=['1', '3', '5',  '7',  '9',  '11', '12', '13', '14',  '17', '18', '19',  '22', '23', '27', '29', '31', '32', '33', '35', '36', '38', '39', '40', '41', '43', '45', '46', '47', '48']
image_folder_list_test=['2',  '4',  '6', '8',  '10', '16', '15','20', '21', '24', '25', '26','28', '30','34','37', '42','44']
# Create an empty DataFrame to store the merged data
df = pd.DataFrame()

# Loop through each Excel file and append its data to the merged_data DataFrame
for file in image_folder_list_Complete:
    #print(file)
    excel_file = f"1000_HCM_Microscope_data/Annotation_v8/{file}_data.xlsx"
    #file_path = os.path.join(folder_path, file)
    df_1 = pd.read_excel(excel_file)
    df = df.append(df_1, ignore_index=True)
df['Cell_type'] = df['Cell_type'].str.capitalize()
#df.to_excel('complete_data.xlsx', index=False)
# Display the first few rows of the DataFrame to understand its structure
#print(df.head())


# Get the frequency of each 'Cell_type'

#df = df[df['Cell_type'] != 'None']  #cell type withour None"
cell_type_frequency = df['Cell_type'].value_counts()
total_cell_type_count = cell_type_frequency.sum()

cell_type_frequency = df['Cell_type'].value_counts()

# Calculate the total count
total_cell_type_count = cell_type_frequency.sum()

# Plot bar graph
plt.figure(figsize=(30, 15))

custom_palette =sns.color_palette(cc.glasbey, n_colors=18)# Add more colors as needed
font_size = 48

# Plot bar graph

plt.figure(figsize=(30, 24))
print(cell_type_frequency )
print(total_cell_type_count)
cell_type_frequency.plot(kind='bar', color=custom_palette, edgecolor='black',width=0.85)

# Add data labels and percentages
for i, count in enumerate(cell_type_frequency):
    percentage = (count / total_cell_type_count) * 100
    plt.text(i, count + 15, f'{count}', ha='center', fontsize=font_size) #\n({percentage:.2f}%)

# Customize the plot
plt.title('Count of Cell Types', fontsize=88,)
plt.xlabel('', fontsize=72)
plt.ylabel('', fontsize=0)
plt.yticks([])
sns.despine(left=True, bottom=True)
plt.xticks(rotation=60, ha='right', fontsize=72)  # Rotate x-axis labels for better visibility
plt.yticks(fontsize=48)  # Set font size for y-axis labels
plt.tight_layout()

# Show the plot
plt.savefig(f'graph/cell_types.pdf', format='pdf')
Cell_Size_frequency = df['Cell Size'].value_counts()
total_Cell_Size_count = Cell_Size_frequency.sum()

NC_frequency = df['Nuclear Chromation'].value_counts()
total_NC_count = NC_frequency.sum()

NS_frequency = df['Nuclear shape'].value_counts()
total_NS_count = NS_frequency.sum()

Nucleous_type_frequency = df['Nucleous'].value_counts()
total_Nucleous_type_count = Nucleous_type_frequency.sum()

Cytoplasm_type_frequency = df['Cytoplasm'].value_counts()
total_Cytoplasm_type_count = Cytoplasm_type_frequency.sum()

CB_frequency = df['Cytoplasmic basophilia'].value_counts()
total_CB_count = CB_frequency.sum()

CV_frequency = df['Cytoplasmic vacuoles'].value_counts()
total_CV_count = CV_frequency.sum()
# Get the count of total unique 'Name' values
unique_name_count = df['Name'].nunique()

# Display the result
#print("Total number of  Images:", unique_name_count)

#print("\n Number of cell  of each 'Cell_type':")
#print(cell_type_frequency)
#print(Cell_Size_frequency)
#print(NS_frequency)
#print(NC_frequency)
#print(Nucleous_type_frequency)
#print(Cytoplasm_type_frequency)
#print(CB_frequency)
#print(CV_frequency)
# Get the total count of all unique 'Cell_type' values
custom_palette = sns.color_palette(cc.glasbey, n_colors=18)
class_mapping_1 = {0: 'Small', 1: 'Medium', 2: 'Large'} 
class_mapping_2= {0: 'Open', 1: 'Coarse'} 
class_mapping_3 = {0: 'Regular', 1: 'Irregular'} 
class_mapping_4 = {0: 'Inconspicuous', 1: 'Prominent'} 
class_mapping_5 = {0: 'Scanty', 1: 'Abundent'} 
class_mapping_6 = {0: 'Slight', 1: 'Moderate'} 
class_mapping_7 = {0: 'Absent', 1: 'Prominent'} 
type_of_cell_list = ['Cell Size','Nuclear Chromation','Nuclear shape','Nucleous','Cytoplasm','Cytoplasmic basophilia','Cytoplasmic vacuoles']
for type_of_cell in type_of_cell_list:
    # Filter the DataFrame and group by 'Cell_type' and the current 'type_of_cell'
    filtered_df_none = df[df['Cell_type'] != 'None']
    
    filtered_df_none['Cell Size']= filtered_df_none['Cell Size'].map ({0: 'Small', 1: 'Medium', 2: 'Large'}) 
    filtered_df_none['Nuclear Chromation']= filtered_df_none['Nuclear Chromation'].map ({0: 'Open', 1: 'Coarse'} ) 
    filtered_df_none['Nuclear shape']= filtered_df_none['Nuclear shape'].map ({0: 'Regular', 1: 'Irregular'} ) 
    filtered_df_none['Nucleous']= filtered_df_none['Nucleous'].map ({0: 'Inconspicuous', 1: 'Prominent'} ) 
    filtered_df_none['Cytoplasm']= filtered_df_none['Cytoplasm'].map ({0: 'Scanty', 1: 'Abundent'} ) 
    filtered_df_none['Cytoplasmic basophilia']= filtered_df_none['Cytoplasmic basophilia'].map ( {0: 'Slight', 1: 'Moderate'}) 
    filtered_df_none['Cytoplasmic vacuoles']= filtered_df_none['Cytoplasmic vacuoles'].map ({0: 'Absent', 1: 'Prominent'} ) 
        
       
       
    count_df = filtered_df_none.groupby(['Cell_type', f'{type_of_cell}']).size().reset_index(name='count')

    # Divide the count by ten
    count_df['count'] = count_df['count'] / 20

    # Plot using seaborn
    plt.figure(figsize=(66, 42))
    custom_palette = sns.color_palette(cc.glasbey, n_colors=18)
    ax = sns.barplot(x='count', y='Cell_type', hue=f'{type_of_cell}', data=count_df, palette=custom_palette,
                     edgecolor="0.6", linewidth=0.0, saturation=2.5, dodge=True,width=0.85)
    ax.legend(title=f'{type_of_cell}', title_fontsize=124, prop={'size': 88},loc='upper right')
    # Display total count in front of each non-empty bar
    for i, p in enumerate(ax.patches):
        if not pd.isna(p.get_width()) and p.get_width() != 0:
            total_count = int(p.get_width() * 20)  # Multiply by 10 to get the total count
            ax.annotate(f'{total_count}', ((p.get_width() + 2, p.get_y() + p.get_height() / 2)),
                        ha='center', va='center', xytext=(40, -2), textcoords='offset points', fontsize=88)
        else:
            total_count = p.get_width() if not pd.isna(p.get_width()) else 0
            ax.annotate(f'{total_count}', ((p.get_width() + 15, p.get_y() + p.get_height() / 2)),
                        ha='center', va='center', xytext=(40, -2), textcoords='offset points', fontsize=88)

    # Customize the plot
    plt.title(f'Count of {type_of_cell} for Each Cell Type', fontsize=144)
    plt.xlabel('', fontsize=0)
    plt.xticks([])
    plt.ylabel('', fontsize=0)
    plt.xticks(rotation=45)
    plt.tight_layout(pad=2.0) 
    ax.tick_params(axis='x', labelsize=124)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=124)
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=124)  # Add this line to increase x-axis labels font size
    sns.despine(left=True, bottom=True)
    plt.tight_layout(pad=2.0) 
    plt.savefig(f'graph/{type_of_cell}.pdf', format='pdf')
    #plt.show()



# Show the plot
#plt.show()
filtered_df = df[((df['Cell_type'] == "Monocyte"))] #& (df['Cell Size'] == 0))]# &
                 #& (df['Nuclear shape'] == 1))]# &
                 #&(df['Nuclear Chromation'] == 1))] 
                 #&(df['Nucleous'] == 3))] 
                 #&(df['Cytoplasm'] == 1) )]
                 #&(df['Cytoplasmic basophilia'] == 1) )]
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 
                 #&(df['Cytoplasmic vacuoles'] == 2))]

print(filtered_df.head())
# Get the list of image names
image_list = filtered_df['Name'].tolist()

print("List of images where cell_type is 'Type1' and cell_size is 'Medium':")
#print(image_list)
filtered_df.to_excel('filtered_data.xlsx', index=False)
