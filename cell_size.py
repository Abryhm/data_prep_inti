import pandas as pd
import os

# Function to apply the condition to the "Cell Size" column
def apply_condition(cell_size, n, o, l, m):
    if cell_size != 0:
        if ((n - l) < 55 and (o - m) < 65 and (n - l) * (o - m) < 3600) or \
           ((o - m) < 55 and (n - l) < 65 and (n - l) * (o - m) < 3600):
            return 1
        elif ((n - l) > 90 and (o - m) > 70 and (n - l) * (o - m) > 8000) or \
             ((o - m) > 90 and (n - l) > 70 and (n - l) * (o - m) > 8000):
            return 3
        else:
            return 2
    else:
        return 0

# Folder containing your Excel files
folder_path = "replaced_sheets/"
output_folder= "1000_HCM_Microscope_data/Annotation_v6"
os.makedirs(output_folder, exist_ok=True)

# Iterate through each Excel file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        # Apply the condition to the "Cell Size" column and create a new column "Result"
        original_cell_type = df['Cell_type'].copy()

        # Apply the condition to the "Cell Size" column and create a new column "Result"
        df['Cell_re_Size'] = df.apply(lambda row: apply_condition(row['Cell Size'], row['X2_cord'], row['Y2_cord'], row['X1_cord'], row['Y1_cord']), axis=1)

        # Restore the original "Cell_type" values
        df['Cell_type'] = original_cell_type

        # Save the modified DataFrame back to the Excel file
        save_path=f"{output_folder}/{filename}"
        print(save_path)
        df.to_excel(save_path, index=False)
