import cv2
import numpy as np
import os

# Input and output directories
input_directory = "C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/remove_holes"
output_directory = "C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/isolating_res"

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Get all the files in the input directory
image_files = [f for f in os.listdir(input_directory) if f.endswith(".jpg")]

# Process each image
for image_file in image_files:
    # Load the image
    image_path = os.path.join(input_directory, image_file)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to binarize
    _, binarized = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours in the binarized image
    contours, _ = cv2.findContours(binarized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask of the same size as the original image, filled with 255 (white)
    mask = np.ones_like(image) * 255

    # Fill detected contours with 0 (black) in the mask
    for contour in contours:
        cv2.drawContours(mask, [contour], -1, 0, -1)

    # Apply the mask to the original image
    isolated_background = cv2.bitwise_or(image, mask)

    # Save the result
    output_path = os.path.join(output_directory, image_file)
    cv2.imwrite(output_path, isolated_background)

print("Processing completed!")
