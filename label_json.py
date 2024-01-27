import pandas as pd
import json

# Load your data from the Excel file
excel_file = "test/test_data.xlsx"  # Update with your file name
df = pd.read_excel(excel_file)

# Initialize COCO format dictionary
coco_data = {
    "images": [],
    "annotations": [],
    "categories": []  # You can add more categories if needed
}

# Create a mapping of image names to image IDs
image_id_mapping = {}
image_id = 1

# Create a mapping of annotation IDs
annotation_id = 1

# Iterate through the Excel data
for _, row in df.iterrows():
    image_name = row["Name"]

    # Check if the image name already has an associated image ID
    if image_name in image_id_mapping:
        image_id = image_id_mapping[image_name]
    else:
        # Create a new image ID and image information for the current image
        image_id = len(coco_data["images"]) + 1
        image_info = {
            "id": image_id,
            "file_name": image_name,  # Use the image name as the file name
            "width": 800,  # Set the image width
            "height": 448,  # Set the image height
        }
        coco_data["images"].append(image_info)
        image_id_mapping[image_name] = image_id

    # Create annotation information for the current cell within the same image name
    annotation_info = {
        "id": annotation_id,
        "image_id": image_id,
        "category_id": row["Leukemia Types"],  # Category ID for "Cell"
        "bbox": [row['X1_cord'], row['Y1_cord'], row['X2_cord'], row['Y2_cord']],  # Set the bounding box coordinates
        "area": (row['X2_cord'] - row['X1_cord']) * (row['Y2_cord'] - row['Y1_cord']),
        "iscrowd": 0,
        "attributes": {
            "Cell Size": row["Cell_re_Size"],
            "Nuclear Chromation": row["Nuclear Chromation"],
            "Nuclear shape": row["Nuclear shape"],
            "Nucleous": row["Nucleous"],
            "Cytoplasm": row["Cytoplasm"],
            "Cytoplasmic basophilia": row["Cytoplasmic basophilia"],
            "Cytoplasmic vacuoles": row["Cytoplasmic vacuoles"],
            #"Leukemia Types": row["Leukemia Types"],
            "Cell_type": row["Cell_type"]
        }
    }
    coco_data["annotations"].append(annotation_info)

    # Create category information for the current cell type
    category_info = {
        "id": row["Cell_type"],
        "name": f"Category_{row['Cell_type']}",
    }
    coco_data["categories"].append(category_info)

    # Increment annotation ID for the next cell
    annotation_id += 1

# Save the single JSON file in COCO dataset format
output_file_name = "test/test_data.json"
with open(output_file_name, "w") as output_file:
    json.dump(coco_data, output_file)

print("COCO JSON file with attributes for all image names has been created.")
