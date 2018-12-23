from PIL import Image, ImageDraw, ImageColor, ImageFont
import cv2
import skimage
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import json 
import pprint

image_width = 1920 # in pixel
image_height = 1080 # in pixel
text_color = "gray"
font_type = "Arial.ttf"
font_size = 29 # in point
txt_color = ImageColor.getrgb(text_color)
font = ImageFont.truetype(font_type, font_size) # somehow change from point --> pixel
testing_img = Image.new('RGB', (image_width, image_height))
testing_d = ImageDraw.Draw(testing_img)
start_x = 0
start_y = 0
testing_d.text((start_x, start_y), 'W88', txt_color, font)
#testing_d.text((font_size*2 + 8, 0), 'XX3', txt_color, font)

src = np.array(testing_img)
labels = skimage.measure.label(src, neighbors=8, background=0)
coords = []
for i in range(len(labels)): 
	for j in range(len(labels[i])): 
		boolean = False
		for k in labels[i][j]: 
			if k!=0: 
				boolean = True
		if boolean: 
			coords.append((j, i))
# print("coords: ", coords)
min_y = min(coords, key=lambda x: x[1])
max_y = max(coords, key=lambda x: x[1])
min_x = min(coords, key=lambda x: x[0])
max_x = max(coords, key=lambda x: x[0])
width = max_x[0] - min_x[0]
height = max_y[1] - min_y[1]

print("width: ", width)
print("height: ", height)

testing_d.rectangle([start_x, start_y, start_x + width, start_y + height], None, txt_color)
testing_img.save('codecharts/test.jpg')
# plt.imshow(src)
# plt.show() 


# CONNECTED COMPONENTS CODE!! 

# testing_img = Image.new('RGB', (image_width, image_height))
# testing_d = ImageDraw.Draw(testing_img)
# testing_d.text((x, y), triplet_code, txt_color, font)
# testing_img.save('codecharts/test.jpg')
# src = np.array(testing_img)
# labels = skimage.measure.label(src, neighbors=8, background=0)
# coords = []
# woo = False
# for i in range(len(labels)): 
# 	for j in range(len(labels[i])): 
# 		boolean = False
# 		for k in labels[i][j]: 
# 			if k!=0: 
# 				woo = True
# 				boolean = True
# 		if boolean: 
# 			coords.append((i, j))
# min_x = min(coords, key=lambda x: x[0])
# max_x = max(coords, key=lambda x: x[0])
# min_y = min(coords, key=lambda x: x[1])
# max_y = max(coords, key=lambda x: x[1])
# width = max_x[0] - min_x[0]
# height = max_y[1] - min_y[1]

# plt.imshow(src)
# plt.show()

# src = cv2.imread('codecharts/test.jpg', 0)
# binary_map = (src > 0).astype(np.uint8)
# connectivity = 8
# output = cv2.connectedComponentsWithStats(binary_map, connectivity, cv2.CV_32S) 
# stats = output[2]
# left = min(stats, key=lambda x: x[0])
# top = max(stats, key=lambda x: x[1])
# width = max(stats, key=lambda x: x[2])
# height = max(stats, key=lambda x: x[3])