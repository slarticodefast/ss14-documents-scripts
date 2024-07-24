# made by slarticodefast
# Version 1.01
# run this script using
# python image_to_paper.py plushie_spacelizard.png
# if you don't want to cut off transparent borders use
# python image_to_paper.py plushie_lizard.png false

import PIL.Image
import numpy as np
import sys

char_transparent = '░░'
char_black = '██'
color_open = '[color={}]'
color_close = '[/color]'

image_path = sys.argv[1]
img = PIL.Image.open(image_path)
img_data = np.array(img)
print('loaded '+image_path)

if not (len(sys.argv)>1 and sys.argv[1]=="false"):
    img_mask = img_data[:,:,3]==0
    coords = np.argwhere(~img_mask)
    y0,x0 = coords.min(axis=0)
    y1,x1 = coords.max(axis=0) + 1  # slices are exclusive at the top
    img_data = img_data[y0:y1, x0:x1]

img_data[img_data[:,:,3]==0]=np.array((255,255,255,0)) # set all transparent pixels to white so char_transparent is colored correctly

text=''
preview=''
previous_color = None

for y in range(img_data.shape[0]):
    for x in range(img_data.shape[1]):
        if (img_data[y,x,3]==0):
            add_text = char_transparent
        else:
            add_text = char_black
        color_hex = '#{:02x}{:02x}{:02x}'.format(img_data[y,x,0],img_data[y,x,1],img_data[y,x,2])
        if color_hex != previous_color:
            if (previous_color!=None):
                text += color_close
            text += color_open.format(color_hex) + add_text  
            previous_color = color_hex
        else:
            text += add_text
        preview += add_text
    text += '\n'
    preview += '\n'
if (previous_color!=None):
    text += color_close + '\n' # close the last markup tag if we opened one

print('preview (no color):')
print(preview) # TODO: ANSI colors for preview
with open('paper.txt', 'w', encoding='utf-8') as text_file:
    text_file.write(text)
print('output written to paper.txt')