# Tile Maker
# Write a program that produces a tiled image from a single image, much
# like a tiles of cat faces in Figure 21-6. Your program should have a make_tile()
# function withe three arguments: a string of the image filename, an integer
# for how many times it should be tiled horizontally, and an integer for how many times
# it should be tiled vertically. The make_tile() function should return a larger Image object of the tiled image. You will
# use the paste() methods as part of this function.
#   For example, if zophie_the_cat.jpg was a 20x50-pixel image, calling make_tile('zophie_the_cat.jpg', 6, 10) should return a 120x500 image
# with 60 tiles total. For a bonus, try randomly flipping or rotating the image to tile when pasting it to the larger image. This title maker works best with
# smaller images to tile. See what abstract art you can create with this code.

import sys
import random

from PIL import Image


def check_input(argv) -> bool:
    if len(argv) != 4 or not argv[2].isdigit() or not argv[3].isdigit():
        print(f"Usage error:{argv[0]} <filename> <tiles_horizontally> <tiles_vertically>")
        return False
    if int(argv[2]) < 1 or int(argv[3]) < 1:
        print("Tile counts must be at least 1")
        return False
    return True


def randomize_tile(tile: Image.Image) -> Image.Image:
    if random.random() < 0.5:
        tile = tile.transpose(Image.FLIP_LEFT_RIGHT)
    if random.random() < 0.5:
        tile = tile.transpose(Image.FLIP_TOP_BOTTOM)
    tile = tile.rotate(random.choice([0, 90, 180, 270]), expand=True)
    return tile


def make_tile(filename: str, horizontal_tiles: int, vertical_tiles: int) -> Image.Image:
    try:
        with Image.open(filename) as tile:
            tile_width, tile_height = tile.size
            result = Image.new('RGB', (tile_width * horizontal_tiles, tile_height * vertical_tiles))
            for row in range(vertical_tiles):
                for col in range(horizontal_tiles):
                    x = col * tile_width
                    y = row * tile_height
                    result.paste(randomize_tile(tile), (x, y))
    except FileNotFoundError:
        print(f"Error: could not find image file '{filename}'")
        sys.exit(1)

    return result


def main():
    if not check_input(sys.argv):
        sys.exit(1)
    
    tiled_image = make_tile(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    tiled_image.save("tiled_output.png")


if __name__ == "__main__":
    main()

