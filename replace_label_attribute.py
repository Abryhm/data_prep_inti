import pandas as pd
import os
import numpy as np 
columns_to_replace = {
     'Cell Size': {0: 4, 1: 0, 2: 1, 3: 2},
    'Nuclear Chromation': {0: 4, 1: 0, 2: 1, 3: 2},
    'Nuclear shape': {0: 4, 1: 0, 2: 1, 3: 2},
    'Nucleous': {0: 4, 1: 0, 2: 1, 3: 2},
    'Cytoplasm': {0: 4, 1: 0, 2: 1, 3: 2},
    'Cytoplasmic basophilia': {0: 4, 1: 0, 2: 1, 3: 2},
    'Cytoplasmic vacuoles': {0: 4, 1: 0, 2: 1, 3: 2},
    'Cell_re_Size':{0: 4, 1: 0, 2: 1, 3: 2}
}
# Function to apply the mapping based on conditions
def map_cell_type(cell_type):
    if cell_type == "Myeloblast":
        return 1
    elif cell_type == "Lymphoblast":
        return 2
    elif cell_type == "Neutrophil":
        return 3
    elif cell_type == "Atypical lymphocyte":
        return 4
    elif cell_type == "Promonocyte":
        return 5
    elif cell_type == "Monoblast":
        return 6
    elif cell_type == "Monoblast ":
        return 6
    elif cell_type == "Lymphocyte":
        return 7
    elif cell_type == "Myelocyte":
        return 8
    elif cell_type == "Abnormal promyelocyte":
        return 9
    elif cell_type == "Monocyte":
        return 10
    elif cell_type == "Promyelocyte":
        return 11
    elif cell_type == "Metamyelocyte":
        return 12
    elif cell_type == "Eosinophil":
        return 13
    elif cell_type == "Basophil":
        return 14
    elif cell_type == "None":
        return 15
    else:
        return 0

# Function to capitalize the first letter of each value in the "Cell_type" column
def capitalize_first_letter(value):
    if isinstance(value, str):
        return value.capitalize()
    else:
        return value

# Folder containing your Excel files
folder_path = "1000_HCM_Microscope_data/Annotation_v6"
output_folder = "1000_HCM_Microscope_data/Annotation_v8"
os.makedirs(output_folder, exist_ok=True)

# Iterate through each Excel file in the folder
for filename in os.listdir(folder_path):
    print(filename)
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)
        file_path2 = os.path.join(output_folder, filename)

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        
        
        # Capitalize the first letter of each value in the "Cell_type" column
        df['Cell_type'] = df['Cell_type'].apply(capitalize_first_letter)

        # Map values in the "Cell_type" column based on conditions
        df['Leukemia Types'] = df['Cell_type'].apply(map_cell_type)

        # Replace values in specific columns
        for column, mapping in columns_to_replace.items():
            df[column].replace(mapping, inplace=True)

        # Save the modified DataFrame back to the new Excel file
        df.to_excel(file_path2, index=False)
