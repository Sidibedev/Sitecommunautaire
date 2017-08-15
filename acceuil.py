
#coding=utf-8
from flask import Flask  
from flask_pymongo import PyMongo
from flask import render_template , request ,redirect
import datetime
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
   date = datetime.datetime.now()
   articles = mongo.db.articles.find()
   if request.method == 'POST':
    prenom = request.form['prenom']
    nom = request.form['nom']
    email = request.form['email']
    cat = request.form['cat']
    titre = request.form['titre']
    article.insert_one({ 'date_creation' : date ,'categories' : cat ,'titre' : titre , 'auteur' : { 'nom' : nom , 'prenom' : prenom , 'email' : email} })

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


@app.route('/readmore') 
def readmore():
    article = mongo.db.articles
    id=request.values.get("idreadmore")
    articlereadmore = mongo.db.articles.find({"_id":ObjectId(id)})
    return render_template('readmore.html', articlereadmore=articlereadmore)


@app.route('/comment' , methods = ['POST'])
def comment():
    idcomment=request.form['idarticlecomment']
    article = mongo.db.articles
    articlereadmore = mongo.db.articles.find({"_id":ObjectId(idcomment)})
    datecomment= datetime.datetime.now()
    email = request.form['emailcomment']
    commentaire = request.form['commentaire']
    article.update({"_id":ObjectId(idcomment)}, {'$set':{  "commentaires"  : {"date" : datecomment , "auteur" : email , "contenu" : commentaire }  }})
    return render_template('readmore.html' , articlereadmore=articlereadmore)



   
if __name__ == "__main__":
            app.run()


