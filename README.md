# Happiness Guru  
## A web application  

## Setting Up  

1. Install the dependencies  
`pip install -r requirements.txt`  
there might be a few packages that you might have to install on your own like `fastai` because their sizes are massive for a virtual environment  

2. Place the `sorted_set` folder inside the `dataset` folder in root dir.

3. Regular Django Setup  
	1. `cd happiness`
	2. Migrations  
		`python manage.py makemigrations`  
	3. Migrate  
		`python manage.py migrate`  
	3. Collectstatic  
		`python manage.py collectstatic`  
	4. Running the server  
		`python manage.py runserver`  
		
3. After Initial Setup is done, to run the server  
	`python manage.py runserver`


## Project Structure  
```
|-dataset  
|  |-sorted_set  
|  |  |-happy  
|  |  |-neutral  
|  |  |-sadness  
|  |  |-anger  
|
|-models_dir
|  |- emotion.pth  
|  
|-media  
|  |-test  
|    |-README.md  
|    |-<blob files>
|
|-templates
|  |-base.html
|  |-camera-back.html
|  |-camera.html
|  |-desc_ques.html
|  |-index.html
|  |-mcq_ques.html
|  |-result.html
|
|-HappinessGuru
|  |-settings.py
|  |-urls.py
|  |-wsgi.py
|
|-test
|
|-api
|  |-__init__.py
|  |- admin.py
|  |- apps.py
|  |- forms.py
|  |- models.py
|  |- serializers.py
|  |- tests.py
|  |- urls.py 
|  |- views.py
```

The missing folders are to be added manually.  

## Web Access  
1. Below are the urls  
	HOME PAGE: `http://localhost:8000/`  
	FACE/EMOTION DETECTION: `http://localhost:8000/face`  
	MCQ: `http://localhost:8000/mcq_ques`  
	DESCRIPTIVE: `http://localhost:8000/desc`  

2. APIs  
	PREDICTION API: `http://localhost:8000/api/predict`  
	DESCRIPTIVE: `http://localhost:8000/api/descriptive`


## Further questions  
[Ping Open]  

The `post` methods under `api/Predict` and `api/Descriptive` are the only two methods that need work. 
