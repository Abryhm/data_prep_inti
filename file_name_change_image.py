import os

folder_path = "26/1000"  # Replace with the path to your image folder

def rename_images(folder_path):
    for filename in os.listdir(folder_path):
        old_path = os.path.join(folder_path, filename)
        
        # Check if the file is a regular file and not a directory
        if os.path.isfile(old_path):
            # Replace "ALL" with "AML" in the file name
            new_filename = filename.replace("ALL", "APML")
            
            # Create the new path
            new_path = os.path.join(folder_path, new_filename)
            
            # Rename the file
            os.rename(old_path, new_path)
            
            print(f"Renamed: {filename} to {new_filename}")

# Call the function to rename images in the specified folder
rename_images(folder_path)