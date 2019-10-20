import cv2
import pickle
#from .. import utilities
from os import listdir, makedirs
from os.path import isfile, isdir, join, exists

# Function to perform line segmentation 
# on all document images in given folder
def performLineSegmentation(raw_image_folder, 
	                        output_data_path,
	                        method, is_required = True):

	# If True , line segmentation is not required
	if not is_required:
		print('Line segmentation not required')
		return
	
	lines_image_data = dict()
	
	# line segmentation over all images
	for image_name in listdir(raw_image_folder):
		if isfile(join(raw_image_folder, image_name)) \
				and ('.png' in image_name \
					or '.tif' in image_name \
						or '.jpg' in image_name):

			image = cv2.imread(join(raw_image_folder, image_name))

			# print(image)

			# utilities.img_show(image)

			lines_image_data[image_name] = {
				# 'document_image_data' : image,
				'line_coordinates'    : segmentLines(
										utilities.color2Gray(image),
										method
										),
				}

	file_path = join(output_data_path, 'G:/Project/Line')
	file_name = 'lines.pkl'

	if not exists(file_path):
		makedirs(file_path, exist_ok = True)

	with open(join(file_path, file_name), 'wb') as lines_data_file:
		pickle.dump(lines_image_data, lines_data_file)
		lines_data_file.close()



# Function to generate segmented lines from given image
def segmentLines(image, method = "HORIZONTAL_PROJECTION_PROFILER"):

	original_image = image.copy()

	if method == "HORIZONTAL_PROJECTION_PROFILER":
		coordinates_list = horizontalProjectionProfiler(image)
	else:
		raise Exception('Unknown method ' + method + " given for line segmentation")

	return coordinates_list


###################### LINE SEGMENTATION METHODS #######################


def horizontalProjectionProfiler(image):
		
	# Generating horizontal projection profile
	projection_profile = utilities.getHorizontalProjectionProfile(image)

	# Smoothening signal to detect local peaks
	smoothened_signal  = utilities.getSmoothSignal(projection_profile)

	# Generating vertical boundaries for different lines
	boundary_list      = utilities.getProfileBoundaries(projection_profile)

	# A list of tuples where a tuple contains two tuples
	# representing coordinates of top left corner and bottom 
	# right corner of the bounding box 
	coordinates_list   = []

	for idx, bound in enumerate(boundary_list):
		coordinates_list.append(((bound[0], 0), (bound[1], image.shape[1]-1)))

	return coordinates_list