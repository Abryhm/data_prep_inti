import cv2
import numpy as np

# Load the circular image
image_path = "4/Mobile_4_55_1000_ALL.png"
gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
orignal_image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
orignal_image1 = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
ret, binary_image = cv2.threshold(gray_image, 30, 255, 0)
binary_image= np.where(binary_image > 0, 1 , binary_image)
#binary_image[binary_image > 0] = 1

row_threshold = np.sum(binary_image[int(binary_image.shape[0]/2)])
col_threshold = np.sum(binary_image[:, int(binary_image.shape[1]/2)])

# Initialize variables for bounding box
x_start, y_start, x_end, y_end = 0, 0, binary_image.shape[1], binary_image.shape[0]
while True:

        first_column_sum = np.sum(binary_image[:, 0])
        last_column_sum = np.sum(binary_image[:, -1])
        first_row_sum = np.sum(binary_image[0, :])
        #print(first_row_sum2 )
        if first_column_sum < first_row_sum :

            binary_image = binary_image[:, 1:]
            orignal_image = orignal_image[:, 1:, :]
            x_start += 1
        #last_column_sum = np.sum(binary_image[:, -1])
        if last_column_sum < first_row_sum :
            #print(last_column_sum)
            #print(col_threshold )
            binary_image = binary_image[:, :-1]
            orignal_image = orignal_image[:, :-1, :]
            x_end -= 1
        row_threshold = np.sum(binary_image[int(binary_image.shape[0]/2)])
        col_threshold = np.sum(binary_image[:, int(binary_image.shape[1]/2)])
        ab = np.sum(binary_image[:, 0])
        cd = np.sum(binary_image[0])

        #if binary_image.shape[0] >= binary_image.shape[1]:
            #break
        if  last_column_sum >= first_row_sum and first_column_sum >= first_row_sum:
            break

while True:




    #print("i am on")
    previous_binary_image = binary_image.copy()
    row_size, column_size = binary_image.shape

    first_column_sum = np.sum(binary_image[:, 0])
    if first_column_sum < col_threshold:
        binary_image = binary_image[:, 1:]
        orignal_image = orignal_image[:, 1:, :]
        x_start += 1

    last_column_sum = np.sum(binary_image[:, -1])
    if first_column_sum < col_threshold:
        binary_image = binary_image[:, :-1]
        orignal_image = orignal_image[:, :-1, :]
        x_end -= 1

    first_row_sum = np.sum(binary_image[0, :])
    if first_row_sum < row_threshold:
        binary_image = binary_image[1:, :]
        orignal_image = orignal_image[1:, :, :]
        y_start += 1

    last_row_sum = np.sum(binary_image[-1, :])
    if first_row_sum < row_threshold:
        binary_image = binary_image[:-1, :]
        orignal_image = orignal_image[:-1, :, :]
        y_end -= 1

    row_threshold = np.sum(binary_image[int(binary_image.shape[0]/2)])
    col_threshold = np.sum(binary_image[:, int(binary_image.shape[1]/2)])
    if np.array_equal(binary_image, previous_binary_image):
        break
# Draw bounding box on the original image
cv2.rectangle(orignal_image1, (x_start, y_start), (x_end, y_end), (255, 0, 0), 2)
#cv2_imshow(orignal_image1)
cv2.imwrite("4/1000_annotated_folder/Mobile_4_55_1000_ALL.png", orignal_image1)
cv2.imwrite("4/1000_Cropped_folder/Mobile_4_55_1000_ALL.png", orignal_image)
print("Done")
# Display or save the image with bounding box
