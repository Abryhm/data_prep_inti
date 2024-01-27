import pandas as pd
import os

# Set the path to the folder containing your Excel files
folder_path = 'test/'

# Get a list of all Excel files in the folder
excel_files = [file for file in os.listdir(folder_path) if file.endswith('.xlsx')]

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through each Excel file and append its data to the merged_data DataFrame
for file in excel_files:
    #print(file)
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path)
    #print(df)
    merged_data = merged_data.append(df, ignore_index=True)

# Save the merged data to a new Excel file
output_file_path = 'test/test_data.xlsx'
merged_data.to_excel(output_file_path, index=False)

print(f'Merged data saved to {output_file_path}')