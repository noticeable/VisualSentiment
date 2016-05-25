import numpy as np
import cv2
import os
import scipy.io as io

from feature_extractors import *

NORMALIZED_SIZE = 64
NUM_GAUSSIANS = 5

class EmotionExtractor: 
	

	def __init__(self): 
		self.face = None


	def set_face(self, face_image):
		self.face = face_image


	def extract_smile(self):
		#read in the image 
		gray_img = cv2.cvtColor(self.face, cv2.COLOR_RGB2GRAY)

		#normalize to 64x64; precondition: make sure that face patches are square!!
		gray_img_resize = cv2.resize(gray_img, (NORMALIZED_SIZE, NORMALIZED_SIZE))

		#subdivide into 4x4 cells 

		pixel_derivs = np.zeros((NORMALIZED_SIZE, NORMALIZED_SIZE, NUM_GAUSSIANS))
		for i in xrange(NORMALIZED_SIZE):
			for k in xrange(NORMALIZED_SIZE): 
				#calculate derivatives 
				deriv_vec = np.zeros((NUM_GAUSSIANS,))

				if i != 0 and i != NORMALIZED_SIZE - 1: 
					deriv_vec[1] = gray_img_resize[i+1,k] - gray_img_resize[i-1,k]
					deriv_vec[3] = gray_img_resize[i+1,k] - 2 * gray_img_resize[i,k] + gray_img_resize[i-1,k]
				else: 
					deriv_vec[1] = -1
					deriv_vec[3] = -1

				if k != 0 and k != NORMALIZED_SIZE - 1: 
					deriv_vec[0] = gray_img_resize[i,k+1] - gray_img_resize[i,k-1]
					deriv_vec[2] = gray_img_resize[i,k+1] - 2 * gray_img_resize[i,k] + gray_img_resize[i,k-1]					
				else: 
					deriv_vec[0] = -1 
					deriv_vec[2] = -1

				if i != 0 and i != NORMALIZED_SIZE - 1 and k != 0 \
					and k != NORMALIZED_SIZE - 1: 
					deriv_vec[4] = gray_img_resize[i+1,k+1] - gray_img_resize[i-1,k+1] - gray_img_resize[i+1,k-1] + gray_img_resize[i-1,k-1]
				else: 
					deriv_vec[4] = -1

				pixel_derivs[i,k] = deriv_vec


		print pixel_derivs[30,30,:]
