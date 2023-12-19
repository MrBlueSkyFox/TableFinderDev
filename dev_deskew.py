import numpy as np
import os

os.environ['MAGICK_HOME'] = './wand'

# from PIL import Image as ImagePIL
# from wand.image import Image

if __name__ == "__main__":
    print(np.array([10, 20]))
    pass
    # np.array([10,20])
    # pass
    # path_src = r"C:\Users\t.abraamyan\Dsocuments\PythonPRJ\TableFinderDev\data\default\pos_credit_1_page-0001.jpg"
    # image = ImagePIL.open(path_src)
    # with Image.from_array(np.array(image)) as img:
    #     img.deskew(0.4 * img.quantum_range)
    #     deskew_img = img.clone()
    #     deskew_img = ImagePIL.fromarray(np.array(deskew_img))
    #     deskew_img.save("out.jpg")
