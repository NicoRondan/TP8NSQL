from pymongo import MongoClient
import json
from bson.objectid import ObjectId

def connect_db():
    try:
        client = MongoClient(host='db', port=27017)
        db = client["restaurants"]
        return db
    except Exception as err:
        print("An exception occurred :", err)
    
def initialize():
    db = connect_db()
    if db.restaurants.count() == 0:
        try:
            #Insertar archivos json contenidos en restaurants.json
            with open('restaurants.json', "r", encoding='utf-8') as file:
                data = json.load(file)
            db.restaurants.insert_many(data)
            with open('restaurants_concepcion.json', "r", encoding='utf-8') as file:
                data = json.load(file)
            db.restaurants.insert_many(data)
        except Exception as err:
            print("An exception occurred :", err)
            
def get_restaurants():
    db = connect_db()
    data = db.restaurants.find({},{"_id":1,"name":2,"borough":3,"address":4,"cuisine":5})
    restaurants = []
    for item in data:
        #Evitar problema del objectId al mapear en el front
        item["id"] = str(item["_id"])
        #Eliminamos del diccionario
        item.pop('_id')
        restaurants.append(item)
    return restaurants 

def get_types():
    db = connect_db()
    #Obtener tipos de restaurantes (no repetidos)
    data = db.restaurants.distinct("cuisine")
    restaurants = []
    for item in data:
        restaurants.append(item)
    return restaurants

def get_restaurants_per_type(type):
    db = connect_db()
    restaurants = []
    data = db.restaurants.find({ "cuisine":{ "$regex": type }}, { "_id":1,"name":2,"borough":3,"address":4,"cuisine":5 })
    for item in data:
        #Evitar problema del objectId al mapear en el front
        item["id"] = str(item["_id"]) 
        item.pop('_id')
        restaurants.append(item) 
    return restaurants 

def get_restaurant(id):
    db = connect_db()
    #Buscar en la bbdd
    restaurant = db.restaurants.find_one({'_id': ObjectId(id)})
    #Evitar problema del objectId al mapear en el front
    restaurant["id"] = str(restaurant["_id"]) 
    restaurant.pop('_id')
    return restaurant

def add_restaurant(restaurant):
    db = connect_db()
    db.restaurants.insert_one(restaurant)

def update_restaurant(restaurant, id):
    db = connect_db()
    db.restaurants.update_one({'_id': ObjectId(id)}, {'$set': restaurant }) 
    
def delete_restaurant(id):
    db = connect_db()
    db.restaurants.delete_one({'_id': ObjectId(id)})