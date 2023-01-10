from PIL import Image
from collections import Counter
from scipy.spatial import KDTree
import numpy as np
def hex_to_rgb(num):
    h = str(num)
    return int(h[0:4], 16), int(('0x' + h[4:6]), 16), int(('0x' + h[6:8]), 16)
def rgb_to_hex(num):
    h = str(num)
    return int(h[0:4], 16), int(('0x' + h[4:6]), 16), int(('0x' + h[6:8]), 16)
filename = input("What's the image name? ")
new_w, new_h = map(int, input("What's the new height x width? Like 28 28. ").split(' '))
# bkg
# palette_hex = ['0x4A3717', '0x525242', '0x5C492F', '0x776447', 
#                '0x524023', '0x69563B', '0x847555', '0xB9CFDB', '0x93A7A9', 
#                '0x342303', '0x606550', '0xAB9B6E', '0x9D8657', '0x8B886F', 
#                '0xBEB180', '0xD7CB97']

# marco
# palette_hex = ['0xff00ff', '0x000000', '0xFFFFFF', '0x3a3010',
#                '0x73693a', '0xbdb273', '0xd6a25a', '0x8c5920',
#                '0x422000', '0xb54100', '0xfee34a', '0xffeb94', 
#                '0x7b0000', '0xd6a15a', '0x412100', '0x8c591f']

# enemy
# palette_hex = ['0x282828', '0x000000', '0xFFFFFF', '0x484800',
#                '0xa7b157', '0xe7f088', '0x717828', '0x402100',
#                '0x906828', '0xd0a058', '0xf9e088', '0x7f1800', 
#                '0xc86140', '0x956c28', '0xd5a45b', '0x402000']

# bkg new
# palette_hex = ['0x000000', '0xFFFFFF', '0x302100', '0x59563D', 
#                '0xB9D0D8', '0x8F9B8C', '0x39332A', '0x98AFB6',
#                '0x424C48', '0x84632F', '0xD7B971', '0x6E7E7E',
#                '0x6C4E1D', '0xECDD93', '0x4D3F1C', '0xB7CEC7']

# bullet
# palette_hex = ['0xffed63', '0xfff5a7', '0xff9200', '0xff00ff']

# board
palette_hex = ['0x282828', '0xAAAAAA']

# cannon
# palette_hex = ['0xff00ff', '0xfec437', '0xFFFFFF', '0x372411',
#                '0x6b5942', '0x630200', '0x922700', '0xbe4e0e',]

# black and white
# palette_hex = ['0x000000', '0xFFFFFF']



## '0xFF00FF' is pink


palette_rgb = [hex_to_rgb(color) for color in palette_hex]

pixel_tree = KDTree(palette_rgb)
im = Image.open("./sprite_originals/" + filename+ ".png") #Can be many different formats.
im = im.convert("RGBA")
im = im.resize((new_w, new_h),Image.ANTIALIAS) # regular resize
pix = im.load()
pix_freqs = Counter([pix[x, y] for x in range(im.size[0]) for y in range(im.size[1])])
pix_freqs_sorted = sorted(pix_freqs.items(), key=lambda x: x[1])
pix_freqs_sorted.reverse()
print(pix)
outImg = Image.new('RGB', im.size, color='white')
outFile = open("./sprite_bytes/" + filename + '.txt', 'w')
i = 0
for y in range(im.size[1]):
    for x in range(im.size[0]):
        pixel = im.getpixel((x,y))
        print(pixel)
        if(pixel[3] < 200):
            outImg.putpixel((x,y), palette_rgb[0])
            outFile.write("%x\n" % (0))
            print(i)
        else:
            index = pixel_tree.query(pixel[:3])[1]
            outImg.putpixel((x,y), palette_rgb[index])
            outFile.write("%x\n" % (index))
        i += 1
outFile.close()
outImg.save("./sprite_converted/" + filename + ".png")

