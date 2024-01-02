import os


def get_all_jpg_images_in_directory(directory):
    """Returns a list of all JPEG images in the given directory.

    Args:
        directory: The path to the directory to search.

    Returns:
        A list of all JPEG images in the given directory.
    """

    jpg_images = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            jpg_images.append(os.path.join(directory, filename))


def create_output_json(path: str, file_name: str) -> str:
    return os.path.join(path, file_name + ".json")
