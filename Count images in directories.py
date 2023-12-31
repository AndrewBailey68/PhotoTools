# - Walk through directories
# - identify images
# - count images by type
# -
#
#
#
#

import os
import csv
import cv2
import shutil
import exifread
from datetime import datetime
import tkinter as tk
from tkinter import Listbox, ttk
from tkinter import filedialog
import threading
from multiprocessing.dummy import Pool as ThreadPool
import queue


# Source directory where photos are stored
source_dir = '/Volumes/media1/Pictures/Photos/'
if not os.path.exists(source_dir):
    print("Path not found")

# Destination directory where organized photos will be stored
destination_dir = '/path/to/destination/directory'

display_time_ms = 1
directory_paths = queue.Queue()  # global to contain temp list
image_number = 0
image_data_cache = []
image_directory_list = []  # list to hold directories with images

image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.cr2', '.raw']
cv2_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
raw_extensions = ['.cr2', '.raw']
# ===============================================
# Preprocess the image extensions to lowercase and convert them into a set for faster membership checking
image_extensions_set = {ext.lower() for ext in image_extensions}
cv2_extensions_set = {ext.lower() for ext in cv2_extensions}
raw_extension_set = {ext.lower() for ext in raw_extensions}

# Threads limited to 3
pool = ThreadPool(3)  # not used


# Function to add image data to the cache
def cache_image_data(filename, path, image_size, image_type):
    image_data_cache.append({'filename': filename, 'path': path,
                            'image_size': image_size, 'image_type': image_type})
# ===============================================

# Function to save cached image data to a CSV file


def save_cached_data_to_csv():
    with open('image_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Path', 'Image Size', 'Image Type'])
        for item in image_data_cache:
            csv_writer.writerow(
                [item['filename'], item['path'], item['image_size'], item['image_type']])
# ===============================================

# Function to load image data from the CSV file into the cache


def load_data_to_cache():
    try:
        with open('image_data.csv', 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                cache_image_data(row['Filename'], row['Path'],
                                 row['Image Size'], row['Image Type'])
    except FileNotFoundError:
        pass  # Handle the case where the CSV file doesn't exist
# ===============================================

# Function to count directories recursively
# Designed to be threaded - puts output into a global variable
# could be improved by taking the global variable in function call
# and using that here to make explicit the function's use of a global


def count_directories(root_directory):
    print("f (count directories)")
    count = 0
    for _, dirs, _ in os.walk(root_directory):
        count += len(dirs)
        for dir_name in dirs:
            dir_path = os.path.join(root_directory, dir_name)
            directory_paths.put(dir_path)
            print(f'd+ {dir_path}')
    return count
# ===============================================


def is_image_file(file_path):
    # Extract the file extension and convert it to lowercase
    file_extension = os.path.splitext(file_path)[1].lower()
    # Check if the lowercase file extension is in the set of image extensions
    return file_extension in image_extensions_set
# ===============================================


def count_image_files(directory):
    image_count = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if is_image_file(file_path):
            image_count += 1
            image_size = os.path.getsize(file_path)
            cache_image_data(filename, directory, image_size,
                             os.path.splitext(filename)[1].lower())
    return image_count
# ===============================================


def isValInLst(val, lst):
    return bool([index for index, content in enumerate(lst) if val in content])
# ===============================================

# designed to be threaded
# takes the files in a directory and determines whether they are images or not
# if they are - add to image list
# if there are images - add dir to image_directory_list


def find_images(temp_dir):
    """
    Find and cache image details from the specified directory.
    
    Parameters:
    - temp_dir (str): The directory path to search for images.
    """
    print(f'+Image thread started {temp_dir}')
    
    if os.path.exists(temp_dir):
        image_flag = False
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            if os.path.isfile(file_path) and file_path.lower().endswith(tuple(image_extensions)):
                image_data_cache.append({'filename': filename, 'path': temp_dir})
                image_flag = True 
                
        if image_flag:
            image_directory_list.append(temp_dir)
            
    print(f' - Image thread ended {temp_dir}')
    return
# ===============================================


def update_directory_list():
    root_source_dir = filedialog.askdirectory(title="Select Root Directory")
    if root_source_dir:
        # Start the dir tree search thread
        result = count_directories(root_source_dir)
        print(f'dir count {result}')

# Scan thread is running
# Now take the contents of the current list and copy to a new list
    print(f'dir path queue size ', directory_paths.qsize())
    while directory_paths.not_empty:
        print(
            f'not empty {directory_paths.not_empty} {directory_paths.qsize()}')
        temp_dir = directory_paths.get()
        print(f'got path {temp_dir}')
        print(f'queue size now f{directory_paths.qsize()}')
        try:
            print(f'Attempting thread start {temp_dir}')
            x = threading.Thread(target=find_images,
                                 args=(temp_dir))
            x.start()
        except RuntimeError:  # a RuntimeError
            print(f'error thread start {temp_dir}')
            break


#         image_directories_tuple = []

#         # Global variable to store all the directories we have images in
#         listbox.delete(0, tk.END)  # Clear the listbox
#         for directory_tuple in image_directories_tuple:
#             directory, image_count = directory_tuple
#             listbox.insert(tk.END, f"{directory} ({image_count} images")
#             directory_paths.append(directory)
# # ===============================================

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
    # cv2.namedWindow("Slideshow", cv2.WINDOW_NORMAL)
    # cv2.setWindowProperty( "Slideshow",cv2.WINDOW_AUTOSIZE)
    for filename in os.listdir(image_directories):
        file_path = os.path.join(image_directories, filename)
        if any(file_path.lower().endswith(ext) for ext in cv2_extensions):
            if is_image_file(file_path):
                display_image_with_exif(file_path)

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
