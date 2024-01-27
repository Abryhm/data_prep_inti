import pandas as pd

i = image_folder_list_Complete = list(map(str, range(19, 47)))
i=["48"]
for image_folder in i:
# Read the Excel sheets into pandas DataFrames
    sheet1 = pd.read_excel(f'Annotation/{image_folder}_data.xlsx')  # Replace 'path_to_sheet1.xlsx' with the actual path
    sheet2 = pd.read_excel(f'error_eanotation/{image_folder}_bb_size_data.xlsx')  # Replace 'path_to_sheet2.xlsx' with the actual path
    sheet2.reset_index(inplace=True)

    # Set 'Name' and 'Cell_number' as the index for both DataFrames
    #print(sheet1)
    sheet1.set_index(['Name', 'Cell_number'], inplace=True)
    sheet2.set_index(['Name', 'Cell_type'], inplace=True)
    
    #print(sheet2)

    # Columns to update
    columns_to_update = ['X1_cord', 'Y1_cord', 'X2_cord', 'Y2_cord']

    # Update the values in Sheet1 with corresponding values from Sheet2 only for the specified columns
    for col in columns_to_update:
       # print(sheet2[col])
        sheet1[col] = sheet2[col].combine_first(sheet1[col])

    # Reset the index to have 'Name' and 'Cell_number' as regular columns
    sheet1.reset_index(inplace=True)

    # Save the updated DataFrame to a new Excel file or overwrite the existing one
    sheet1.to_excel(f'replaced_sheets/{image_folder}_data.xlsx', index=False)
