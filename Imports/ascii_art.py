from PIL import Image
from PIL import ImageStat
from PIL import ImageOps
import os
import random

class get_ascii_image():
    def __init__(self):
        self.pixel_data = []
        self.ascii_10x20_pixel_data = dict()
        self.ascii_8x12_pixel_data = dict()
        self.ascii_chars = dict()


    def get_image(self, file_name):
        img = Image.open('Images/' + file_name)
        self.create_monotone_thumbnail(img)


    def create_monotone_thumbnail(self, img):
        size = 120, 15
        new_img = img.resize(size, Image.ANTIALIAS)                                          # Resizes the image to size defined above
        new_img = ImageOps.grayscale(new_img)                               # Converts image to grayscale
        # new_img = ImageOps.invert(new_img)
        # Save the image to appropriate directory with new name
        # new_img.save('Monotone Thumbnails/' + image_name + '_monoThumb.jpeg')
        self.pixel_data.append(list(new_img.getdata()))
        self.get_ascii_data()


    def get_ascii_data(self):
        """
        """
        font_list = os.listdir('Fonts/wincmd10x20')

        for file_name in font_list:
            image_file = file_name.split('.')
            image_name = image_file[0]
            img = Image.open('Fonts/wincmd10x20/' + file_name)
            stat = ImageStat.Stat(img)

            self.ascii_chars[chr(int(image_name))] = file_name

            self.ascii_10x20_pixel_data.setdefault(int(round(stat.mean[0])), []).append(file_name)

        self.get_ascii_string()


    def get_ascii_string(self):
        """
        """
        # create a reversed list for pixel_data
        reversed_ascii_chars = [(value, key) for (key, value) in self.ascii_chars.iteritems()]
        reversed_dict = dict(reversed_ascii_chars)

        # compare pixel data from char and img
        for i in range(0, len(self.pixel_data)):
            the_string = ''

            for j in range(0, len(self.pixel_data[i])):

                if self.pixel_data[i][j] == 0.0:
                    # then get img from ascii dict where ascii_dict[0]
                    ascii_file_name = self.ascii_10x20_pixel_data[0]
                    the_string += reversed_dict[ascii_file_name[0]]
                else :
                    max_keys = max(self.ascii_10x20_pixel_data.keys())
                    scaled_pixel_data = (self.pixel_data[i][j] / 255.0) * max_keys   # scale the pixel data

                    for m in range(0, len(self.ascii_10x20_pixel_data.keys())):
                        pixel_keys = self.ascii_10x20_pixel_data.keys()
                        if pixel_keys[m] < scaled_pixel_data <= pixel_keys[m + 1] :
                            ascii_file_name = self.ascii_10x20_pixel_data[pixel_keys[m]]
                            the_string += reversed_dict[random.choice(ascii_file_name)]

            the_list = list(the_string)
            while the_list:
                line = the_list[0:120]
                if line != ' '*120:
                    print ''.join(line)
                # print '\n'
                del the_list[0:120]