
#coding=utf-8
from flask import Flask  
from flask_pymongo import PyMongo
from flask import render_template , request ,redirect
from bson.objectid import ObjectId

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
    

@app.route('/delete')
def delete():
    article = mongo.db.articles
    key=request.values.get("id")
    article.remove({"_id":ObjectId(key)})
    return redirect("/")
	
@app.route('/update')
def update():
    article = mongo.db.articles
    id=request.values.get("idmodif")
    articleToUpdate = mongo.db.articles.find({"_id":ObjectId(id)})
    return render_template('modif.html', articleToUpdate=articleToUpdate)
    
@app.route('/updatearticle' , methods=['POST'])
def updatearticle():
    prenom = request.form['prenom']
    nom = request.form['nom']
    email = request.form['email']
    titre = request.form['titre']
    idarticle = request.form['id']
    article = mongo.db.articles
    article.update({"_id":ObjectId(idarticle)}, {'$set':{ "titre":titre, "auteur":{ 'nom' : nom , 'prenom' : prenom , 'email' : email } }})
    return redirect("/")



@app.route('/search' , methods=['POST'])
def search():
    search = request.form['search']
    ref = request.form['ref']
    articlesearch =  mongo.db.articles.find({ref : search})
    return render_template('search.html' , articlesearch=articlesearch)






   
if __name__ == "__main__":
            app.run()


