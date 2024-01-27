import cv2
import pandas as pd
import os

# Function to draw multiple bounding boxes on an image
def draw_bboxes(image, bboxes):
    cell_type_colors = {
          # Default color
        1: (255, 0, 0),  # Red
        2: (0, 255, 0),  # Green
        3: (0, 0, 255),  # Blue
        4: (255, 255, 0),  # Yellow
        5: (255, 0, 255),  # Magenta
        6: (0, 255, 255),  # Cyan
        7: (128, 0, 128),  # Purple
        8: (128, 128, 0),  # Olive
        9: (0, 128, 128),  # Teal
        10: (0, 102, 204),
        11: (102, 102, 204),# light blue
        12: (255, 165, 0),  # Orange
        13: (255, 20, 147),  # Deep Pink
        14: (0, 0, 128),
        15: (0,0,0),
        16: (100,100,100)# Navy
        # Add more colors as needed
    }

    for bbox in bboxes:
        x1, y1, x2, y2,Cell_type= bbox
        color = cell_type_colors.get(Cell_type, (255, 255, 255))  # Default to white if cell type is not found in the color map
        cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 255, 255), 2)
        # Add text with cell type
        class_labels = ["Myeloblast", "Lymphoblast", "Neutrophil", "Atypical lymphocyte", "Promonocyte",
                "Monoblast", "Lymphocyte", "Myelocyte", "Abnormal promyelocyte", "Monocyte",
                "Promyelocyte", "Metamyelocyte", "Eosinophil", "Basophil", "None", "Not_predicted"]

        # Assuming Cell_type ranges from 1 to 15
        cell_type_index = Cell_type - 1  # Adjust to 0-based index
        cell_type_label = class_labels[cell_type_index]

        # Use the label in cv2.putText
        cv2.putText(image, cell_type_label, (int(x1 + 5), int(y2 - 15)),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255),2 )
        #cv2.putText(image, str(cell_size), (int(x1+((x2 - x1) / 2)), int(y1+((y2 - y1) / 2)+10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

 
# Load the Excel sheet with bounding box information
# Specify the range of folders from 1 to 48

excel_file = f"prediction_Blood Cancer_test.xlsx"
    #excel_file = f"Annotation/replaced_sheets/{image_folder}_data.xlsx"
df = pd.read_excel(excel_file)
    # Folder containing the images


    # Output folder for images with bounding boxes
output_folder = f"1000_HCM_Microscope_data/v8_bb_2/test_bb_size_pred/"

    # Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

    # Initialize variables to keep track of the current image and its bounding boxes
current_image = None
current_bboxes = []

    # Loop through the rows in the Excel sheet
for index, row in df.iterrows():
        # Get the image filename and bounding box coordinates from the Excel sheet
        file_name = row['Image']
        folder_path = file_name.split("_")[0]
        image_filename = f"Image/{folder_path}/{file_name}.png"
        
        #bbox = [row['X1_cord'], row['Y1_cord'], row['X2_cord'], row['Y2_cord']]
        bbox = [row['Box_x1'], row['Box_y1'], row['Box_x2'], row['Box_y2'],row['Label']]
        # Check if the image has changed
        if current_image != image_filename:
            # If a new image is encountered, draw the accumulated bounding boxes on the previous image (if any)
            if current_image is not None:
                #print(current_image)
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
