import os
import time
import subprocess
import shutil
# Folder paths
watch_folder = "camera_images"  # Replace with the folder where images are saved
uploaded_folder = os.path.join(watch_folder, "uploaded")
# Create the "uploaded" folder if it doesn't exist
if not os.path.exists(uploaded_folder):
    os.makedirs(uploaded_folder)
# URL for uploading images
upload_url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
def upload_image(image_path):
    """Upload an image using curl and return success status."""
    try:
        # Use curl to upload the image
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{image_path}", upload_url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Check for success (e.g., HTTP 200 or expected response)
        if result.returncode == 0 and "success" in result.stdout.lower():
            print(f"Uploaded successfully: {image_path}")
            return True
        else:
            print(f"Upload failed: {image_path}\n{result.stdout}\n{result.stderr}")
            return False
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")
        return False
def monitor_folder():
    """Monitor the folder for new images and upload them."""
    while True:
        # Get all files in the watch folder
        files = [f for f in os.listdir(watch_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        for file in files:
            file_path = os.path.join(watch_folder, file)
            # Attempt to upload the file
            if upload_image(file_path):
                # Move to the "uploaded" folder if successful
                shutil.move(file_path, os.path.join(uploaded_folder, file))
        # Wait 30 seconds before checking again
        time.sleep(30)
if __name__ == "__main__":
    print("Monitoring folder for new images...")
    monitor_folder()






