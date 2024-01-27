import cv2
import numpy as np

# Load the larger and smaller microscopy images
large_image = cv2.imread('BC/2/1000/2_1_1000_ALL.jpeg')
small_image = cv2.imread('bc_low/02/1000/02_1_1000_ALL.jpg')

# Convert images to grayscale
large_image_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
small_image_gray = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)

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

# Extract matched keypoints
src_pts = np.float32([keypoints_small[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([keypoints_large[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# Calculate the transformation matrix
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

# Get dimensions of the small image
h, w, _ = small_image.shape

# Warp the small image onto the large image
warped_small = cv2.warpPerspective(small_image, M, (large_image.shape[1], large_image.shape[0]))

# Create a mask for the small image region
mask = np.ones_like(large_image) * 255
cv2.warpPerspective(np.ones_like(small_image) * 255, M, (large_image.shape[1], large_image.shape[0]), dst=mask, flags=cv2.WARP_INVERSE_MAP)

# Combine the images using the mask
final_image = cv2.addWeighted(large_image, 1, warped_small, 0.5, 0, dtype=cv2.CV_8U)

# Display the final image
cv2_imshow(final_image)
cv2.imwrite('match.png', orignal_image1)
cv2.waitKey(0)
cv2.destroyAllWindows()