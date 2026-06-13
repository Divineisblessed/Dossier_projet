#db_url sera utilisé pour lier notre base de données à models.py
#db_url = "lien de la base de données." 
# fichiers python


import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre code secret ici'
    # pour creer un l'url de votre base de donnes vous suivez cette syntaxe: 
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/nom_dela_base_de_donnees'
    SQLALCHEMY_TRACK_MODIFICATIONS = False