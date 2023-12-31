import os
import cv2
import rawpy
import exifread
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import Listbox, ttk
from tkinter import filedialog


# Source directory where photos are stored
source_dir = '/Volumes/media1/Pictures/Photos/'
display_time_ms = 1
directory_paths = [source_dir]

if not os.path.exists(source_dir):
    print("Path not found")

# Destination directory where organized photos will be stored
destination_dir = '/path/to/destination/directory'

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.cr2', '.raw']
cv2_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
raw_extensions = ['.cr2', '.raw']


def is_image_file(file_path):
    return any(file_path.lower().endswith(ext) for ext in image_extensions)
# ===============================================

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
# ===============================================

def update_directory_list():
    root_source_dir = filedialog.askdirectory(title="Select Root Directory")
    if root_source_dir:
        image_directories = find_image_directories(root_source_dir)
        # Global variable to store all the directories we have images in

        listbox.delete(0, tk.END)  # Clear the listbox
        for directory in image_directories:
            listbox.insert(tk.END, directory)
            directory_paths.append(directory)
# ===============================================

# Function to resize the listbox if the window size changes
def resize_listbox(event):
    # Adjust height and width as needed
    listbox.config(height=(event.height // 20), width=(event.width // 20))
# ===============================================
# Function to display images from the selected directory

def display_selected_directory():
    # index needs adjusting up by the base of the list isn't the same as the array
    indexadjustment = 1
    # Get the selected directory path
    selected_index = listbox.curselection()
    print(selected_index)
    if selected_index:
        index = int(selected_index[0])  # Get the selected index
        if 0 <= index < len(directory_paths):
            # Get the corresponding directory path
            selected_directory = directory_paths[index + + indexadjustment]
            display_images(selected_directory)
# ===============================================

# Function to read Exif data from an image file
def read_exif_data(image_path):
    exif_data = ""
    with open(image_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                exif_data += f'{tag}: {tags[tag]}\n'
    return exif_data
# ===============================================

# Function to display images and Exif data
def display_image_with_exif(image_path):
    # Create a Tkinter window
    exif_window = tk.Toplevel()
    exif_window.title("Image with Exif Data")

    # Load the image
    img = cv2.imread(image_path)
    cv2.imshow("Image", img)

    # Read and display Exif data
    exif_data = read_exif_data(image_path)
    exif_text = tk.Text(exif_window, wrap=tk.WORD)
    exif_text.insert(tk.END, exif_data)
    exif_text.pack(fill=tk.BOTH, expand=True)
# ===============================================


# Function to walk through the directories and display the contents
def display_images(image_directories):
    #cv2.namedWindow("Slideshow", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty( "Slideshow",cv2.WINDOW_AUTOSIZE)
    for filename in os.listdir(image_directories):
        file_path = os.path.join(image_directories, filename)
        if any(file_path.lower().endswith(ext) for ext in cv2_extensions):
            if is_image_file(file_path):
                display_image_with_exif (file_path)
                
                # img = cv2.imread(file_path)
                # if img is not None:
                #     cv2.imshow("Slideshow", img)
                #     cv2.waitKey(display_time_ms)
                #     key = cv2.waitKey(1) & 0xFF
                #     if key == 32 or key == 27:
                #         break
        # elif any(file_path.lower().endswith(ext) for ext in raw_extensions):
        #     with rawpy.imread(file_path) as raw:
        #         rgb = raw.postprocess()  # a numpy RGB array
        #         image = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        #         cv2.imshow("Slideshow", image)
        #         cv2.waitKey(display_time_ms)
        #         key = cv2.waitKey(1) & 0xFF
        #         if key == 32 or key == 27:
        #             break

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 32 or key == 27:
            break

    cv2.destroyWindow("Slideshow")
# ===============================================


# Create a Tkinter window to display the directory list
window = tk.Tk()
window.title("Image Directories")

# Create a button to trigger the directory selection
select_button = ttk.Button(
    window, text="Select Root Directory", command=update_directory_list)
select_button.pack()
# Create a button to allow the user to show images from the selected path and subdirs
image_button = ttk.Button(window, text="Display Images",
                          command=display_selected_directory)
image_button.pack()
# Create a listbox to display the directory paths
listbox = tk.Listbox(window)
listbox.pack(fill=tk.BOTH, expand=True)  # Allow listbox to expand


window.bind("<Configure>", resize_listbox)

window.mainloop()


print("Task completed.")
