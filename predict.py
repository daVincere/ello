import os
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
import joblib

from fastai.vision import * #importing libraries
from fastai.metrics import error_rate

import nltk



PATH = os.getcwd() +'/dataset/sorted_set' #insert path to sorted set in depression_project_data folder
data  = ImageDataBunch.from_folder(PATH, ds_tfms=get_transforms(), size=244, bs=16, valid_pct=0.3).normalize(imagenet_stats)

learn = cnn_learner(data, models.resnet34, metrics=accuracy)

learn.load(os.getcwd(),'/models/emotion') #loading trained model saved in folder with the name emotion.pth

# In the flask code, you have to first extract the blob from the request, save it as test.jpg and then open it

img = open_image('test/test.png')#insert file name whose class is to be predcited
pred_class,pred_idx,outputs = learn.predict(img)

print ("Emotion recognized", pred_class) 
