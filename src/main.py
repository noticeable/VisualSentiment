import sys
import os
import cv2
import sklearn
import numpy as np
sys.path.insert(0, './util')

from FaceExtractor import FaceExtractor
from EmotionExtractor import EmotionExtractor
from sklearn import svm
from sklearn.decomposition import PCA


def main():
	## Face Extraction ## 
	# img_path = "../data/groupdataset_release/images/Library3.jpg"
	# face_extractor = FaceExtractor()
	# faces_lists, image = face_extractor.detect_faces(img_path)
	# for face_list in faces_lists: 
	# 	for (x,y,w,h) in face_list: 

	img_path = "../data/GENKI-R2009a/Subsets/GENKI-4K/GENKI-4K_Images.txt"
	labels_path = "../data/GENKI-R2009a/Subsets/GENKI-4K/GENKI-4K_Labels.txt"
	train_smile_extractor(img_path, labels_path)

# Given an image path and a classifier (svm), this method returns a list of 
# image coordinates of faces, a matrix of smile features and the classifier's
# predictions for each face.
def predict_smiles(img_path, classifier):
	face_extractor = FaceExtractor()
	faces_list, im = face_extractor.detect_faces(img_path)
	faces = face_extractor.get_scaled_faces(faces_list, im)
	n_faces = len(faces_list)

	emotion_extractor = EmotionExtractor()
	smile_features = np.zeros((n_faces, emotion_extractor.NUM_FEATURES))
	for i, face in enumerate(faces_list):
		emotion_extractor.set_face(face)
		feature_vec = emotion_extractor.extract_smile_features()
		smile_features[i,:] = feature_vec

	predictions = classifier.predict(smile_features)

	return faces_list, smile_features, predictions


def train_smile_extractor(img_path, labels_path): 
	#read in stuff 
	img_base_path = "../data/GENKI-R2009a/Subsets/GENKI-4K/files"
	images_file = open(img_path, 'r')
	filenames = []
	
	filenames = images_file.readlines()
	filenames = [os.path.join(img_base_path, filename.strip()) for filename in filenames]

	print filenames


	labels_file = open(labels_path, 'r')
	lines = labels_file.readlines()
	labels = []
	for line in lines: 
		labels.append(int(line.split()[0]))

	#setup 
	emotion_extractor = EmotionExtractor()
	
	X = np.zeros((len(filenames), emotion_extractor.NUM_FEATURES))
	y = np.array(labels)

	print X.shape

	for i, img_name in enumerate(filenames): 
		face_image = cv2.imread(img_name)
		emotion_extractor.set_face(face_image)
		X[i,:] = emotion_extractor.extract_smile_features()

	pca = PCA()
	X_new = pca.fit_transform(X)

	print X_new.shape

	# X_train, X_test, Y_train, Y_test = sklearn.cross_validation.train_test_split(X, y, test_size=0.2)

	# run SVM








if __name__ == '__main__':
	main()
