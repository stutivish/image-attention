from PIL import Image, ImageDraw, ImageColor, ImageFont
import cv2
import skimage
import matplotlib.pyplot as plt
import numpy as np
import string
import random
import json 
import pprint

# DEFINE PARAMATERS 
forbidden_letters = set(["I", "O"]) # letters to not use in c
image_width = 1920 # in pixel
image_height = 1080 # in pixel
px_pt_ratio = 20/29 # according to our image dimensions, 29 point = 20 px
text_color = "gray"
font_type = "Arial.ttf"
font_size = 20 # in pixel - described in paper
max_triplet_width = 60 # in pixel - the widest a triplet can be; utlilized 'W88' as widest triplet code (width~60, height=20) --> thus it is 3 times as big as the height
max_triplet_height = font_size # the tallest a triplet can be
d_v = 4*max_triplet_height # vertical distance b/w triplets in the grid
d_h = 2*max_triplet_width # horizontal distance b/w triplets = 2*d_v in the grid
post_jitter_buffer = 6 # small buffer to cover edge case of triplets immediately adjacent to one another (so that there's differentiability in reading the tripets)
j_v = int(0.25*(d_v) - post_jitter_buffer/2) # max vertical jitter for one side of a triplet
j_h = int(0.25*(d_h) - post_jitter_buffer) # max horizontal jitter for on side of a triplet  
num_codecharts = 1

data = {}

def point_to_pixel(num): 
	return int(num*px_pt_ratio)

def pixel_to_point(num): 
	return int(num*(1/px_pt_ratio))

def generate_rand_letter(): 
	letter = random.choice(string.ascii_uppercase)
	if letter in forbidden_letters: 
		return generate_rand_letter()
	return letter

def generate_rand_triplet(): 
	code = ""
	code += generate_rand_letter()
	for i in range(0, 2): 
		forbidden_num = 0
		if len(code) == 2: 
			forbidden_num = int(code[1])
		r = list(range(1, forbidden_num)) + list(range(forbidden_num+1, 10))
		code += str(random.choice(r))
	return code

def create_codechart(img_count): 
	# ADD FLAGS TO TURN JITTER ON AND OFF

	testing_img = Image.new('RGB', (image_width, image_height))
	img = Image.new('RGB', (image_width, image_height))

	d = ImageDraw.Draw(img)
	txt_color = ImageColor.getrgb(text_color)
	font = ImageFont.truetype(font_type, pixel_to_point(font_size)) # takes in point value
	valid_codes = set()
	coordinates = {}

	for x in range(0, image_width, d_h): 
		for y in range(0, image_height, d_v): 
			triplet_code = generate_rand_triplet()
			# check for if code has already been made in image since all codes should be unique
			while triplet_code in valid_codes: 
				triplet_code = generate_rand_triplet() 
			valid_codes.add(triplet_code)

			# implement jitter to x and y 
			x_range = list(range(x-j_h, x+j_h+1))
			y_range = list(range(y-j_v, y+j_v+1))
			j_x = random.choice(x_range)
			j_y = random.choice(y_range)

			# writes triplet to image 
			d.text((j_x, j_y), triplet_code, txt_color, font)
			coordinates[triplet_code] = (j_x, j_y)
	filename = './codecharts' + str(img_count) + '.jpg'
	# filename = 'codecharts/quick_test.jpg'
	img.save(filename)
	return (filename, list(valid_codes), coordinates)

# for i in range(num_codecharts): 
# 	filename, valid_codes = create_codechart(i+1)
# 	data[filename] = valid_codes

# with open('data.json', 'w') as outfile: 
# 	json.dump(data, outfile)

