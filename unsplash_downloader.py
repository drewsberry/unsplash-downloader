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
            print("Ignored duplicate Unsplash image.")
            os.remove(new_filename)
            image_hashes.append(new_image_hash)

            return False
        else:
            print("Successfully saved unique Unsplash image", fname + ".")

            return True

    else:
        print("Failed to download Unplash image from", url + ".")

    return False


def hash_file(filename):
    md5 = hashlib.md5()

    with open(filename, "rb") as f:
        md5.update(f.read())

    return md5.digest()


def get_file_hashes(target_dir, trim_duplicates=False):
    print("Generating file hashes for folder", target_dir + "...")
    file_hashes = []

    for filename in os.listdir(target_dir):
        full_filename = target_dir + filename

        new_hash = hash_file(full_filename)

        if new_hash in file_hashes:
            if trim_duplicates:
                os.remove(full_filename)
        else:
            file_hashes.append(new_hash)

    print("Successfully generated", len(file_hashes),
          "file hashes from", target_dir + ".")
    return file_hashes


def main():
    image_hashes = get_file_hashes(IMAGE_DIR, SHOULD_TRIM_DUPLICATES)

    print("Downloading", NUM_IMAGES, "images from Unsplash...")

    num_images_downloaded = 0
    while (num_images_downloaded < NUM_IMAGES):
        if get_unplash_picture(IMAGE_DIR, WIDTH, HEIGHT, image_hashes):
            num_images_downloaded += 1
            print("Only", NUM_IMAGES - num_images_downloaded,
                  "images left to download.")

    print("Successfully downloaded", NUM_IMAGES,
          "unique images from Unsplash.")

if __name__ == "__main__":
    main()
