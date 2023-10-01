import os
import cv2
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import Listbox, ttk
from tkinter import filedialog


# Source directory where photos are stored
source_dir = '/Volumes/media1/Pictures/Photos/'
display_time_ms = 1

if not os.path.exists(source_dir):
    print("Path not found")

# Destination directory where organized photos will be stored
destination_dir = '/path/to/destination/directory'


def is_image_file(file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    return any(file_path.lower().endswith(ext) for ext in image_extensions)


def find_image_directories(root_directory):
    image_directories = []

    for root, dirs, _ in os.walk(root_directory):
        for dir_name in dirs:
            print(dir_name)
            dir_path = os.path.join(root, dir_name)
            # Check if the directory contains at least one image file
            if any(is_image_file(os.path.join(dir_path, filename)) for filename in os.listdir(dir_path)):
                image_directories.append(dir_path)

    return image_directories


def display_images(image_directories):

    cv2.namedWindow("Slideshow", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty( "Slideshow",cv2.WINDOW_AUTOSIZE)

    for dir_path in image_directories:
        print(dir_path)
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if is_image_file(file_path):
                img = cv2.imread(file_path)
                if img is not None:
                    cv2.imshow("Slideshow", img)
                    cv2.waitKey(display_time_ms)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 32 or key == 27:
            break

    cv2.destroyWindow("Slideshow")


def update_directory_list():
    root_source_dir = filedialog.askdirectory(title="Select Root Directory")
    if root_source_dir:
        image_directories = find_image_directories(root_source_dir)
        listbox.delete(0, tk.END)  # Clear the listbox
        for directory in image_directories:
            listbox.insert(tk.END, directory)

def resize_listbox(event)
    listbox.config(height=(event.height // 20), width=(event.width // 20))  # Adjust height and width as needed

# Create a Tkinter window to display the directory list
window = tk.Tk()
window.title("Image Directories")

# Create a button to trigger the directory selection
select_button = ttk.Button(
    window, text="Select Root Directory", command=update_directory_list)
select_button.pack()
# Create a listbox to display the directory paths
listbox = tk.Listbox(window)
listbox.pack(fill=tk.BOTH, expand = True)   #Allow listbox to expand

# Create a button to allow the user to show images from the selected path and subdirs
image_button = ttk.Button(window, text="Display Images",
                          command=lambda: display_images(listbox.get(0, tk.END)))
image_button.pack()

window.bind("<Configure>", resize_listbox)

window.mainloop()


# image_directories = find_image_directories(source_dir)


# if image_directories:
#     # Display images from the found directories
#     display_images(image_directories)
# else:
#     print("No directories with images found.")

# for root, _, files in os.walk(source_dir):
#     for file in files:
#         # Assuming photos have date information in the filename or metadata
#         file_path = os.path.join(root, file)
#         try:
#             # Extract the date from the file name or metadata
#             date_taken = datetime.strptime(date_from_filename_or_metadata, "%Y-%m-%d")
#         except Exception as e:
#             print(f"Error processing {file}: {e}")
#             continue

#         # Create a directory for the date if it doesn't exist
#         date_dir = os.path.join(destination_dir, date_taken.strftime("%Y-%m-%d"))
#         os.makedirs(date_dir, exist_ok=True)

#         # Copy the file to the destination directory with the new name
#         destination_file = os.path.join(date_dir, file)
#         shutil.copy2(file_path, destination_file)

print("Task completed.")
