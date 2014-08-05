from model_feature_creator import create_feature_vector
from model_feature_creator import create_feature_matrix
from model_feature_creator import feature_vector_meaning

from sklearn import metrics
from sklearn import preprocessing
from sklearn import cross_validation
from sklearn.svm import SVC
import sklearn.linear_model as lm

import numpy as np

# Classifiers
def direction_classifier(x,y):
	clf = SVC()
	clf.fit(x,y)

	return clf 

def change_classifier(x,y):
	clf = lm.LinearRegression()
	clf.fit(x,y)

	return clf 

# Experiments
def experiment_zero(data,company):
	print '___Experiment One___'
	# Experiment Parameters
	finance_datatype = 0    # finance_datatype: Integer 2 = Stock price change, 1 = Percentage stock price change, 0 = Only direction
	finance_n = 2           # finance_n: Integer >=0 Number of days of finance data to include
	sentiment_datatype = 1	# sentiment_datatype: Boolean 1 = all sentiment featues, 0 = Total
	sentiment_n = 1 		# sentiment_n: Integer >=0 Number of days of sentiment data to include
	day = 0                 # day: Boolean 1 = Include day of the week, 0 = do not
	target = 0				# target: Boolean 1 = Amount, 0 = Direction
	volume = 0 				# volume: boolean 1 = Yes, 0 = No
	if (finance_n + sentiment_n + day + volume) == 0:
		print 'Insufficient parameters set'
		return 

	# Data Processing
	feature_vector_meaning(company, finance_datatype, finance_n, sentiment_datatype, sentiment_n, day, target, volume)
	matrix = create_feature_matrix(company, data, finance_datatype, finance_n, sentiment_datatype, sentiment_n, day, target, volume)
	end = len(matrix[0])
	train_x = matrix[:,0:end-1]
	train_y = matrix[:,end-1]

	# Classifier training
	scaler = preprocessing.StandardScaler().fit(train_x)
	train_x = scaler.transform(train_x)

	clf = direction_classifier(train_x,train_y)
	cv = cross_validation.ShuffleSplit(len(train_x), n_iter=5, test_size=0.2, random_state=0)
	print ' _ _ _Evaluation_ _ _'
	if target == 0:
		scores = cross_validation.cross_val_score(clf, train_x, train_y, cv=cv, scoring='accuracy')
		print("  Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
	elif target == 1:
		scores = cross_validation.cross_val_score(clf, train_x, train_y, cv=cv, scoring='mean_squared_error')
		print("  MSE: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))		
	print '====================='

# Read Data
def read_data(filename):
	ignore_start = True
	matrix = []
	with open(filename) as f:
		for line in f.readlines():
			line = line.replace('\n','')
			if ignore_start == False:
				matrix.append(line.split('\t'))
			else:
				ignore_start = False

	return matrix

if __name__ == '__main__':
	print 'Running Model.py - Creates classifiers and runs experiments'
	print '====================='
	mcdonalds = read_data('./../output/mcdonalds_daily.txt')
	jpmorgan = read_data('./../output/jpmorgan_daily.txt')
	# microsoft = read_data('./../output/microsoft_daily.txt')

	experiment_zero(jpmorgan, 'jpmorgan')
	experiment_zero(mcdonalds, 'mcdonalds')
	# experiment_one(microsoft, 'microsoft')