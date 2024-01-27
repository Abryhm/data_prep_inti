import cv2
import numpy as np
import os 

# Load the circular image
selected_folder_path = "2/1000_Cropped_folder/"
target_folder = os.listdir(selected_folder_path)

for i in target_folder:
    mobile_i = i.split("_")[0]
    if mobile_i == "Mobile":
        parts = i.split(',')[-1]
        parts_0 = i.split(',')[0]
        print(parts_0)
        new_part_0 = parts_0.replace('ALL', '400')

        new_part = parts.replace('400_', 'ALL_')
        new_name = f"{new_part_0}_{new_part}"
        
        old_path = os.path.join(selected_folder_path, i)
        new_path = os.path.join(selected_folder_path, new_name)
        
        #os.rename(old_path, new_path)
        print(f"Renamed: {i} -> {new_name}")