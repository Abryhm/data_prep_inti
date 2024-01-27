import cv2
import pandas as pd
import os

# Function to draw multiple bounding boxes on an image
def draw_bboxes(image, bboxes):
    for bbox in bboxes:
        x1, y1, x2, y2 = map(int, bbox)
        cv2.rectangle(image, (2*x1, 2*y1), (2*x2, 2*y2), (0, 255, 0), 2)

# Load the Excel sheet with bounding box information
image_folder = 'data/val'
excel_file = "data/prediction_Blood Cancer_99.xlsx"
df = pd.read_excel(excel_file)

# Folder containing the images


# Output folder for images with bounding boxes
output_folder = f"data/bb_display/val_bbox/"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Initialize variables to keep track of the current image and its bounding boxes
current_image = None
current_bboxes = []

# Loop through the rows in the Excel sheet
for index, row in df.iterrows():
    # Get the image filename and bounding box coordinates from the Excel sheet
    #image_filename =f"{image_folder}/{row['Name']}.png"
    #bbox = [row['X1_cord'], row['Y1_cord'], row['X2_cord'], row['Y2_cord']]
    image_filename =f"{image_folder}/{row['Image']}.png"
    bbox = [row['Box_x1'], row['Box_y1'], row['Box_x2'], row['Box_y2']]
    #bbox=bbox*2

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
    current_bboxes.append(bbox)350	169	398	210
239	20	267	48
234	11	270	56
238	23	251	49
100	55	133	80


# Draw and save bounding boxes for the last image (if any)
if current_image is not None:
    image = cv2.imread(current_image)
    draw_bboxes(image, current_bboxes)
    output_filename = os.path.join(output_folder, os.path.basename(current_image))
    cv2.imwrite(output_filename, image)

print(f"Bounding boxes added to {len(df)} images. Images with bounding boxes saved in {output_folder}")
