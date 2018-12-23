from PIL import Image, ImageDraw, ImageColor, ImageFont
import cv2
import skimage
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import json 
import pprint
import generate_code

image_width = 1920 # in pixel
image_height = 1080 # in pixel
border_padding = 100
text_color = "white"
font_type = "Arial.ttf"
px_pt_ratio = 20/29 # according to our image dimensions, 29 point = 20 px
font_size = 30 # in pixel - described in paper

def pixel_to_point(num): 
	return int(num*(1/px_pt_ratio))

correct_code = {}
img_count = 1
for i in range(32):
	# generate random code chart
	filename, valid_codes, coordinates = generate_code.create_codechart('/sentinel/sentinel_code_chart_' + str(img_count))
	# pick random code 
	r = list(range(0, len(valid_codes)))
	index = random.choice(r)
	triplet = valid_codes[index]
	triplet_coordinate = coordinates[triplet]
	# to make sure that the cross is visible
	while (triplet_coordinate[0] <= border_padding or triplet_coordinate[0] >= image_width-border_padding) or (triplet_coordinate[1] <= border_padding or triplet_coordinate[1] >=image_height-border_padding): 
		index = random.choice(r)
		triplet = valid_codes[index]
		triplet_coordinate = coordinates[triplet]
	coordinate = (triplet_coordinate[0]+20, triplet_coordinate[1])
	# create sentinel image
	img = Image.new('RGB', (image_width, image_height), (126, 126, 126))
	d = ImageDraw.Draw(img)
	txt_color = ImageColor.getrgb(text_color)
	font = ImageFont.truetype(font_type, pixel_to_point(font_size)) # takes in point value
	d.text(coordinate, '+', txt_color, font)

	bucket = ''
	if img_count>=1 and img_count<=4: 
		bucket = 'bucket1'
	elif img_count>=5 and img_count<=8: 
		bucket = 'bucket2'
	elif img_count>=9 and img_count<=12: 
		bucket = 'bucket3'
	elif img_count>=13 and img_count<=16: 
		bucket = 'bucket4'
	elif img_count>=17 and img_count<=20: 
		bucket = 'bucket5'
	elif img_count>=21 and img_count<=24: 
		bucket = 'bucket6'
	elif img_count>=25 and img_count<=28: 
		bucket = 'bucket7'
	elif img_count>=29 and img_count<=32: 
		bucket = 'bucket8'

	filename = './sentinel_images/' + bucket + '/sentinel_image_' + str(img_count) + '.jpg'
	img.save(filename)
	correct_code[filename] = (triplet, coordinate)
	img_count+=1

with open('./sentinel_images/sentinel_codes.json', 'w') as outfile: 
		json.dump(correct_code, outfile)

## FIXATION CROSS CODE ##

# img = Image.new('RGB', (image_width, image_height), (126, 126, 126))
# d = ImageDraw.Draw(img)
# txt_color = ImageColor.getrgb(text_color)
# font = ImageFont.truetype(font_type, pixel_to_point(font_size)) # takes in point value
# d.text((940, 520), '+', txt_color, font)
# filename = 'sentinel_images/test.jpg'
# img.save(filename)
