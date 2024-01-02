import os


def get_all_jpg_images_in_directory(directory):
    """Returns a list of all JPEG images in the given directory.

    Args:
        directory: The path to the directory to search.

    Returns:
        A list of all JPEG images in the given directory.
    """

    jpg_images = get_all_with_ext_in_dir(directory, ".jpg")
    return jpg_images


def get_all_pdf_files_in_directory(directory: str):
    pdf_files = get_all_with_ext_in_dir(directory, ".pdf")
    return pdf_files


def get_all_with_ext_in_dir(directory: str, ext: str):
    ext_files = []
    for filename in os.listdir(directory):
        if filename.endswith(ext):
            ext_files.append(os.path.join(directory, filename))

    return ext_files


def get_basename(path: str) -> str:
    base_file_name = os.path.basename(path)
    base_file_name = os.path.splitext(base_file_name)[0]
    return base_file_name


def create_output_json(path: str, file_name: str) -> str:
    return os.path.join(path, file_name + ".json")
