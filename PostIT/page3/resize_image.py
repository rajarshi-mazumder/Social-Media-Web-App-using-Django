from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO, StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import random
import string


def get_size_format(b, factor=1024, suffix="B"):
    """ 
    Scale bytes to its proper byte format 
    e.g: 
        1253656 => '1.20MB' 
        1253656678 => '1.17GB' 
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


def compress_image(img, new_size_ratio=0.9, quality=10, image_width=None, height_width=None, to_jpg=True):
    print("OG Image: ", img)
    print("[*] The size of image:", img.size)
    print("[*] Size before compression:", get_size_format(img.size))

    img = Image.open(img)

    print(img)
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio),
                         int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        # print new image shape
        print("New Image shape:", img.size)

        print("pppp", img)
        # return img

        # code from stackoverflow
        img_io = BytesIO()  # creat in memory object by io (you should import io)
        # save your PIL image object to memory object you created by io
        img = img.convert('RGB')
        img.save(img_io, format='jpeg', quality=20, optimize=True)
        # you should import InMemoryUploadedFile
        # give your file to InMemoryUploadedFile to create django imagefield object
        # thumb = InMemoryUploadedFile(
        #     img_io, None, 'foo2.jpeg', 'image/jpeg', thumb_io.seek(0, os.SEEK_END), None)
        new_pic = InMemoryUploadedFile(img_io,
                                       'ImageField',
                                       get_random_string(10),
                                       'JPEG',
                                       sys.getsizeof(img_io), None)
        print(new_pic.size)
        print("[*] Size after compression:", get_size_format(new_pic.size))
        return new_pic

    elif image_width and height_width:
        # if image_width and height_width are set, resize with them instead
        img = img.resize((image_width, height_width), Image.ANTIALIAS)
        # print new image shape
        print("New Image shape:", img.size)
        print("pppp", img)
        return img
