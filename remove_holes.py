import cv2
import os

def detect_and_remove_objects(input_directory, object_image_path, output_directory):
    # Load the object image
    object_image = cv2.imread(object_image_path, cv2.IMREAD_GRAYSCALE)

    if object_image is None:
        raise ValueError("Object image not found or could not be loaded.")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            # Construct the full path to the input image
            input_image_path = os.path.join(input_directory, filename)

            # Load the input image
            input_image = cv2.imread(input_image_path)

            if input_image is None:
                print(f"Skipping {filename}: Image not found or could not be loaded.")
                continue

            # Convert the input image to grayscale
            input_gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

            # Match the object image within the input image using template matching
            result = cv2.matchTemplate(input_gray, object_image, cv2.TM_CCOEFF_NORMED)

            # Find the location (top-left corner) of the best match
            _, _, _, max_loc = cv2.minMaxLoc(result)

            # Get the dimensions of the object image
            h, w = object_image.shape

            # Erase the detected object region (set it to white)
            input_image[max_loc[1]:max_loc[1]+h, max_loc[0]:max_loc[0]+w] = 255

            # Save the result image with the object removed to the output directory
            output_image_path = os.path.join(output_directory, filename)
            cv2.imwrite(output_image_path, input_image)

# Example usage:
input_directory = 'C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/splited_images'  # Replace with your input image directory
object_image_path = 'C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/circle2.PNG'  # Replace with the path to your object image
output_directory = 'C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/remove_holes'  # Replace with the path to your output directory

detect_and_remove_objects(input_directory, object_image_path, output_directory)
