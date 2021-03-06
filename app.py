from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
from sklearn.feature_extraction.text import CountVectorizer
import pickle 
import pandas as pd



app = Flask(__name__) 
Bootstrap(app)

@app.route('/')
def index():
	return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
	
	data = pd.read_csv('phishing_url.csv')
	df_x = data['URLS']
	df_y = data['Label']
	corpus = df_x
	cv = CountVectorizer()
	x = cv.fit_transform(corpus)
	
	from sklearn.model_selection import train_test_split
	x_train,x_test,y_train,y_test = train_test_split(x,df_y, test_size=0.33)
	from sklearn.naive_bayes import MultinomialNB
	clf = MultinomialNB() 
	clf.fit(x_train,y_train)
	clf.score(x_test,y_test)
	
    

	if request.method == 'POST':
		comment = request.form['comments']
		if comment == '':
			empty = "Blank Page, please fill in a message"
			return render_template('home.html', empty = empty)
		data = [comment]
		vec = cv.transform(data).toarray()
		pred = clf.predict(vec)
	return render_template('home.html', prediction = pred)

	



if __name__=='__main__':
	app.run(debug=True)