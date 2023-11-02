import cv2
import numpy as np
import os


def line_detect(image_path, kernel_size=(1, 125), height_range=(20, 60), width_threshold=10, save_output=False,
                output_dir=None, border_thickness=20):
    # Extract the base name without extension to use in saving lines
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if image is None:
        print(f"Error loading image {image_path}")
        return None

    # Preprocess: Apply Gaussian blur
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Threshold the image to binarize
    _, binarized = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Convert white borders of binarized image to black
    binarized[:, :border_thickness] = 0  # Left border
    binarized[:, -border_thickness:] = 0  # Right border

    # Use morphology to enhance the lines and reduce noise
    kernel = np.ones(kernel_size, np.uint8)
    morphed = cv2.morphologyEx(binarized, cv2.MORPH_CLOSE, kernel)
    erode_kernel = np.ones((1, 10), np.uint8)
    morphed = cv2.erode(morphed, erode_kernel, iterations=1)

    # Find connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(morphed, connectivity=8)

    # Prepare output directory
    if save_output and output_dir is not None and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    line_count = 0  # Counter to name the individual line images

    # Draw bounding boxes around lines and save them
    output_img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for i in range(1, num_labels):
        x, y, w, h, _ = stats[i]
        if height_range[0] <= h <= height_range[1] and w > width_threshold:
            x1, y1 = max(x - 10, 0), max(y - 5, 0)
            x2, y2 = min(x + w + 10, image.shape[1]), min(y + h + 7, image.shape[0])
            line_img = image[y1:y2, x1:x2]

            if line_img.size > 0:
                line_count += 1
                if save_output:
                    # Use the original image name and line count in the saved file name
                    line_filename = f"{name}_line_{line_count}.jpg"
                    cv2.imwrite(os.path.join(output_dir, line_filename), line_img)

            cv2.rectangle(output_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return output_img


def process_directory(input_dir, output_dir):
    # Check if input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist.")
        return

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each image in the directory
    for filename in os.listdir(input_dir):
        # Check for image formats here (e.g. jpg, png, etc.)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif')):
            image_path = os.path.join(input_dir, filename)
            print(f"Processing {filename}...")
            detected_img = line_detect(image_path, save_output=True, output_dir=output_dir)

            if detected_img is not None:
                # If needed, save or show the image with detected lines here
                pass


# Specify the input and output directories
input_dir = "C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/remove_holes"
output_dir = "C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/detected_lines"

# Process the directory
process_directory(input_dir, output_dir)
