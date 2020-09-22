from imutils import paths
import argparse
import requests
import cv2
import os
import urllib3
urllib3.disable_warnings()
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
	help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())
 
# grab the list of URLs from the input file, then initialize the
# total number of images downloaded thus far

full = open(args["urls"],'r', encoding='UTF-8').read().strip().split("\n")
#rows = open(args["urls"]).read().strip().split("\n")
total = 0
p="empty"
# loop the URLs
for url in full:
	try:
		# try to download the image
		name = url.split(" ")  
		#print(name[1])
		r = requests.get(name[1], timeout=60,verify=False)
 
		# save the image to disk
		p = os.path.sep.join([args["output"], "{}.jpg".format(
			str(name[0]))])
		f = open(p, "wb")
		f.write(r.content)
		f.close()
 
		# update the counter
		print("[INFO] downloaded: {}".format(p))
		total += 1
 
	# handle if any exceptions are thrown during the download process
	except:
		print("[INFO] error downloading {}...skipping".format(p))

# loop over the image paths we just downloaded
for imagePath in paths.list_images(args["output"]):
	# initialize if the image should be deleted or not
	delete = False
 
	# try to load the image
	try:
		image = cv2.imread(imagePath)
 
		# if the image is `None` then we could not properly load it
		# from disk, so delete it
		if image is None:
			delete = True
 
	# if OpenCV cannot load the image then the image is likely
	# corrupt so we should delete it
	except:
		print("Except")
		delete = True
 
	# check to see if the image should be deleted
	if delete:
		print("[INFO] deleting {}".format(imagePath))
		os.remove(imagePath)
