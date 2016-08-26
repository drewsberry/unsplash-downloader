import requests
import shutil
import os
import hashlib
from datetime import datetime


UNSPLASH_URL = "https://unsplash.it"
WIDTH = 3840
HEIGHT = 2160
IMAGE_DIR = "D:/pictures/unsplash/"
NUM_IMAGES = 1000
SHOULD_TRIM_DUPLICATES = False


def get_unplash_picture(target_dir, width, height, image_hashes):
    url = UNSPLASH_URL + "/" + str(width) + "/" + str(height) + "?random"
    response = requests.get(url, stream=True)

    fname = datetime.utcnow().isoformat().replace(":", "-")

    if response.status_code == 200:
        new_filename = target_dir + "/" + fname + ".jpg"
        with open(new_filename, "wb") as pictureFile:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, pictureFile)

        new_image_hash = hash_file(new_filename)
        if new_image_hash in image_hashes:
            print("Successfully downloaded duplicate Unsplash image.")
            os.remove(new_filename)
            image_hashes.append(new_image_hash)
            return True
        else:
            print("Successfully saved unique Unsplash image", fname,
                  "to", target_dir + ".")

    else:
        print("Failed to download Unplash image from", url)

    return False


def hash_file(filename):
    md5 = hashlib.md5()

    with open(filename, "rb") as f:
        md5.update(f.read())

    return md5.digest()


def get_file_hashes(target_dir):
    print("Generating file hashes for folder", target_dir + "...")
    file_hashes = []

    for filename in os.listdir(target_dir):
        full_filename = target_dir + filename

        file_hashes.append(hash_file(full_filename))

    print("Successfully generated", len(file_hashes),
          "file hashes from", target_dir + ".")
    return file_hashes


def trim_duplicates(target_dir):
    print("Trimming duplicate files in", target_dir, "...")
    file_hashes = []

    for filename in os.listdir(target_dir):
        full_filename = target_dir + filename

        file_hash = hash_file(full_filename)

        if file_hash in file_hashes:
            print("File", filename, "is already present; deleting...")
            os.remove(full_filename)
        else:
            print("File", filename, "is unique; continuing...")
            file_hashes.append(file_hash)

    print("Successfully trimmed diplicate files in", target_dir + ".")


def main():
    image_hashes = get_file_hashes(IMAGE_DIR)

    if SHOULD_TRIM_DUPLICATES:
        trim_duplicates(IMAGE_DIR)

    print("Downloading", NUM_IMAGES, "images from Unsplash...")

    num_images_downloaded = 0
    while (num_images_downloaded < NUM_IMAGES):
        if get_unplash_picture(IMAGE_DIR, WIDTH, HEIGHT, image_hashes):
            num_images_downloaded += 1

    print("Successfully downloaded", NUM_IMAGES,
          "unique images from Unsplash.")

if __name__ == "__main__":
    main()
