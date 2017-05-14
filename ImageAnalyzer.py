import cv2
import matplotlib.pyplot as plt
import EmojiAnalyzer
import math
import os
import json


def cvToMatplt(image):
    """
    Takes a cv2 image and converts it into an appropriate format for matplotlib
    :param image:
    :return:
    """
    returnImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return returnImg


def meanSquares(image, square_size):
    """
    Splits an image in to squares of a given size and paints them in the average color as well as returns average
    colors as array
    :param image: Images in cv2 BGR format
    :param square_size: edge length of a square
    :return: squarified image, array
    """
    # calc number of squares in both directions
    x_dim = len(image)
    y_dim = len(image[0])
    x_amount = x_dim // square_size
    y_amount = y_dim // square_size

    mean_color_array = [[0 for y in range(y_amount)] for x in range(x_amount)]
    for x_square_num in range(0, x_amount):  # assumes x > y
        for y_square_num in range(0, y_amount):
            # calc average from x_square * square_size and y_square * square_size on
            x_start = x_square_num * square_size
            y_start = y_square_num * square_size

            # sum up pixels in square
            colorsum = [0, 0, 0]
            for x in range(x_start, x_start + square_size):
                for y in range(y_start, y_start + square_size):
                    colorsum[0] += image[x][y][0]
                    colorsum[1] += image[x][y][1]
                    colorsum[2] += image[x][y][2]

            # calc mean
            colorsum[:] = [x // (square_size ** 2) for x in colorsum]

            # set squares to mean
            for x in range(x_start, x_start + square_size):
                for y in range(y_start, y_start + square_size):
                    image[x][y][0] = colorsum[0]
                    image[x][y][1] = colorsum[1]
                    image[x][y][2] = colorsum[2]
            mean_color_array[x_square_num][y_square_num] = colorsum  # save result
    return image, mean_color_array


def emojify_image(image, emoji_dict, mean_array, square_size, path_of_folder='emoji'):
    """
    Emojifies the image and returns it
    """
    # TODO: move most other function calls here
    x_dim = len(image)
    y_dim = len(image[0])
    x_amount = x_dim // square_size
    y_amount = y_dim // square_size

    for x_square_num in range(0, x_amount):
        for y_square_num in range(0, y_amount):

            # calc closest matching emoji

            best_fit = ''
            minimum_distance = 1000000
            for key, val in emoji_dict.items():
                distance = math.sqrt(
                    (mean_array[x_square_num][y_square_num][0] - val[0]) ** 2 +
                    (mean_array[x_square_num][y_square_num][1] - val[1]) ** 2 +
                    (mean_array[x_square_num][y_square_num][2] - val[2]) ** 2
                )  # euclidian distance
                if distance < minimum_distance:
                    minimum_distance = distance
                    best_fit = key

            # load and crop emoji

            emoji_img = cv2.imread(os.path.join(path_of_folder, best_fit), cv2.IMREAD_COLOR)
            emoji_cropped = cv2.resize(emoji_img, (square_size, square_size))

            # put emoji in image

            x_start = x_square_num * square_size
            y_start = y_square_num * square_size
            for x in range(square_size):
                for y in range(square_size):
                    image[x + x_start][y + y_start] = emoji_cropped[x][y]
    return image


def main():
    emoji_path = 'emoji'
    square_size = 5
    image_path = 'johannes.jpg'

    # generate or load emoji_dict
    emoji_dict = {}
    if (os.path.isfile('emoji_dict.json')):
        with open('emoji_dict.json', 'r') as f:
            emoji_dict = json.load(f)
    else:
        emoji_dict = EmojiAnalyzer.index_emoji(emoji_path)
        try:
            with open('emoji_dict.json', 'w') as f:
                json.dump(dict(emoji_dict), f)
        except Exception:
            print('Exception during json dump, removing json file.')
            if os.path.isfile('emoji_dict.json'):
                os.remove('emoji_dict.json')

    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    square_img, mean_array = meanSquares(img, square_size)

    print('Emojifying image...')
    emojifyed_img = emojify_image(img, emoji_dict, mean_array, square_size, emoji_path)

    cv2.imwrite('output.jpg', emojifyed_img)

    plt.imshow(cvToMatplt(emojifyed_img))
    plt.show()


if __name__ == '__main__':
    main()
