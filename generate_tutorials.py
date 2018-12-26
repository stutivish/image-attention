import generate_code
import os
import string
import random
import json 
import pprint
import matplotlib.pyplot as plt
import numpy as np
import base64 


path = './tutorials'
files = os.listdir(path)
tutorial_files = []

for file in files: 
	if not 'images' in file: 
		tutorial_files.append(file)

ts_codechart_path = './codecharts/sentinel'
# ts_codecharts = os.listdir(ts_codechart_path)

# ts_img_to_num_dict = {} # maps image to its number {"img_path: 4"}
# ts_cc_dict = {} # maps number to codechart {"4: codechart_path"}
# ts_dict = {} # maps image to its codechart {"img_path: codechart_path"}


# for tsi in all_sentinel_images: 
# 	image_num = tsi[tsi.index('image_')+6:tsi.index('.jpg')]
# 	ts_img_to_num_dict[tsi] = image_num

# for tscc in sentinel_codecharts: 
# 	cc_num = tscc[tscc.index('chart_')+6:tscc.index('.jpg')]
# 	ts_cc_dict[cc_num] = tscc

# for tsi in all_sentinel_images: 
# 	num = ts_img_to_num_dict[sti]
# 	tscc = ts_cc_dict[num]
# 	bucket = num_to_bucket_dict[num]
# 	sentinel_dict[sentinel_path + '/' + bucket + '/' + si] = sentinel_codechart_path + '/' + scc


num_to_bucket_dict = {} # maps each number to its bucket {"1: bucket1...4: bucket1, 5: bucket2,..."}

# assigns each number to its bucket 
for i in range(33, 42): 
	bucket = ''
	if i>=33 and i<=36: 
		bucket = 'bucket9'
	elif i>=37 and i<=40: 
		bucket = 'bucket10'
	elif i>=41: 
		bucket = 'bucket11'
	num_to_bucket_dict[str(i)] = bucket

# loads the valid codes for the sentinel images 
with open('./sentinel_images/sentinel_codes.json') as f:
    sentinel_codes_data = json.load(f) # contains mapping of sentinel image path to (valid triplet code, coordinate of valid triplet code)


tutorials = []

for file in tutorial_files: 
	single_tutorial = []
	real_dict = {}
	sentinel_dict = {}
	tutorial_folder = path + '/' + file
	imgs = os.listdir(tutorial_folder)
	for img in imgs: 
		if "real" in img: 
			real_dict["image"] = tutorial_folder + '/' + img
			img_count = img[img.index("real")+4:img.index(".jpg")]
			filename, valid_codes, coordinates = generate_code.create_codechart('/tutorial/tutorial_code_chart_' + str(img_count))
			real_dict["codechart"] = filename
			real_dict["codes"] = valid_codes
			real_dict["flag"] = 'tutorial_real'
			real_dict["coordinates"] = coordinates
			single_tutorial.append(real_dict)
		else: 
			sentinel_dict["image"] = tutorial_folder + '/' + img
			img_count = img[img.index("image_")+6:img.index(".jpg")]
			sentinel_dict["codechart"] = ts_codechart_path + '/' + 'sentinel_code_chart_' + str(img_count) + '.jpg'
			bucket = num_to_bucket_dict[img_count]
			sentinel_path = './sentinel_images/' + bucket + '/' + img
			sentinel_dict["correct_code"] = sentinel_codes_data[sentinel_path][0]
			sentinel_dict["valid_codes"] = sentinel_codes_data[sentinel_path][2]
			sentinel_dict["flag"] = 'tutorial_sentinel'
			sentinel_dict["coordinates"] = sentinel_codes_data[sentinel_path][1]
			single_tutorial.append(sentinel_dict)
	tutorials.append(single_tutorial)

with open('./tutorials/tutorial.json', 'w') as outfile: 
		json.dump(tutorials, outfile)
			












