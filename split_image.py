import os
import pandas as pd
from PIL import Image

# Function to split image and update Excel for a single image
def process_single_image(image_path, excel_path):
    # Load the image
    original_image = Image.open(image_path)

    # Image size
    image_width, image_height = original_image.size

    # Desired size for each split image
    split_width = 448
    split_height = 448

    # Overlap size
    overlap_size = 48

    # Calculate coordinates for the left split
    left_x1 = 0
    left_y1 = (image_height - split_height) // 2
    left_x2 = left_x1 + split_width
    left_y2 = left_y1 + split_height

    # Calculate coordinates for the right split
    right_x1 = image_width - split_width
    right_y1 = (image_height - split_height) // 2
    right_x2 = right_x1 + split_width
    right_y2 = right_y1 + split_height

    # Crop the left and right images
    left_image = original_image.crop((left_x1, left_y1, left_x2, left_y2))
    right_image = original_image.crop((right_x1, right_y1, right_x2, right_y2))

    # Save the cropped images
    left_image.save(f'output/{os.path.basename(image_path).split(".")[0]}_left.png')
    right_image.save(f'output/{os.path.basename(image_path).split(".")[0]}_right.png')

    # Load Excel sheet into DataFrame
    df = pd.read_excel(excel_path)

    # Add a new column 'patch_number'
    df['patch_number'] = 0

    # Update DataFrame with patch numbers for left and right patches
    df.loc[(df['X1_cord'] >= left_x1) & (df['X2_cord'] <= left_x2), 'patch_number'] = 1
    df.loc[(df['X1_cord'] >= right_x1) & (df['X2_cord'] <= right_x2), 'patch_number'] = 2

    # Update bounding box coordinates in the DataFrame
    df.loc[df['patch_number'] == 1, 'X1_cord'] -= left_x1
    df.loc[df['patch_number'] == 1, 'X2_cord'] -= left_x1
    df.loc[df['patch_number'] == 2, 'X1_cord'] -= right_x1
    df.loc[df['patch_number'] == 2, 'X2_cord'] -= right_x1

    # Save the updated Excel sheet
    updated_excel_path = f'output/{os.path.basename(excel_path)}'
    df.to_excel(updated_excel_path, index=False)

    return df

# Function to process all images in a folder and create a single Excel sheet
def process_all_images_and_create_single_excel(folder_path, output_excel_path):
    # Initialize an empty DataFrame to store the consolidated data
    consolidated_df = pd.DataFrame()

    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):  # Adjust file extensions as needed
            image_path = os.path.join(folder_path, filename)
            excel_path = os.path.join(folder_path, f"{filename.split('.')[0]}.xlsx")  # Assuming corresponding Excel file has the same name

            # Process a single image and append its DataFrame to the consolidated DataFrame
            single_image_df = process_single_image(image_path, excel_path)
            consolidated_df = consolidated_df.append(single_image_df, ignore_index=True)

    # Save the consolidated DataFrame to a single Excel file
    consolidated_df.to_excel(output_excel_path, index=False)

if __name__ == "__main__":
    folder_path = 'path/to/your/folder'
    output_excel_path = 'output/consolidated_data.xlsx'

    process_all_images_and_create_single_excel(folder_path, output_excel_path)
