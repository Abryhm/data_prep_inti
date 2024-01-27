import os
import cv2
import pandas as pd
import math
import cv2
import numpy as np

# Function to calculate Euclidean distance
def euclidean_distance(x1, y1, x2, y2):
    return ((x2 - x1) + (y2 - y1))
# Enter slide name 
folder_name="100_HCM_Mobile_data"
lis=["3"]
for i in range (48):
   if i > 11: 
    i=i+1
 
    slide_number= str(i)
            #Enter small and large image required  folder 


            #large 400 and small 100 
            #large 1000 and small 400
    small_image= '1000'
    large_image= '100'



    large_folder= os.path.join(slide_number,large_image)
            #small_folder= os.path.join(slide_number,f"{small_image}_Cropped_folder")
    small_folder= os.path.join(slide_number,small_image)
    large_folder_image= os.listdir(large_folder)
    small_folder_image= os.listdir(small_folder)
    data = pd.read_excel( os.path.join(slide_number,'data.xlsx') ) # Replace with the actual file path
    data_bb = pd.read_excel( os.path.join('1000_HCM_Microscope_data/Annotation/',f'{slide_number}_data.xlsx') )# Replace with the actual file path
   

            # Filter out rows corresponding to '2_38_400_ALL'
    unique_slide_names = data['Slide Name'].unique()
    a=1
    k=0
    combined_data = pd.DataFrame()
    dfs = []
            # Iterate through the unique Slide Name values
    for small_slide_name in unique_slide_names:
                # Filter out rows corresponding to the current Slide Name
                small_image_res = small_slide_name.split("_")[2]
                if small_image_res== small_image:
                    #print(small_slide_name)
                    filtered_data = data[data['Slide Name'].str.contains(small_slide_name)]
                    
                    # Extract 'slide_x_axis' and 'slide_y_axis' values
                    x1 = filtered_data['slide_x_axis'].tolist()
                    y1 = filtered_data['slide_y_axis'].tolist()
                    slide_anme_small= filtered_data['Slide Name'].tolist()
                    #print(x1
                    score=0
                    b=0 
                
                    for large_slide_name in unique_slide_names:
                        # Filter out rows corresponding to the current Slide Name
                        large_image_res = large_slide_name.split("_")[2]
                        
                        if large_image_res == large_image:
                        
                            filtered_data_large = data[data['Slide Name'].str.contains(large_slide_name)]
                            
                            
                            # Extract 'slide_x_axis' and 'slide_y_axis' values
                            x2 = filtered_data_large['slide_x_axis'].tolist()
                            y2  = filtered_data_large['slide_y_axis'].tolist()
                            #print("hello")
                            slide_anme= filtered_data_large['Slide Name'].tolist()
                            
                            


                            e_distance = euclidean_distance(x1[0],y1[0],x2[0],y2[0])
                            if e_distance < 1 and e_distance > -1:
                                #print(large_folder_image)

                                large_image_match = cv2.imread(os.path.join(large_folder,"Mobile_"+slide_anme[0]+".png"))
                                large_image_match=cv2.rotate(large_image_match, cv2.ROTATE_90_CLOCKWISE)
                                small_image_match = cv2.imread(os.path.join(small_folder,slide_anme_small[0]+".png" ))
                                print(slide_anme[0])
                                print(slide_anme_small[0])

                                # Convert images to grayscale
                                large_image_gray = cv2.cvtColor(large_image_match, cv2.COLOR_BGR2GRAY)
                                small_image_gray = cv2.cvtColor(small_image_match, cv2.COLOR_BGR2GRAY)

                                # Create SIFT detector
                                sift = cv2.SIFT_create()
                            

                                # Find keypoints and descriptors in both grayscale images
                                keypoints_large, descriptors_large = sift.detectAndCompute(large_image_gray, None)
                                keypoints_small, descriptors_small = sift.detectAndCompute(small_image_gray, None)

                                # Create a Brute Force Matcher
                                bf = cv2.BFMatcher()

                                # Match descriptors
                                matches = bf.knnMatch(descriptors_small, descriptors_large, k=2)

                                # Apply ratio test
                                good_matches = []
                                for m, n in matches:
                                    if m.distance < 0.75 * n.distance:
                                        good_matches.append(m)

                                # Calculate the match area percentage
                                match_area_percentage = (len(good_matches) / len(keypoints_small)) * 100

                                #print(f"Match Area Percentage: {match_area_percentage}%")

                                # Save the final image only if the match area percentage is above a threshold
                                match_area_threshold = 2 # Adjust this threshold as needed
                                if match_area_percentage > match_area_threshold:
                                    # Get dimensions of the small image
                                    h, w, _ = small_image_match.shape
                                    #print(match_area_percentage)
                                    #kk

                                    # Calculate the transformation matrix
                                    src_pts = np.float32([keypoints_small[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                                    dst_pts = np.float32([keypoints_large[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
                                    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

                                

                                    # Warp the small image onto the large image
                                    warped_small = cv2.warpPerspective(small_image_match, M, (large_image_match.shape[1], large_image_match.shape[0]))

                                    # Get the coordinates of the matching keypoints in the small image
                                    h, w = small_image_match.shape[:2]
                                    pts = np.array([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]], dtype=np.float32).reshape(-1, 1, 2)

                                    # Transform the keypoints to the coordinates in the larger image
                                    dst_pts = cv2.perspectiveTransform(pts, M)

                                    # Convert the coordinates to integers
                                    dst_pts_int = np.int32(dst_pts)


                                    bb_slide = data_bb[data_bb['Name'].str.contains(small_slide_name)]
                                    
                                    
                                  
                                    coordinates = bb_slide[['X1_cord', 'Y1_cord', 'X2_cord', 'Y2_cord']].values
                                   
                                    coordinates = coordinates.reshape(-1, 1, 2).astype(np.float32)

                                    if (len(coordinates)!=0):
                                  

                                    # Transform the coordinates using the perspective transformation
                                        transformed_coordinates = cv2.perspectiveTransform(coordinates, M)
                                    

                                        # Reshape the transformed coordinates to match the original format
                                        transformed_coordinates = transformed_coordinates.reshape(-1,4)
                                    

                                        # Convert the transformed coordinates to integers
                                        transformed_coordinates_int = np.int32(transformed_coordinates)
                                        print(transformed_coordinates_int)
                                       
                                        x, y, w1, h1 = cv2.boundingRect(dst_pts_int)
                                        print(x, y, w1, h1)
                                        
                                        
                                    
                                        w1= 100
                                        h1= 64

                                        # Update the bb_slide DataFrame with the transformed coordinates
                                        bb_slide['X1_cord'] = transformed_coordinates_int[:, 0] - x
                                        bb_slide['Y1_cord'] = transformed_coordinates_int[:, 1] - y
                                        bb_slide['X2_cord'] = transformed_coordinates_int[:, 2] - x
                                        bb_slide['Y2_cord'] = transformed_coordinates_int[:, 3] - y 
                                        
                                                                    

                                    

                                        
                                        print(w1,h1)

                                    
                                        # Crop the region of interest from the larger image
                                        #cropped_image1 = large_image_match[y:y + h1, x:x + w1]
                                        new_iamge_resolution1= large_slide_name.split("_")[2]
                                        new_iamge_lukemi_type1= large_slide_name.split("_")[3]
                                        new_image_name1= slide_anme_small[0].split("_")[1]  
                                        bb_slide['Name'] = f"{slide_number}_{new_image_name1}_{new_iamge_resolution1}_{new_iamge_lukemi_type1}"
                                        dfs.append(bb_slide)
                                    # print("_____________________after________________________")
                                        print("after", x,y,w,h)
                                        #print(bb_slide)
                                        
                                        create_folder = f"mobile_1000_HCM"
                                        if not os.path.exists(os.path.join(folder_name,slide_number)):
                                            os.makedirs(os.path.join(folder_name,slide_number))
                                        
                                        if b==0:
                                            new_large_slide_name=large_slide_name
                                            b=b+1 
                                            #print(k)
                                            if k==10:
                                                
                                                cv2.imwrite(os.path.join(folder_name,slide_number,f"{slide_number}_{new_image_name}_{new_iamge_resolution}_{new_iamge_lukemi_type}.png"), cropped_image)
                                                print("image saved")
                                        

                                        if new_large_slide_name == large_slide_name and score < match_area_percentage:

                                            cropped_image = large_image_match[y:y + h1, x:x + w1]
                                            new_iamge_resolution= large_slide_name.split("_")[2]
                                            new_iamge_lukemi_type= large_slide_name.split("_")[3]
                                            new_image_name= slide_anme_small[0].split("_")[1]


                                            #print( slide_number,new_image_name,new_iamge_resolution, new_iamge_lukemi_type)
                                        


                                            k=10
                                            #print(k)

                                            

                                        # Save the cropped image
                                    
                                        


                                    

                                        #warped_small = cv2.warpPerspective(small_image_match, M, (large_image_match.shape[1], large_image_match.shape[0]))

                                        # Create a mask for the small image region
                                        #mask = np.ones_like(large_image_match) * 255
                                    #cv2.warpPerspective(np.ones_like(small_image_match) * 255, M, (large_image_match.shape[1],large_image_match.shape[0]), dst=mask, flags=cv2.WARP_INVERSE_MAP)

                                        # Combine the images using the mask
                                    # final_image = cv2.addWeighted(large_image_match, 1, warped_small, 0.5, 0, dtype=cv2.CV_8U)

                                        # Save the final image
                                        #create_folder= f"{small_image}_to_{large_image}_matching_MC"
                                    # if not os.path.exists(os.path.join(slide_number,create_folder)):
                                    #     os.makedirs(os.path.join(slide_number,create_folder))
                                        #cv2.imwrite(os.path.join(slide_number,create_folder,slide_anme_small[0]+"_"+slide_anme[0]+".png"), final_image)
                                    #else:
                                    # print("No good match found. Image not saved.")
    cv2.imwrite(os.path.join(folder_name,slide_number,f"{slide_number}_{new_image_name}_{new_iamge_resolution}_{new_iamge_lukemi_type}.png"), cropped_image)
    print("image saved")                                # print("No good match found. Image not saved.")
    combined_data = pd.concat(dfs, ignore_index=True)
    output_filename = f'{folder_name}/Annotation/{slide_number}_data.xlsx'  # Change the filename as needed
    combined_data.to_excel(output_filename, index=False)
    print("file save")
                                                        
                                                    


                                        
                                        # Print the extracted values
                                        

                                    #for image in small_folder_image:
                                        #parts = image.split('_')
                                        #image_name_excel= '_'.join(parts[1:5])
                                    # print(image_name_excel)
                                    #Slide Name	Patch Number	Medical Record #	Flow Cytometry	Image Size	Leukemia Type	slide_x_axis	slide_y_axis
