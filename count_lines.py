import os

def count_jpg_files(directory):
    # Counter for jpg files
    jpg_count = 0

    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory {directory} does not exist.")
        return jpg_count

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        # Check for jpg file extension
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            jpg_count += 1

    return jpg_count

# Specify the directory to count jpg files in
directory_path = "C:/Users/Pc/Desktop/Project a/Workspace/images_jpg/detected_lines"

# Call the function and print the result
count = count_jpg_files(directory_path)
print(f"The directory '{directory_path}' contains {count} JPG files.")
