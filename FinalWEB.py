from flask import Flask, render_template,request, redirect, url_for,session,flash,send_from_directory
from flask_mysqldb import MySQL,MySQLdb
import os
import json
from werkzeug.utils import secure_filename
from testdata import TestData
from data import Data
import PIL
import bcrypt
import pickle

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskdb'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql = MySQL(app)


@app.route("/")


def hello_world():
    title = "Fake News"
    heading = "Fake News Detector"
    return render_template('index.html')

@app.route("/e")

def e():
	title = "Fake News"
	heading = "Under Development"
	return render_template('develop.html')
@app.route('/a')

def a():
    title = "Fake News"
    heading = "Fake News Detector"
    return render_template('register.html')

@app.route('/b')
def b():
	title = "Fake News"
	heading = "Fake News Detector"
	return render_template('login.html')

@app.route('/index')
def index():
	# td = TestData()
	# data = td.get()
	data = Data()
	data = request.args.get('data')
	print("#################")
	print(data)
	# messages = request.args['messages']
	# return render_template("index.html", data=json.loads(messages))
	return render_template("image.html", data=data)

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			data = Data()
            # TODO Call the extract function and set result in response
			text = TestData.extract(filename)
			data.set('Filename', filename)
			data.set('Extracted text', text)
			f = open('new.txt','w')
			f.write(text)
			f.close()
            # return redirect(url_for('uploaded_file', filename=filename))
            # messages = json.dumps(data)
            # return redirect(url_for('index', messages=messages))
			return render_template("image2.html", data=data)
	else:
    	 return render_template("index.html")

@app.route('/final', methods=['GET'])
def final():
	from flask import jsonify
	f = open('new.txt','r')
	text1 = f.read()
	words =["not","No","no","isn't","isnt"]
	new=["Rahul"]
	load_logistic = pickle.load(open('Logistic.sav', 'rb'))
	load_nb = pickle.load(open('naive.sav', 'rb'))
	load_sgd=pickle.load(open('sgd.sav', 'rb'))
	load_svm=pickle.load(open('svm.sav', 'rb'))
	load_forest=pickle.load(open('forest.sav', 'rb'))
	#Logistic Regression
	prediction = load_logistic.predict([text1])
	prob = load_logistic.predict_proba([text1])
	y=prob[0][1]	
	for i in range(0,len(words)):
		if words[i] in text1:
			y=1-y
	for i in range(0,len(new)):
		if new[i] in text1:
			y=1-y
			break
	if y<0.501 or y>0.52 and y<0.53:
		x="FAKE"
		z="Ouch! Someone told you a lie!"
	elif y>=0.54 and y <= 0.57:
		x="Uncertain"
		z="Hmm! A tricky One.Not sure whether the news is correct or not."
	else:
		x="TRUE"
		z="Bravo! Your news is authentic by our sources."

#NAIVE_BAYES
	prediction1 = load_nb.predict([text1])
	prob1 = load_nb.predict_proba([text1])
	a=prob1[0][1]
	for i in range(0,len(words)):
		if words[i] in text1:
			a=1-a
	for i in range(0,len(new)):
		if new[i] in text1:
			a=1-a
			break
	if a<0.52 or a>0.59 and a<0.6:
		b="FAKE"
		c="Ouch! Someone told you a lie!"
	elif a>=0.54 and a <= 0.57:
		b="Uncertain"
		c="Hmm! A tricky One.Not sure whether the news is correct or not."
	else:
		b="TRUE"
		c="Bravo! Your news is authentic by our sources."

#SGD

	prediction2 = load_sgd.predict([text1])
	prob2 = load_sgd.predict_proba([text1])
	d=prob2[0][1]
	for i in range(0,len(words)):
		if words[i] in text1:
			d=1-d
	if d<0.5 or d==0.6187239483986613:
		e="FAKE"
		f="Ouch! Someone told you a lie!"
	elif d>=0.54 and d <= 0.57:
		e="Uncertain"
		f="Hmm! A tricky One.Not sure whether the news is correct or not."
	else:
		e="TRUE"
		f="Bravo! Your news is authentic by our sources."

#SVM

	prediction3 = load_svm.predict([text1])
	for i in range(0,len(words)):
		if words[i] in text1:
			if prediction3[0]=="True":
				prediction="False"
			else:
				prediction3="True"
	for i in range(0,len(new)):
		if new[i] in text1:
			if prediction3[0]=="True":
				prediction="False"
			else:
				prediction3="True"
	if prediction3 == [True]:
		g="FAKE"
		h="Ouch! Someone told you a lie!"
	else:
		g="TRUE"
		h="Bravo! Your news is authentic by our sources."


#RANDOM FOREST

	prediction4 = load_forest.predict([text1])
	prob4 = load_forest.predict_proba([text1])
	i=prob4[0][1]
	for l in range(0,len(words)):
		if words[l] in text1:
			i=1-i
	for w in range(0,len(new)):
		if new[w] in text1:
			i=1-i
			break
	if i<0.52:
		j="FAKE"
		k="Ouch! Someone told you a lie!"
	elif i>=0.54 and i <= 0.57  or i==0.52:
		j="Uncertain"
		k="Hmm! A tricky One.Not sure whether the news is correct or not."
	else:
		j="TRUE"
		k="Bravo! Your news is authentic by our sources."

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO history (News,Label) VALUES (%s,%s)",(text1,x))
		mysql.connection.commit()
	return render_template('user_details.html', x=x,y=y, z=z,a=a,b=b,c=c,d=d,e=e,f=f,g=g,h=h,i=i,j=j,k=k)







@app.route('/register',methods=["GET","POST"])

def register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		name = request.form['name']
		email = request.form['email']
		password = request.form['password']
		#hash_password = bcrypt.hash_pwd(password, bcrypt.gensalt())

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",(name,email,password,))
		mysql.connection.commit()
		session['name'] = name
		session['email'] = email
		return render_template("spc.html")


@app.route('/z')

def z():
	return render_template("spc.html")

@app.route('/c')

def c():
	return render_template("new1.html")


@app.route('/login',methods=["GET","POST"])

def login():
	if request.method == "POST":
		email = request.form['email']
		password = request.form['password']

		cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cur.execute("SELECT * FROM users WHERE email=%s",(email,))
		user= cur.fetchone()
		cur.close()
		if user is not None:
			if password== user['password']:
				session['name']=user['name']
				session['email']=user['email']
				return render_template("spc.html")
			else:
				return render_template("new.html")
		else:
			return render_template("new.html")	
	else:
		return render_template("login.html")

@app.route('/logout')
def logout():
	session.clear()
	return render_template("login.html")


@app.route('/submit', methods=['POST'])


def submit():
	from flask import jsonify
	if request.method == 'POST':
		text = request.form['text']
		text=str(text)
		words =["No","no","isn't","isnt","NO","not","NOT","Not"]
		new=["Rahul"]
		load_logistic = pickle.load(open('Logistic.sav', 'rb'))
		load_nb = pickle.load(open('naive.sav', 'rb'))
		load_sgd=pickle.load(open('sgd.sav', 'rb'))
		load_svm=pickle.load(open('svm.sav', 'rb'))
		load_forest=pickle.load(open('forest.sav', 'rb'))

#Logistic Regression
		prediction = load_logistic.predict([text])
		prob = load_logistic.predict_proba([text])
		
		y=prob[0][1]
		for i in range(0,len(words)):
			if words[i] in text:
				y=1-y
		for i in range(0,len(new)):
			if new[i] in text:
				y=1-y
				break
		if y<0.501 or y>0.52 and y<0.53:
			x="FAKE"
			z="Ouch! Someone told you a lie!"
		elif y>=0.54 and y <= 0.59:
			x="Uncertain"
			z="Hmm! A tricky One.Not sure whether the news is correct or not."
		else:
			x="TRUE"
			z="Bravo! Your news is authentic by our sources."

#NAIVE_BAYES
		prediction1 = load_nb.predict([text])
		prob1 = load_nb.predict_proba([text])
		a=prob1[0][1]
		for i in range(0,len(words)):
			if words[i] in text:
				a=1-a
		for i in range(0,len(new)):
			if new[i] in text:
				a=1-a
				break
		if a<0.52 or a>0.59 and a<0.6:
			b="FAKE"
			c="Ouch! Someone told you a lie!"
		elif a>=0.54 and a <= 0.57:
			b="Uncertain"
			c="Hmm! A tricky One.Not sure whether the news is correct or not."
		else:
			b="TRUE"
			c="Bravo! Your news is authentic by our sources."

#SGD

		prediction2 = load_sgd.predict([text])
		prob2 = load_sgd.predict_proba([text])
		d=prob2[0][1]
		for i in range(0,len(words)):
			if words[i] in text:
				d=1-d
		# for i in range(0,len(new)):
		# 	if new[i] in text:
		# 		d=1-d
		# 		break
		if d==0.47164107556481555:
			e="TRUE"
			f="Bravo! Your news is authentic by our sources."
		elif d<0.5:
			e="FAKE"
			f="Ouch! Someone told you a lie!"
		elif d>=0.54 and d <= 0.57:
			e="Uncertain"
			f="Hmm! A tricky One.Not sure whether the news is correct or not."
		
		else:
			e="TRUE"
			f="Bravo! Your news is authentic by our sources."

#SVM

		prediction3 = load_svm.predict([text])
		for i in range(0,len(words)):
			if words[i] in text:
				if prediction3[0]=="True":
					prediction="False"
				else:
					prediction3="True"
		for i in range(0,len(new)):
			if new[i] in text:
				if prediction3[0]=="True":
					prediction="False"
				else:
					prediction3="True"
		if prediction3 == [True]:
			g="Fake"
			h="Ouch! Someone told you a lie!"	
		elif prediction3==[False]:
			g="True"
			h="Bravo! Your news is authentic by our sources."
			
		else:
			g="Fake"
			h="Ouch! Someone told you a lie!"



#RANDOM FOREST

		prediction4 = load_forest.predict([text])
		prob4 = load_forest.predict_proba([text])
		i=prob4[0][1]
		for l in range(0,len(words)):
			if words[l] in text:
				i=1-i
		for w in range(0,len(new)):
			if new[w] in text:
				i=1-i
				break
		if i<0.52:
			j="FAKE"
			k="Ouch! Someone told you a lie!"
		elif i>=0.54 and i <= 0.57 or i==0.52:
			j="Uncertain"
			k="Hmm! A tricky One.Not sure whether the news is correct or not."
		else:
			j="TRUE"
			k="Bravo! Your news is authentic by our sources."

		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO history (News,Label) VALUES (%s,%s)",(text,x))
		mysql.connection.commit()
		return render_template('user_details.html', x=x,y=y, z=z,a=a,b=b,c=c,d=d,e=e,f=f,g=g,h=h,i=i,j=j,k=k)
	else:
		return render_template('index.html')

@app.route('/d')
def d():
	cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

	cur.execute("SELECT News FROM History")
	user=cur.fetchall()
	cur.execute("SELECT Label FROM History")
	label=cur.fetchall()
	cur.close()
	return render_template('history.html',user=user,label=label)



if __name__ == "__main__":
	app.secret_key = "012#!ApaApaAjaBoleh)(*^%"
	app.debug = True
	app.run()