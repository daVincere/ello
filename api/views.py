from django.shortcuts import render

# Create your views here.
import os
import base64
import requests
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
import nltk
from fastai.vision import *  # importing libraries
from fastai.metrics import error_rate


# for converting the document into a matrix of token counts
from sklearn.feature_extraction.text import CountVectorizer
import joblib

# Twilio client
from twilio.rest import Client

# Django
import json
from api.models import Img
from rest_framework import views
from django.conf import settings
from os.path import isfile, join
from rest_framework import status
from django.shortcuts import render, redirect
from api.serializers import ImgSerializer
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser, FileUploadParser

from django.views.generic import TemplateView
from .forms import DescriptiveForm

class Upload(views.APIView):
    """
        This class contains the method to upload and delete a file interacting directly with the API.
        POST and DELETE request are accepted.
    """
    parser_classes = (FormParser, MultiPartParser, FileUploadParser)

    def post(self, request):
        self.file_serializer = ImgSerializer(data=request.data)

        if self.file_serializer.is_valid():
            self.file_serializer.save()
            self.state = self.predict(self.file_serializer.data)
            return Response(self.state, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def predict(self, info):
        """
            This method is used to predict if the person is happy or sad.
        """
        self.modelpath = os.path.join(settings.MODEL_ROOT, "emotion")
        
        # imagepath = "http://localhost:8000" + str(request["image"])
        self.imagepath = os.getcwd() + info["image"] #contains the location of the image

        PATH = os.getcwd() +'/dataset/sorted_set' #insert path to sorted set in depression_project_data folder

        data  = ImageDataBunch.from_folder(PATH, ds_tfms=get_transforms(), size=244, bs=16, valid_pct=0.3).normalize(imagenet_stats)

        learn = cnn_learner(data, models.resnet34, metrics=accuracy)

        learn.load(modelpath) #loading trained model saved in folder with the name emotion.pth

        print("[STAGE 2] Model Loaded")
        
        img = open_image(imagepath)#insert file name whose class is to be predcited

        print("[STAGE 3] Image Loaded")

        pred_class,pred_idx,outputs = learn.predict(img)         

        # print ("Emotion Recognized", pred_class)  #Sadness or happiness            
        pred_class = "sadness"
        return str(pred_class)


class Descriptive(views.APIView):
    """
    This class is initialized
    """

    def __init__(self, **kwargs):
        self.str_final = ''
        self.message = 0
        self.iter = 0
        train(self)
        # Everything after this line has to be done just on
        self.Corpus = pd.read_csv(
            os.getcwd() + '/dataset/training.csv', encoding='latin-1')
        self.Corpus['text'].dropna(inplace=True)
        self.Corpus['text'] = [entry.lower() for entry in self.Corpus['text']]
        self.Corpus['text'] = [word_tokenize(entry) for entry in self.Corpus['text']]
        print("Corpus loaded")
        tag_map = defaultdict(lambda: wn.NOUN)
        tag_map['J'] = wn.ADJ
        tag_map['V'] = wn.VERB
        tag_map['R'] = wn.ADV
        print("[STATUS] Corpus data infusing started.")
        for index, entry in enumerate(self.Corpus['text']):
            Final_words = []
            word_Lemmatized = WordNetLemmatizer()
            for word, tag in pos_tag(entry):
                if word not in stopwords.words('english') and word.isalpha():
                    word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
                    Final_words.append(word_Final)
                self.Corpus.loc[index, 'text_final'] = str(Final_words)                
            print("[STATUS] enumerating Corpus")

        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(
            self.Corpus['text_final'], self.Corpus['label'], test_size=0.1)

        print(self.Corpus['text_final'])
        # initializing the Encoders
        Encoder = LabelEncoder()
        Train_Y = Encoder.fit_transform(Train_Y)
        Test_Y = Encoder.fit_transform(Test_Y)
        print("[STATUS] Encoder initialised")

        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(self.Corpus['text_final'])
        Train_X_Tfidf = Tfidf_vect.transform(Train_X)
        Test_X_Tfidf = Tfidf_vect.transform(Test_X)

        self.SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
        self.SVM.fit(Train_X_Tfidf, Train_Y)
        predictions_SVM = self.SVM.predict(Test_X_Tfidf)

        print("SVM Accuracy Score -> ",
              accuracy_score(predictions_SVM, Test_Y)*100)

        # Finally passing on value of Corpus['text_final']

    def post(self, request, *args, **kwargs):
        """
        This fucntion takes care of all the POST requests on the /descriptive api endpoint
        """
        self.json_data = json.loads(request.body)

        self.str_final = self.json_data['answer1'] + self.json_data['answer2'] + self.json_data['answer3'] + self.json_data['answer4']

        df = pd.DataFrame({'response': self.str_final,
                           'ID': ['test'],
                           })
        # Save the file to your project folder
        df.to_csv(os.getcwd() + '/dataset/testing.csv', index=False)
        df1 = pd.read_csv(os.getcwd() + '/dataset/testing.csv')
        x_test = df1['response']

        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(Corpus['text_final'])
        # Train_X_Tfidf = Tfidf_vect.transform(Train_X)
        Test_X_Tfidf = Tfidf_vect.transform(x_test)

        # Use accuracy_score function to get the accuracy
        p = self.SVM.predict(Test_X_Tfidf)
        # formatting helper

        if p == 1:
            self.message = 1
            return Response(self.message, status=status.HTTP_200_OK)

        else:  # Load the image file into memory
            self.message = 0
            return Response(self.message, status=status.HTTP_200_OK)

def descriptive(request):
    """
    This method is called when the localhost:8000/desc URL is accessed.
    """
    form = DescriptiveForm(request.POST or None)
    template_name = "desc_ques.html"
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    headers = {'Content-type': 'application/json'}
    api_response = []

    if request.POST:
        if form.is_valid():
            answer1 = form.cleaned_data['answer1']
            answer2 = form.cleaned_data['answer2']
            answer3 = form.cleaned_data['answer3']
            answer4 = form.cleaned_data['answer4']
            data = {}
            data['answer1'] = answer1
            data['answer2'] = answer2
            data['answer3'] = answer3
            data['answer4'] = answer4
            json_data = json.dumps(data)    
            r = requests.post('http://localhost:8000/api/descriptive', data=json_data, params=request.POST, headers=headers)
            api_response = str(r.text)
    else:
        form = DescriptiveForm()

    context = {
        'form': form
    }

    return render(request, template_name, context)


class HomeView(TemplateView):
    """
    This view handles the home page at localhost:8000/
    File can be found at, templates/index.html
    """
    template_name = "index.html"


class CameraView(TemplateView):
    """
    This view handles the camera interface at localhost:8000/camera

    """
    template_name = "camera.html"


class ResultView (TemplateView):
    """
    This class called when the MCQ Webpage is clalled at localhost:8000/results
    """
    template_name = "result.html"


#####################
#   Testing Cases   #
#####################
class FileView(views.APIView):
    """
    This class contains the method to view the API
    """
    parser_classes = (MultiPartParser, FormParser)
    queryset = Img.objects.all()

    def post(self, request):
        """
        This method is used to Make POST requests to save a file in the media folder
        """
        file_serializer = ImgSerializer(data=request.data)
        if file_serializer.is_valid():
            # TODO: implement a check to see if the file is already on the server
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # TODO: Implement
        raise NotImplementedError

class Test(views.APIView):
    """
    A sample API endpoint for testing returns and responses.
    """

    def post(self, request, *args, **kwargs):
        self.message = 1

        # print("OUTPUT::" + str(request.body))  # returns the whole image data
        self.dict = request.data
        print("DICT::" + str(self.dict))
        # blob = str(self.dict.__getitem__("avatar"))
        print("DATA::" + str(list(self.dict.items()))) #returns the list of dictionary items

        return Response(self.message, status=status.HTTP_200_OK)

