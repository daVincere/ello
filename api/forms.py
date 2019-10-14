from django import forms

class DescriptiveForm(forms.Form):
	answer1 = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
											'placeholder':'How have you been feeling these days?',
											'rows' : '5', 'cols' : '100', 
											}))
	answer2 = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
											'placeholder':'What are your plans for the future? What according to you would you be doing in next 5-7 years?', 
											'rows' : '5', 'cols' : '100', 
											}))
	answer3 = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
											'placeholder':'Describe a situation where you would feel uneasy/uncomfortable', 
											'rows' : '5', 'cols' : '100', 
											}))
	answer4 = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={
											'placeholder':'If you had all the power, where would you use it?', 
											'rows' : '5', 'cols' : '100', 
											}))