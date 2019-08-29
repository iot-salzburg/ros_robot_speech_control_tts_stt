from sklearn import svm
from random import shuffle
import tensorflow as tf
import math
import csv
import pickle
import numpy as np
from joblib import dump, load

listFeatures = []

with open('MFCCEnglish.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		listFeatures.append(row)

with open('MFCCGerman.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		listFeatures.append(row)

shuffle(listFeatures)

trainSetPercentage = 0.8
trainSetAmount = math.trunc(len(listFeatures) * trainSetPercentage)

train_data = listFeatures[:trainSetAmount]
test_data = listFeatures[trainSetAmount:]

x_train = []
y_train = []
x_test = []
y_test = []

for row in train_data:
	lastValueIndex = len(row)-1
	x_train.append(row[:lastValueIndex])
	y_train.append(row[lastValueIndex:])

for row in test_data:
	lastValueIndex = len(row)-1
	x_test.append(row[:lastValueIndex])
	y_test.append(row[lastValueIndex:])

clf = svm.SVC(gamma='scale')

x_train_train = []
y_train_train = []
x_test_test = []
y_test_test = []

for x in x_train:
	x_float = []
	for i in x:
		x_float.append(float(i))
	x_train_train.append(x_float)

for x in x_test:
	x_float = []
	for i in x:
		x_float.append(float(i))
	x_test_test.append(x_float)

for y in y_train:
	for i in y:
		y_train_train.append(float(i))

for y in y_test:
	for i in y:
		y_test_test.append(float(i))

clf.fit(x_train_train, y_train)

for x in x_test_test: 
	x = np.reshape(x, (1, -1))
	print(clf.predict(x))

dump(clf, 'saved_SVM_Model.joblib')

#model = tf.keras.models.Sequential()
#model.add(layers.Conv2D())

#model.compile(optimizer='adam',
#              loss='sparse_categorical_crossentropy',
#              metrics=['accuracy'])

#model.fit(x_train, y_train, epochs=5)
#model.evaluate(x_test, y_test)

