import cv2
import pandas as pd
import os

# Function to draw multiple bounding boxes on an image
def draw_bboxes(image, bboxes):
    cell_type_colors = {
        "None": (0,0,0),  # Default color
        "Myeloblast": (255, 0, 0),  # Red
        "Lymphoblast": (0, 255, 0),  # Green
        "Neutrophil": (0, 0, 255),  # Blue
        "Atypical lymphocyte": (255, 255, 0),  # Yellow
        "Promonocyte": (255, 0, 255),  # Magenta
        "Monoblast": (0, 255, 255),  # Cyan
        "Lymphocyte": (128, 0, 128),  # Purple
        "Myelocyte": (128, 128, 0),  # Olive
        "Abnormal promyelocyte": (0, 128, 128),  # Teal
        "Monocyte": (0, 102, 204),  # light blue
        "Metamyelocyte": (255, 165, 0),  # Orange
        "Eosinophil": (255, 20, 147),  # Deep Pink
        "Basophil": (0, 0, 128)  # Navy
        # Add more colors as needed
    }

    for bbox in bboxes:
        x1, y1, x2, y2,Cell_type= bbox
        color = cell_type_colors.get(Cell_type, (255, 255, 255))  # Default to white if cell type is not found in the color map
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        # Add text with cell type
        cv2.putText(image, str(Cell_type), (int(x1 + 5), int(y2 - 15)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color,2 )
        #cv2.putText(image, str(cell_size), (int(x1+((x2 - x1) / 2)), int(y1+((y2 - y1) / 2)+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

 
# Load the Excel sheet with bounding box information
# Specify the range of folders from 1 to 48
image_folder_list = list(map(str, range(2, 48)))
#image_folder_list = ['1']
for image_folder in image_folder_list:
    excel_file = f"prediction_Blood Cancer_test.xlsx"
    #excel_file = f"Annotation/replaced_sheets/{image_folder}_data.xlsx"
    df = pd.read_excel(excel_file)
    df['Cell_type'] = df['Cell_type']#.str.capitalize()
    # Folder containing the images


    # Output folder for images with bounding boxes
    output_folder = f"1000_HCM_Microscope_data/v8_bb_2/{image_folder}_test_bb_size/"

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Initialize variables to keep track of the current image and its bounding boxes
    current_image = None
    current_bboxes = []

    # Loop through the rows in the Excel sheet
    for index, row in df.iterrows():
        # Get the image filename and bounding box coordinates from the Excel sheet
        image_filename = os.path.join('Image/',image_folder, row['Name'] + ".png")
        #bbox = [row['X1_cord'], row['Y1_cord'], row['X2_cord'], row['Y2_cord']]
        bbox = [row['X1_cord'], row['Y1_cord'], row['X2_cord'], row['Y2_cord'],row['Cell_type']]
        # Check if the image has changed
        if current_image != image_filename:
            # If a new image is encountered, draw the accumulated bounding boxes on the previous image (if any)
            if current_image is not None:
                image = cv2.imread(current_image)
                draw_bboxes(image, current_bboxes)
                # Save the image with the accumulated bounding boxes
                output_filename = os.path.join(output_folder, os.path.basename(current_image))
                cv2.imwrite(output_filename, image)
            
            # Reset variables for the new image
            current_image = image_filename
            current_bboxes = []

        # Accumulate the bounding boxes for the current image
        current_bboxes.append(bbox)

    # Draw and save bounding boxes for the last image (if any)
    if current_image is not None:
        image = cv2.imread(current_image)
        draw_bboxes(image, current_bboxes)
        output_filename = os.path.join(output_folder, os.path.basename(current_image))
        cv2.imwrite(output_filename, image)

    print(f"Bounding boxes added to {len(df)} images. Images with bounding boxes saved in {output_folder}")
