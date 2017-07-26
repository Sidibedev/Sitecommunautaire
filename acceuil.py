
#coding=utf-8
from flask import Flask  
from flask_pymongo import PyMongo
from flask import render_template , request

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'

mongo = PyMongo(app);



@app.route('/')
def index():
   articles = mongo.db.articles.find()
   return render_template('index.html', articles=articles)

@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/send' , methods= ['POST'])
def add():
   article = mongo.db.articles
   articles = mongo.db.articles.find()
   if request.method == 'POST':
   	prenom = request.form['prenom']
   	nom = request.form['nom']
   	email = request.form['email']
   	titre = request.form['titre']
   	article.insert_one({'titre' : titre , 'auteur' : { 'nom' : nom , 'prenom' : prenom , 'email' : email} })
    

   	

   return render_template('index.html' , articles=articles)	




