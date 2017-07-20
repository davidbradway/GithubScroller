#!/home/dpb6/miniconda3/bin/python
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
#
# Direct translation of example 1 from the freetype tutorial:
# http://www.freetype.org/freetype2/docs/tutorial/step1.html
#
import math
import datetime as dt
import matplotlib.pyplot as plt
from subprocess import call
from freetype.raw import *
from PIL import Image

[WIDTH, HEIGHT] = 104, 7


def to_c_str(text):
    """ Convert python strings to null terminated c strings. """
    c_str = create_string_buffer(text.encode(encoding='UTF-8'))
    return cast(pointer(c_str), POINTER(c_char))


def draw_bitmap(image, bitmap, x, y):
    x_max = x + bitmap.width
    y_max = y + bitmap.rows
    for p, i in enumerate(range(x, x_max)):
        for q, j in enumerate(range(y, y_max)):
            if i < 0 or j < 0 or i >= WIDTH or j >= HEIGHT:
                continue
            pixel = image.getpixel((i, j))
            pixel |= int(bitmap.buffer[q * bitmap.width + p])
            image.putpixel((i, j), pixel)
    return image


def draw_word(text, image):

    library = FT_Library()
    matrix = FT_Matrix()
    face = FT_Face()
    pen = FT_Vector()
    font_filename = 'Vera.ttf'
    num_chars = len(text)
    angle = (0. / 360) * 3.14159 * 2

    # initialize library, error handling omitted
    error = FT_Init_FreeType(byref(library))

    # create face object, error handling omitted
    error = FT_New_Face(library, to_c_str(font_filename), 0, byref(face))

    # set character size: 7pt at 100dpi, error handling omitted
    error = FT_Set_Char_Size(face, 7 * 64, 0, 100, 0)
    slot = face.contents.glyph

    # set up matrix
    matrix.xx = int(math.cos(angle) * 0x10000)
    matrix.xy = int(-math.sin(angle) * 0x10000)
    matrix.yx = int(math.sin(angle) * 0x10000)
    matrix.yy = int(math.cos(angle) * 0x10000)

    # start at (0,0) relative to the upper left corner  */
    pen.x = 0 * 64
    pen.y = (HEIGHT - 7) * 64

    for n in range(num_chars):
        # set transformation
        FT_Set_Transform(face, byref(matrix), byref(pen))

        # load glyph image into the slot (erase previous one)
        charcode = ord(text[n])
        index = FT_Get_Char_Index(face, charcode)
        FT_Load_Glyph(face, index, FT_LOAD_RENDER)

        # now, draw to our target surface (convert position)
        image = draw_bitmap(image, slot.contents.bitmap,
                            slot.contents.bitmap_left,
                            HEIGHT - slot.contents.bitmap_top)

        # increment pen position
        pen.x += slot.contents.advance.x
        pen.y += slot.contents.advance.y

    FT_Done_Face(face)
    FT_Done_FreeType(library)
    return image


def show_word(image):
    plt.imshow(image, origin='lower',
               interpolation='nearest', cmap=plt.cm.gray)
    plt.gca().invert_yaxis()
    plt.show()


def make_n_commits(n):
    for i in range(n):
        now = dt.datetime.now().strftime("%H:%M:%S.%f")
        call(["touch", "." + now + '.txt'])
        call(["git", "add", "."])
        call(["git", "commit", "-m", "'add " + now + " file'"])
        call(["git", "rm", ".*.txt"])
        call(["git", "commit", "-m", "'remove text files'"])
    call(["git", "status"])
    call(["git", "push"])


def main():
    image = Image.new('L', (WIDTH, HEIGHT))
    image = draw_word('DAVID P. BRADWAY', image)
    # show_word(image)
    rgb_im = image.convert('RGB')
    commits = [0, 1, 3, 5, 10]

    # need top corner to be sunday of the week
    # when you want to start drawing pixels
    day0 = dt.datetime(2017, 7, 16, 0, 0, 0)
    day_diff = dt.datetime.today() - day0
    column = day_diff.days // HEIGHT
    # print(column)
    row = day_diff.days % HEIGHT
    # print(row)
    r, g, b = rgb_im.getpixel((column, HEIGHT - 1 - row))
    level = math.floor((r + g + b) / 3. / 255. * (len(commits)-1))

    print(commits[level])
    make_n_commits(commits[level])

if __name__ == '__main__':
    main()
