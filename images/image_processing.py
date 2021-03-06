# Author: Xinshuo Weng
# email: xinshuo.weng@gmail.com
import numpy as np

from check import *

def imagecoor2cartesian(pts, debug=True):
	'''
	change the coordinate system from image coordinate system to normal cartesian system, basically reverse the y coordinate

	parameter: 
		pts:	a single point (list, tuple, numpy array) or a 2 x N numpy array representing a set of points

	return:
		pts:	a tuple if only single point comes in or a 2 x N numpy array
	'''
	return cartesian2imagecoor(pts, debug=debug)


def cartesian2imagecoor(pts, debug=True):
	'''
	change the coordinate system from normal cartesian system back to image coordinate system, basically reverse the y coordinate
	
	parameter: 
		pts:	a single point (list, tuple, numpy array) or a 2 x N numpy array representing a set of points

	return:
		pts:	a tuple if only single point comes in or a 2 x N numpy array
	'''
	if debug:
		assert is2dpts(pts) or (isnparray(pts) and pts.shape[0] == 2 and pts.shape[1] > 0), 'point is not correct'
	
	if is2dpts(pts):
		if isnparray(pts):
			pts = np.reshape(pts, (2, ))
		return (pts[0], -pts[1])
	else:
		pts[1, :] = -pts[1, :]
		return pts


def imagecoor2cartesian_center(image_shape, debug=True):
	'''
	given an image shape, return 2 functions which change the original image coordinate to centered cartesian coordinate system
	basically the origin is in the center of the image
	
	for example:
		if the image shape is (480, 640) and the top left point is (0, 0), after passing throught forward_map function, it returns (-320, 240)
		for the bottom right point (639, 479), it returns (319, -239)
	'''
	if debug:
		assert (istuple(image_shape) or islist(image_shape) or isnparray(image_shape)) and np.array(image_shape).size == 2, 'input image shape is not correct'

	width = image_shape[1]
	height = image_shape[0]

	def forward_map(pts, debug=True):
		if debug:
			assert is2dpts(pts), 'input 2d point is not correct'
			assert pts[0] >= 0 and pts[0] < width and isinteger(pts[0]), 'x coordinate is out of range %d should in [%d, %d)' % (pts[0], 0, width)
			assert pts[1] >= 0 and pts[1] < height and isinteger(pts[1]), 'y coordinate is out of range %d shoud in [%d, %d)' % (pts[1], 0, height)

		car_pts = imagecoor2cartesian(pts, debug=debug)
		car_pts = np.array(car_pts)
		car_pts[0] += -width/2		# shift x axis half length of width to the right
		car_pts[1] += height/2		# shigt y axis hald length of height downside
		return (car_pts[0], car_pts[1])

	def backward_map(pts, debug=True):
		if debug:
			assert is2dpts(pts), 'input 2d point is not correct'
			assert is2dpts(pts), 'input 2d point is not correct'
			assert pts[0] >= -width/2 and pts[0] < width/2 and isinteger(pts[0]), 'x coordinate is out of range %d should in [%d, %d)' % (pts[0], -width/2, width/2)
			assert pts[1] > -height/2 and pts[1] <= height/2 and isinteger(pts[1]), 'y coordinate is out of range %d shoud in (%d, %d]' % (pts[1], -height/2, height/2)

		pts = np.array(pts)
		pts[0] += width/2		
		pts[1] += -height/2		
		img_pts = cartesian2imagecoor(pts, debug=debug)
		return img_pts
		
	return forward_map, backward_map
