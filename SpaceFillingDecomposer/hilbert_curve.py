from math import log
from PIL import Image
import numpy as np

def flip_curve_right90(curve):
    flipped = []
    for new_row in zip(*curve):
        flipped.append(list(new_row))
    return flipped

def flip_curve_left90(curve):
    flipped = []
    for new_row in zip(*curve[::-1]):
        flipped.append(list(new_row))
    return flipped

def mirror_curve_horizontally(curve):
    mirrored = []
    for row in curve:
        mirrored.append(row[::-1])
    return mirrored

def mirror_curve_vertically(curve):
    return curve[::-1]

def add_to_curve(curve, factor):
    new_curve = []
    for row in curve:
        new_curve.append([n+factor for n in row])
    return new_curve

def join_halves(curve1, curve2):
    new_curve = []
    for row1, row2 in zip(curve1, curve2):
        new_curve.append(row1 + row2)
    return new_curve

def gen_curve(order):
    if order>1:
        fact = 2 ** (2*(order-1))
        curve = gen_curve(order-1)
        quad1 = flip_curve_right90(curve)
        quad2 = mirror_curve_vertically(flip_curve_left90(add_to_curve(curve, fact*3)))
        quad4 = add_to_curve(curve, 2*fact)
        quad3 = add_to_curve(curve, fact)
        return join_halves(quad1, quad2) + join_halves(quad3, quad4)
    else:
        return [[0,3],
                [1,2]]

def decompose(image):
    pix_dict = {}
    image_dim = (image.size[0] * image.size[1]) ** (1/2)
    order = log(image_dim, 2)
    image.resize((2 ** int(order), 2 ** int(order)))
    curve = gen_curve(int(order))
    pixels = image.load()
    for y, row in enumerate(curve):
        for x, index in enumerate(row):
            pix_dict[index] = pixels[x, y]

    l = []
    for n in range(2 ** (2*int(order))):
        l.append(pix_dict[n])
    return l

def render_decomposed(decomposed):
    im = Image.new('RGB', (len(decomposed), 1))
    pixi = im.load()
    for n, pix in enumerate(decomposed):
        pixi[n, 0] = pix
    return im

def create_dataset(decomposed):
    reds, greens, blues = [], [], []
    for pix in decomposed:
        reds.append(pix[0]/255)
        greens.append(pix[1]/255)
        blues.append(pix[2]/255)
    return np.array([reds, greens, blues])


def visualized_dataset(dataset):
    im = Image.new('RGB', (dataset.shape[1], 3))
    pix = im.load()
    for n, (red, green, blue) in enumerate(zip(*dataset)):
        pix[n, 0] = (int(red*255), 0, 0)
        pix[n, 1] = (0, int(green*255), 0)
        pix[n, 2] = (0, 0, int(blue*255))
    return im

if __name__ == '__main__':
    I = Image.open('forest.jpg')
    compost = decompose(I)
    pretty = render_decomposed(compost)
    pretty.save('compost_forest.png')
    pretty.show()


    data = create_dataset(compost)
    visualized_dataset(data).save('compost_forest_dataset.png')










