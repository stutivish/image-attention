import os 
import glob
import random
import json

# real_path = './tutorials/tutorial_real_images'
# sentinel_path = './tutorials/tutorial_sentinel_images'
# add_to_path = './tutorials/tutorial'

# real_files = os.listdir(real_path)
# sentinel_files = os.listdir(sentinel_path)

# random.shuffle(real_files)
# random.shuffle(sentinel_files)

# loads the valid codes for the sentinel images 
with open('./subject_files/bucket1/subject_file_1.json') as f:
    data = json.load(f) # contains mapping of sentinel image path to (valid triplet code, coordinate of valid triplet code)

# random.shuffle(tutorial_data)

print(len(data))


# count = 1
# for subdir in subdirs: 
# 	print('subdir: ', subdirs)
# 	subpath = path + '/' + subdir
# 	print('subpath: ', subpath)
# 	for filename in os.listdir(subpath): 
# 		os.rename(subpath + '/' + filename, "./all_images/image_" + str(count) + ".jpg")
# 		count+=1 



