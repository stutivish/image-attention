import os 
import glob
import random

path = './all_images'

files = os.listdir(path)

random.shuffle(files)

# count = 1
# for subdir in subdirs: 
# 	print('subdir: ', subdirs)
# 	subpath = path + '/' + subdir
# 	print('subpath: ', subpath)
# 	for filename in os.listdir(subpath): 
# 		os.rename(subpath + '/' + filename, "./all_images/image_" + str(count) + ".jpg")
# 		count+=1 



