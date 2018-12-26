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

random.shuffle(files) # shuffle all images randomly at start 

sentinel_path = './sentinel_images'
sentinel_codechart_path = './codecharts/sentinel'
sentinel_codecharts = os.listdir(sentinel_codechart_path)

all_buckets = []
img_count = 0 # keeps track of the number of codecharts being produced 
num_buckets = 8
num_subject_files = 1 # 100 subject files/ bucket
num_images_per_sf = 20 # 20 images/ subject file
num_tutorials_per_sf = 3 # 3 tutorials/ subject file
num_imgs_per_tutorial = 3 # 2 images/ tutorial 
images_per_bucket = int(len(files)/num_buckets)
for i in range(0, len(files), images_per_bucket): 
	all_buckets.append(files[i:i+images_per_bucket])

# Images corresponding to each bucket
bucket1 = all_buckets[0]
bucket2 = all_buckets[1]
bucket3 = all_buckets[2]
bucket4 = all_buckets[3]
bucket5 = all_buckets[4]
bucket6 = all_buckets[5]
bucket7 = all_buckets[6]
bucket8 = all_buckets[7]

# Sentinel images corresponding to each bucket 
sentinel_bucket1 = os.listdir('./sentinel_images/bucket1')
sentinel_bucket2 = os.listdir('./sentinel_images/bucket2')
sentinel_bucket3 = os.listdir('./sentinel_images/bucket3')
sentinel_bucket4 = os.listdir('./sentinel_images/bucket4')
sentinel_bucket5 = os.listdir('./sentinel_images/bucket5')
sentinel_bucket6 = os.listdir('./sentinel_images/bucket6')
sentinel_bucket7 = os.listdir('./sentinel_images/bucket7')
sentinel_bucket8 = os.listdir('./sentinel_images/bucket8')
all_sentinel_buckets = [sentinel_bucket1, sentinel_bucket2, sentinel_bucket3, sentinel_bucket4, sentinel_bucket5, sentinel_bucket6, sentinel_bucket7, sentinel_bucket8]

# Dictionaries to help keep mappings between images + codecharts for sentinel images organized
sentinel_img_to_num_dict = {} # maps image to its number {"img_path: 4"}
sentinel_num_to_img_dict = {} # maps number to its image {"4: img_path"}
sentinel_cc_dict = {} # maps number to codechart {"4: codechart_path"}
sentinel_dict = {} # maps image to its codechart {"img_path: codechart_path"}
num_to_bucket_dict = {} # maps each number to its bucket {"1: bucket1...4: bucket1, 5: bucket2,..."}

all_sentinel_images = [] # a list of lists (all sentinel buckets as elements)
all_sentinel_images.extend(sentinel_bucket1)
all_sentinel_images.extend(sentinel_bucket2)
all_sentinel_images.extend(sentinel_bucket3)
all_sentinel_images.extend(sentinel_bucket4)
all_sentinel_images.extend(sentinel_bucket5)
all_sentinel_images.extend(sentinel_bucket6)
all_sentinel_images.extend(sentinel_bucket7)
all_sentinel_images.extend(sentinel_bucket8)

# assigns each number to its bucket (32 sentinel images total)
for i in range(1, 33): 
	bucket = ''
	if i>=1 and i<=4: # sentinel images 1-4 correspond to bucket1
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

# loads the valid codes for the sentinel images 
with open('./sentinel_images/sentinel_codes.json') as f:
    sentinel_codes_data = json.load(f) # contains mapping of sentinel image path to (valid triplet code, coordinate of valid triplet code)

with open('./tutorials/tutorial.json') as f:
    tutorial_data = json.load(f) # contains mapping of sentinel image path to (valid triplet code, coordinate of valid triplet code)

# Inserting sentinel images at "random" indices (~4-5 images apart) within the subject file 
def index_jitter(): 
	indices = [4, 10, 16, 23] # default to every 5 indices exactly
	for i in range(len(indices)): 
		jitter = random.choice((-1, 1)) # adds jitter of a jitter away from ideal to add randomness
		indices[i] = indices[i] + jitter
	return indices


## GENERATING SUBJECT FILES 
# iterate over all buckets 
for num in range(num_buckets): 
	bucket = all_buckets[num]
	sentinel_bucket = all_sentinel_buckets[num]
	bucket_name = 'bucket' + str(num+1)
	# for each bucket, generate 100 subject files 
	for i in range(num_subject_files): 
		random.shuffle(bucket)
		# for each subject files, add 20 real images 
		sf_data = []
		full_sf_data = []

		# ADDING TUTORIALS
		# randomly choose 3 tutorials to include with each subject file
		forbidden_numbers = set() 
		for y in range(num_tutorials_per_sf): 
			r = list(range(0, 9))
			choice = random.choice(r)
			while choice in forbidden_numbers:
				choice = random.choice(r)
			forbidden_numbers.add(choice)

		for t in forbidden_numbers: 
			for img in tutorial_data[t]: 
				smaller_img_dict = img.copy()
				del smaller_img_dict['coordinates']
				sf_data.append(smaller_img_dict)
				full_sf_data.append(img)

		# ADDING REAL IMAGES 
		for j in range(num_images_per_sf): 
			img_count += 1
			image_data = {}
			full_image_data = {} # identical to image_data but includes a key for coordinates
			image_data["image"] = path + '/' + bucket[j] # stores image path 
			full_image_data["image"] = path + '/' + bucket[j]
			# generate code chart
			filename, valid_codes, coordinates = generate_code.create_codechart('/code_chart_' + str(img_count))
			image_data["codechart"] =  filename # stores codechart path 
			full_image_data["codechart"] =  filename
			image_data["codes"] = valid_codes # stores valid codes 
			full_image_data["codes"] = valid_codes
			image_data["flag"] = 'real' # stores flag of whether we have real or sentinel image
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
			full_sentinel_image_data = {} # identical to sentinel_image_data but includes coordinate key 
			sentinel_file = sentinel_bucket[index]
			file_number = sentinel_file[sentinel_file.index('image_')+6:sentinel_file.index('.jpg')] # extracts which sentinel image we're dealing with (i.e. image1, image2, image3...)
			sentinel_image_path = sentinel_num_to_img_dict[file_number]
			sentinel_image_data["image"] = sentinel_image_path # stores image path 
			full_sentinel_image_data["image"] = sentinel_image_path
			sentinel_image_data["codechart"] = sentinel_dict[sentinel_image_path] # stores codechart path 
			full_sentinel_image_data["codechart"] = sentinel_dict[sentinel_image_path]
			sentinel_image_data["correct_code"] = sentinel_codes_data[sentinel_image_path][0] # stores the valid code that must be entered for sentinel image
			full_sentinel_image_data["correct_code"] = sentinel_codes_data[sentinel_image_path][0]
			sentinel_image_data["valid_codes"] = sentinel_codes_data[sentinel_image_path][2]
			full_sentinel_image_data["valid_codes"] = sentinel_codes_data[sentinel_image_path][2]
			sentinel_image_data["flag"] = 'sentinel' # stores flag of whether we have real or sentinel image
			full_sentinel_image_data["flag"] = 'sentinel'
			full_sentinel_image_data["coordinates"] = sentinel_codes_data[sentinel_image_path][1] # stores the coordinate of the valid code 
			sf_data.insert(sentinel_indices[index], sentinel_image_data)
			full_sf_data.insert(sentinel_indices[index], full_sentinel_image_data)

		# Add an image_id to each entry
		image_id = 0 # represents the index of the image in the subject file 
		for d in range(len(sf_data)): 
			sf_data[d]['index'] = image_id+1 # NOT zero-indexed
			full_sf_data[d]['index'] = image_id+1
			image_id+=1

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
