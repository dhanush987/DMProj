
# This document is used to study various factors such as no of train documents, alpha, features vs accuracy on Train and cross Validation 
#sets, This uses a 10 fold stratified cv and uses grid search to implement the pipeline. Also plots various graphs.

import numpy as np
from BuildData import BuildData
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from nltk.tokenize import TreebankWordTokenizer
from sklearn.model_selection import cross_val_score
from sklearn.cross_validation import ShuffleSplit
# from sklearn.grid_search import GridSearchCV
from sklearn.learning_curve import learning_curve
from sklearn.model_selection import GridSearchCV
from matplotlib import pyplot as pl
from matplotlib.backends.backend_pdf import PdfPages
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_blobs
import gc
from sklearn import svm


file_loc='/Users/Dhanush/Desktop/Projects/DM_project/DMProj_Data/Data_train/CODE_'
file_loc_out ='/Users/Dhanush/Desktop/Projects/DM_project/DMProj_Data/Data_Domain_selected/CODE_'

def data_extract_using_parms(Domain_select,write_output,characters_limit,output_loc,features):
	build_data_source =  BuildData(file_loc)
	build_data_source.extract_data_routines()
	data = build_data_source.fetch_train_test_data(Domain_select,write_output,characters_limit,output_loc)
	return data

def Vectorize_split(total_feature_list,total_label,features,binary):
	stop_words = {'english',}
	if features == 'max':
		cv = CountVectorizer(input ='total_feature_list',stop_words = {'english'},lowercase=True,analyzer ='word',binary =binary)#,non_negative=True)#,max_features =75000)
	else:
		cv = CountVectorizer(input ='total_feature_list',stop_words = {'english'},lowercase=True,analyzer ='word',binary =binary,max_features =features)
	X = cv.fit_transform(total_feature_list)#.toarray()
	vocab = np.array(cv.get_feature_names())
	#feature_names = cv.get_feature_names()
	y = (np.array(total_label))
	train_test_data = [i for i in range(5)]
	#X_train, X_test, y_train, y_test = train_test_split(X,y ,test_size=0.2, random_state=5677)
	train_test_data[0] = X
	train_test_data[2] = y
	#train_test_data[0],train_test_data[1],train_test_data[2],train_test_data[3] = train_test_split(X,y ,test_size=0.2, random_state=5677)
	train_test_data[4] = len(vocab)
	return train_test_data
# Main routine, Create an instance of BuildData and call extract_data_routine

def MyMultiNomialNB(X_train, y_train):
	clf = MultinomialNB()
	param_grid = {'alpha': [0.00001,0.0000001] }
	# Ten fold Cross Validation
	classifier= GridSearchCV(estimator=clf, cv=10 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyBernoulliNB(X_train, y_train):
	clf = BernoulliNB()
	param_grid = {'alpha': [0.00001,0.0000001] }
	# Ten fold Cross Validation
	classifier= GridSearchCV(estimator=clf, cv=10 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyGaussianNB(X_train, y_train):
	clf = GaussianNB()
	param_grid = {}
	# Ten fold Cross Validation
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyRandomForest(X_train, y_train):
	clf = RandomForestClassifier()
	param_grid = {'n_estimators': [10,20,30,50,70,100,200,500,1000,2000,2500]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyDecisionTree(X_train, y_train):
	clf = DecisionTreeClassifier(min_samples_split=2,random_state=0)
	param_grid = {'max_depth': [1,5,10,25,50,75,100,500,1000,2000]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyExtraTreeClassifier(X_train, y_train):
	clf = ExtraTreesClassifier(min_samples_split=2, random_state=0,max_depth = 10)
	param_grid = {'n_estimators': [10,20,30,50]}
	#param_grid = {'max_depth': [1,5,10,25,50,75,100,500,1000,2000]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

def MyAdaBoostClassifier(X_train, y_train):
	clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10),learning_rate=0.5)
	param_grid = {'n_estimators': [1000,2000,2500]}
	classifier= GridSearchCV(estimator=clf, cv=3 ,param_grid=param_grid)
	classifier.fit(X_train, y_train)
	return classifier.cv_results_

# main Function
gc.enable()

#Execution Step for Ensemble Method Classifiers
# Use count Vectorizer but with very few samples and number of features < 200.
#Steps For implementation.
#1) Find the Number of features and keep it fixed for each classifier
#2) varying Tuning parameters like Depth and no of estimates
#3) Plot graph for each case
#4) Extremely random classifier needs both parameters to be varied
#5) Do not give too many inputs or features since these will overfit easily.
Domain_select = 1
write_output = 0
characters_limit = 2500
Document_count = []
results_CV_DTC = []
results_train_DTC = []
results_CV_ETC = []
results_train_ETC = []
results_CV_RFC = []
results_train_RFC = []
results_CV_ABC = []
results_train_ABC = []
feature_count = []
features = 'max'
data=data_extract_using_parms(Domain_select,write_output,characters_limit,file_loc_out,features)
total_feature_list = data[0]
total_label = data[1]
features = 170

for i in range(1,2,1):
	print i
	train_test_data=Vectorize_split(total_feature_list,total_label,features,True)
	"""
	results_DTC = MyDecisionTree(train_test_data[0],train_test_data[2])
	results_train_DTC.append(1 - np.mean(results_DTC['mean_train_score']))
	results_CV_DTC.append(1-np.mean(results_DTC['mean_test_score']))
	"""
	#results_ETC = MyExtraTreeClassifier(train_test_data[0],train_test_data[2])
	#results_train_ETC.append(1 - np.mean(results_ETC['mean_train_score']))
	#results_CV_ETC.append(1-np.mean(results_ETC['mean_test_score']))
	#print "Training Random Forest"
	#results_RFC = MyRandomForest(train_test_data[0],train_test_data[2])
	#results_train_RFC.append(1 - np.mean(results_RFC['mean_train_score']))
	#results_CV_RFC.append(1-np.mean(results_RFC['mean_test_score']))
	print "Training Adaboost"
	results_ABC = MyAdaBoostClassifier(train_test_data[0],train_test_data[2])
	#results_train_ABC.append(1 - np.mean(results_ABC['mean_train_score']))
	#results_CV_ABC.append(1-np.mean(results_ABC['mean_test_score']))
	feature_count.append(train_test_data[4])
	Document_count.append((train_test_data[0]).shape[0])
	#features +=10
"""
print "------- Decision Tree Classifier-------------------------------------"
index_max_accuracy = np.argmax(results_DTC['mean_test_score'])
print index_max_accuracy
print "Maximum CV accuracy : "
print results_DTC['mean_test_score']
print "Maximum Train accuracy: " 
print results_DTC['mean_train_score']
depth = [1,5,10,25,50,75,100,500,1000,2000]
print "max_depth" +str(depth[index_max_accuracy])

print "------- Extemely Random Tree Classifier-------------------------------------"
index_max_accuracy = np.argmax(results_ETC['mean_test_score'])	
print "Maximum CV accuracy : "
print results_ETC['mean_test_score']
print "Maximum Train accuracy: " 
print results_ETC['mean_train_score']
estimators = [10,20,30,50]
print "max_estimator" +str(estimators[index_max_accuracy])

print "------- RandomForestClassifier-------------------------------------"
index_max_accuracy = np.argmax(results_RFC['mean_test_score'])
print "Maximum CV accuracy : "
print results_RFC['mean_test_score']
print "Maximum Train accuracy: " 
print results_RFC['mean_train_score']
estimators = [10,20,30,50,70,100,200,500,1000,2000,2500]
print "max_estimator" +str(estimators[index_max_accuracy])

"""
print "------- AdaBoostClassifier-------------------------------------"
index_max_accuracy = np.argmax(results_ABC['mean_test_score'])	
print "Maximum CV accuracy : "
print results_ABC['mean_test_score']
print "Maximum Train accuracy: " 
print results_ABC['mean_train_score']
estimators = [10,20,30,50,70,100,200,500,1000,2000,2500]
print "max_estimator" +str(estimators[index_max_accuracy])

"""
with PdfPages('Decision_Tree_Depth_vs_Accuracy_study.pdf') as pdf:
    pl.plot([1,5,10,25,50,75,100,500,1000,2000],results_DTC['mean_train_score'],marker='.',markersize = 13.0,linewidth=2, linestyle='-', color='m',label ='Train Score')
    pl.plot([1,5,10,25,50,75,100,500,1000,2000],results_DTC['mean_test_score'],marker='.',markersize = 13.0,linewidth=1, linestyle='-', color='b',label ='CV Score')
    pl.ylabel('Classification Accuracy',color='r')
    pl.xlabel('Depth of Tree',color='r')
    pl.title('Decision Tree - Accuracy Vs Depth of tree using CountVectorizer',color = 'r')
    pl.legend(bbox_to_anchor=(0.69, 0.27), loc=2, borderaxespad=0.)
    pdf.savefig()
    pl.close()

with PdfPages('Random_forests_No_of_estimators_vs_Accuracy_study.pdf') as pdf:
    pl.plot([10,20,30,50,70,100,200,500,1000,2000,2500],results_RFC['mean_train_score'],marker='.',markersize = 13.0,linewidth=2, linestyle='-', color='m',label ='Train Score')
    pl.plot([10,20,30,50,70,100,200,500,1000,2000,2500],results_RFC['mean_test_score'],marker='.',markersize = 13.0,linewidth=1, linestyle='-', color='b',label ='CV Score')
    pl.ylabel('Classification Accuracy',color='r')
    pl.xlabel('Number Of Estimators',color='r')
    pl.title('Random_forests - Accuracy Vs # of estimator for train using CountVectorizer',color = 'r')
    pl.legend(bbox_to_anchor=(0.69, 0.27), loc=2, borderaxespad=0.)
    pdf.savefig()
    pl.close()

with PdfPages('extremely Random Tree__estimators_vs_Accuracy_study.pdf') as pdf:
    pl.plot([1,5,10,25,50],results_ETC['mean_train_score'],marker='.',markersize = 13.0,linewidth=2, linestyle='-', color='m',label ='Train Score')
    pl.plot([1,5,10,25,50],results_ETC['mean_test_score'],marker='.',markersize = 13.0,linewidth=1, linestyle='-', color='b',label ='CV Score')
    pl.ylabel('Classification Accuracy',color='r')
    pl.xlabel('Number Of estimators for Training',color='r')
    pl.title('Extree Random_Tree - Accuracy Vs # estimators for train using CountVectorizer',color = 'r')
    pl.legend(bbox_to_anchor=(0.69, 0.27), loc=2, borderaxespad=0.)
    pdf.savefig()
    pl.close()

with PdfPages('AdaBoost_No_of_estimators_vs_Accuracy_study.pdf') as pdf:
    pl.plot([10,20,30,50,70,100,200,500,1000,2000,2500],results_ABC['mean_train_score'],marker='.',markersize = 13.0,linewidth=2, linestyle='-', color='m',label ='Train Score')
    pl.plot([10,20,30,50,70,100,200,500,1000,2000,2500],results_ABC['mean_test_score'],marker='.',markersize = 13.0,linewidth=1, linestyle='-', color='b',label ='CV Score')
    pl.ylabel('Classification Accuracy',color='r')
    pl.xlabel('Number Of estimators for Training',color='r')
    pl.title('Adaboost - Accuracy Vs # of estimators for train using CountVectorizer',color = 'r')
    pl.legend(bbox_to_anchor=(0.69, 0.27), loc=2, borderaxespad=0.)
    pdf.savefig()
    pl.close()

"""



