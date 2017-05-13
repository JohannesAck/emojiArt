from os import listdir
import os.path
import cv2


def index_emoji(path_of_folder):
    """
    Indexes emoji by mean color
    :param path_of_folder: path to the folder containing emoji
    :return:
    """
    dir = listdir(path_of_folder)
    index = {}
    count = 0
    for emoji in dir:
        count += 1
        print('Processing emoji:' + emoji + " (" + str(count) + '/2427)')
        index.update({emoji : list(mean_color_of_file(os.path.join(path_of_folder, emoji)))})  # adds path and color to dict

    return index


def mean_color_of_file(path):
    """
    Calculates the mean color of a given file
    """
    image = cv2.imread(path, cv2.IMREAD_COLOR)

    colorsum = [0, 0, 0]
    for x in range(len(image)):
        for y in range(len(image[0])):
            colorsum[0] += image[x][y][0]
            colorsum[1] += image[x][y][1]
            colorsum[2] += image[x][y][2]

    # calc mean
    colorsum[:] = [x // (len(image) * len(image[0])) for x in colorsum]

    return colorsum
