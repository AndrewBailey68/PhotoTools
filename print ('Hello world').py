import os
import cv2  
import shutil
from datetime import datetime

# Source directory where photos are stored
source_dir = 'afp://ULTRA6 (AFP)._afpovertcp._tcp.local/media1/Pictures/100GOPRO'

# Destination directory where organized photos will be stored
destination_dir = '/path/to/destination/directory'

image_files = [os.path.join (source_dir, file) for file in os.listdir(source_dir) if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

image_files(sort)

cv2.namedWindow("Slideshow", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Slideshow", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

display_time_ms = 300

for image_file in image_files
    img = cv.imread(image_file)
    if img is not None:
        cv2.imshow("Slideshow", img)
        cv2.waitKey(display_time_ms)
        
while True:
    key = cv2.waitkey(0)
    if key == 32:
        break

cv2.destroyWindow("Slideshow")


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
