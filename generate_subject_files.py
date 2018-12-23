import generate_code
import os
import string
import random
import json 
import pprint
import matplotlib.pyplot as plt
import numpy as np
import base64 

path = './all_images'
files = os.listdir(path)

random.shuffle(files)

sentinel_path = './sentinel_images'
sentinel_codechart_path = './codecharts/sentinel'
sentinel_codecharts = os.listdir(sentinel_codechart_path)

all_buckets = []
img_count = 0
num_buckets = 8
num_subject_files = 100
num_images_per_sf = 20
images_per_bucket = int(len(files)/num_buckets)
for i in range(0, len(files), images_per_bucket): 
	all_buckets.append(files[i:i+images_per_bucket])

bucket1 = all_buckets[0]
bucket2 = all_buckets[1]
bucket3 = all_buckets[2]
bucket4 = all_buckets[3]
bucket5 = all_buckets[4]
bucket6 = all_buckets[5]
bucket7 = all_buckets[6]
bucket8 = all_buckets[7]

sentinel_bucket1 = os.listdir('./sentinel_images/bucket1')
sentinel_bucket2 = os.listdir('./sentinel_images/bucket2')
sentinel_bucket3 = os.listdir('./sentinel_images/bucket3')
sentinel_bucket4 = os.listdir('./sentinel_images/bucket4')
sentinel_bucket5 = os.listdir('./sentinel_images/bucket5')
sentinel_bucket6 = os.listdir('./sentinel_images/bucket6')
sentinel_bucket7 = os.listdir('./sentinel_images/bucket7')
sentinel_bucket8 = os.listdir('./sentinel_images/bucket8')
all_sentinel_buckets = [sentinel_bucket1, sentinel_bucket2, sentinel_bucket3, sentinel_bucket4, sentinel_bucket5, sentinel_bucket6, sentinel_bucket7, sentinel_bucket8]

sentinel_img_to_num_dict = {}
sentinel_num_to_img_dict = {}
sentinel_cc_dict = {}
sentinel_dict = {}
num_to_bucket_dict = {}

all_sentinel_images = []
all_sentinel_images.extend(sentinel_bucket1)
all_sentinel_images.extend(sentinel_bucket2)
all_sentinel_images.extend(sentinel_bucket3)
all_sentinel_images.extend(sentinel_bucket4)
all_sentinel_images.extend(sentinel_bucket5)
all_sentinel_images.extend(sentinel_bucket6)
all_sentinel_images.extend(sentinel_bucket7)
all_sentinel_images.extend(sentinel_bucket8)

for i in range(1, 33): 
	bucket = ''
	if i>=1 and i<=4: 
		bucket = 'bucket1'
	elif i>=5 and i<=8: 
		bucket = 'bucket2'
	elif i>=9 and i<=12: 
		bucket = 'bucket3'
	elif i>=13 and i<=16: 
		bucket = 'bucket4'
	elif i>=17 and i<=20: 
		bucket = 'bucket5'
	elif i>=21 and i<=24: 
		bucket = 'bucket6'
	elif i>=25 and i<=28: 
		bucket = 'bucket7'
	elif i>=29 and i<=32: 
		bucket = 'bucket8'
	num_to_bucket_dict[str(i)] = bucket

for si in all_sentinel_images: 
	image_num = si[si.index('image_')+6:si.index('.jpg')]
	sentinel_img_to_num_dict[si] = image_num

for si in all_sentinel_images: 
	image_num = si[si.index('image_')+6:si.index('.jpg')]
	bucket = num_to_bucket_dict[image_num]
	sentinel_num_to_img_dict[image_num] = sentinel_path + '/' + bucket + '/' + si

for scc in sentinel_codecharts: 
	cc_num = scc[scc.index('chart_')+6:scc.index('.jpg')]
	sentinel_cc_dict[cc_num] = scc

for si in all_sentinel_images: 
	num = sentinel_img_to_num_dict[si]
	scc = sentinel_cc_dict[num]
	bucket = num_to_bucket_dict[num]
	sentinel_dict[sentinel_path + '/' + bucket + '/' + si] = sentinel_codechart_path + '/' + scc

with open('./sentinel_images/sentinel_codes.json') as f:
    sentinel_codes_data = json.load(f)

# Inserting sentinel images at "random" indices (~4-5 images apart) within the subject file 
def index_jitter(): 
	indices = [4, 10, 16, 21] # default to every 5 indices exactly 
	for i in range(len(indices)): 
		jitter = random.choice((-1, 1)) # adds jitter of a jitter away from ideal to add randomness
		indices[i] = indices[i] + jitter
	return indices

for num in range(len(all_buckets)): 
	bucket = all_buckets[num]
	sentinel_bucket = all_sentinel_buckets[num]
	bucket_name = 'bucket' + str(num+1)
	# 1 bucket, 100 sf
	for i in range(num_subject_files): 
		random.shuffle(bucket)
		# 1 sf, 20 real images per
		sf_data = []
		full_sf_data = []
		for j in range(num_images_per_sf): 
			img_count += 1
			image_data = {}
			full_image_data = {}
			image_data["image"] = path + '/' + bucket[j]
			full_image_data["image"] = path + '/' + bucket[j]
			# generate code chart
			filename, valid_codes, coordinates = generate_code.create_codechart('/code_chart_' + str(img_count))
			image_data["codechart"] =  filename
			full_image_data["codechart"] =  filename
			image_data["codes"] = valid_codes
			full_image_data["codes"] = valid_codes
			image_data["flag"] = 'real'
			full_image_data["flag"] = 'real'
			# store locations - (x, y) coordinate of each triplet 
			# 2 different versions of subject files 
			full_image_data["coordinates"] = coordinates
			sf_data.append(image_data)
			full_sf_data.append(full_image_data)

		## ADDING SENTINEL IMAGES 
		sentinel_indices = index_jitter() 
		for index in range(len(sentinel_indices)): 
			sentinel_image_data = {}
			full_sentinel_image_data = {}
			sentinel_file = sentinel_bucket[index]
			file_number = sentinel_file[sentinel_file.index('image_')+6:sentinel_file.index('.jpg')]
			sentinel_image_path = sentinel_num_to_img_dict[file_number]
			sentinel_image_data["image"] = sentinel_image_path
			full_sentinel_image_data["image"] = sentinel_image_path
			sentinel_image_data["codechart"] = sentinel_dict[sentinel_image_path]
			full_sentinel_image_data["codechart"] = sentinel_dict[sentinel_image_path]
			sentinel_image_data["codes"] = sentinel_codes_data[sentinel_image_path][0]
			full_sentinel_image_data["codes"] = sentinel_codes_data[sentinel_image_path][0]
			sentinel_image_data["flag"] = 'sentinel'
			full_sentinel_image_data["flag"] = 'sentinel'
			full_sentinel_image_data["coordinates"] = sentinel_codes_data[sentinel_image_path][1]
			sf_data.insert(sentinel_indices[index], sentinel_image_data)
			full_sf_data.insert(sentinel_indices[index], full_sentinel_image_data)

		with open('./subject_files/' + bucket_name + '/subject_file_' + str(i+1) + '.json', 'w') as outfile: 
			json.dump(sf_data, outfile)
		with open('./full_subject_files/' + bucket_name + '/subject_file_' + str(i+1) + '.json', 'w') as outfile: 
			json.dump(full_sf_data, outfile)

# with open('./subject_files/bucket1.json', 'w') as outfile: 
# 	json.dump(bucket1_data, outfile)

## CODE to remove .DS_Store element that pops up when generating files sometimes 
# for file in sentinel_bucket8: 
# 	print("file: ", file)
# 	if 'image_' not in file: 
# 		print("here")
# 		os.remove(sentinel_path + '/bucket8/' + file)
