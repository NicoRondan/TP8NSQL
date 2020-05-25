import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Use a service account
cred = credentials.Certificate('key.json')
firebase_admin.initialize_app(cred)

#connection
db = firestore.client()
    
def initialize():
    restaurants = db.collection('restaurants')
    #Insertar archivos json contenidos en restaurants.json
    with open('restaurants.json', "r", encoding='utf-8') as file:
        data = json.load(file)
        for i in range (0,483):
            restaurants.add(data[i])
    with open('restaurants_concepcion.json', "r", encoding='utf-8') as file:
        data = json.load(file)
        for i in range (0,17):
            restaurants.add(data[i])  

            
def get_restaurants():
    data = db.collection('restaurants').stream()
    restaurants = []
    for item in data:
        document = item.to_dict()
        document['id'] = item.id
        restaurants.append(document)
    return restaurants 

def get_types():
    #Obtener tipos de restaurantes (no repetidos)
    data = db.collection('restaurants').stream()
    types = []
    for item in data:
        document = item.to_dict()
        if (document["cuisine"] not in types):
            types.append(document["cuisine"])
    return types

def get_restaurants_per_type(type):
    restaurants = []
    data = db.collection('restaurants').where('cuisine','==', type).stream()
    for item in data:
        document = item.to_dict()
        document['id'] = item.id
        restaurants.append(document)
    return restaurants 

def get_restaurant(id):
    #Buscar en la bbdd
    restaurants = db.collection('restaurants')
    document = restaurants.document(id).get()
    restaurant = document.to_dict()
    restaurant['id'] = document.id
    return restaurant

def add_restaurant(restaurant):
    restaurants = db.collection('restaurants')
    restaurants.add(restaurant)

def update_restaurant(restaurant, id):
    restaurants = db.collection('restaurants')
    restaurants.document(id).update(restaurant)
    
def delete_restaurant(id):
    restaurants = db.collection('restaurants')
    restaurants.document(id).delete()