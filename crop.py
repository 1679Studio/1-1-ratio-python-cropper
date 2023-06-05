from PIL import Image, ExifTags
import os
import shutil

def crop_images_in_folder(folder_path, prefix, output_folder):
    cropped_files = []  # Store the paths of the cropped files
    original_files = []  # Store the paths of the original files

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")

            try:
                image = Image.open(file_path)

                # Rotate image based on EXIF orientation
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())

                if orientation in exif:
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)

                width, height = image.size

                # Calculate the dimensions for cropping
                if width > height:
                    new_width = height
                    new_height = height
                    left = (width - height) // 2
                    upper = 0
                else:
                    new_width = width
                    new_height = width
                    left = 0
                    upper = (height - width) // 2

                # Crop the image
                image = image.crop((left, upper, left + new_width, upper + new_height))

                # Save the cropped image with the prefixed filename in the output folder
                cropped_filename = f"{prefix}_{filename}"
                cropped_file_path = os.path.join(output_folder, cropped_filename)
                image.save(cropped_file_path)
                print(f"Cropped image saved: {cropped_file_path}")

                cropped_files.append(cropped_file_path)
                original_files.append(file_path)

            except Exception as e:
                print(f"Error processing file: {file_path}")
                print(f"Error details: {str(e)}")

        else:
            print(f"Skipping file: {filename} (unsupported format)")

    return cropped_files, original_files


# Example usage
folder_path = "./input"
prefix = input("Enter the file name prefix: ")
output_folder = input("Enter the output folder name: ")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Crop images in the input folder
cropped_files, original_files = crop_images_in_folder(folder_path, prefix, output_folder)

# Delete the original image files
for cropped_file_path, original_file_path in zip(cropped_files, original_files):
    os.remove(original_file_path)
    print(f"Original image deleted: {original_file_path}")

# Alternatively, if you want to delete the input folder itself, you can use the following line instead
# shutil.rmtree(folder_path)
