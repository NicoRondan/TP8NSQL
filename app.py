from flask import Flask, render_template, request, redirect, url_for, jsonify, Response, flash
from db import initialize, get_restaurants, get_restaurant, get_types, get_restaurants_per_type, add_restaurant, update_restaurant, delete_restaurant

app = Flask(__name__)

"""Clave necesaria para poder utilizar flash"""
app.secret_key = 'clave_secreta'

@app.route('/initialize_db', methods=['GET'])
@app.before_first_request
def initialize_db():
    initialize()

@app.route('/about', methods=['GET'])
def about():
    #Renderizar about
    return render_template('about.html')  

@app.route('/', methods=['GET', 'POST'])
def index():
    #Obtener tipos de restaurantes
    types = get_types()
    if request.method == 'GET':
        #Obtener restaurantes
        restaurants = get_restaurants()
        #Renderizar index
        return render_template('index.html', restaurants=restaurants, types=types)
    else:
        option = request.form.get('types')
        #En caso de que no se elija una opción, retornamos al index
        if option == None:
            flash('Select an Option, Please')
            return redirect(url_for('index'))
        else:
            #Obtener restaurantes por tipo
            restaurants = get_restaurants_per_type(option)
            #Renderizar index
            return render_template('index.html', restaurants=restaurants, types=types, option=option)

@app.route('/restaurant/<id>', methods=['GET'])
def restaurant_info(id):
    restaurant = get_restaurant(id)
    #Renderizar detail
    return render_template('detail.html', restaurant=restaurant)

@app.route('/add', methods=['GET', 'POST'])
def append_restaurant():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        #Obtener datos del formulario
        name = request.form.get('name')
        cuisine = request.form.get('cuisine')
        borough = request.form.get('borough')
        street = request.form.get('street')
        zipcode = request.form.get('zipcode')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        
        coord = [longitude, latitude]
        restaurant = {
            'address': {
                'coord': coord,
                'street': street,
                'zipcode': zipcode
            },
            'borough': borough,
            'cuisine': cuisine.capitalize(),
            'name': name
        }
        #Insertar objeto
        try:
            add_restaurant(restaurant)
            flash('Restaurant added successfully!')
            return redirect(url_for('index'))
        except Exception as err:
            print("An exception occurred :", err)
            flash('An error has occurred...')
            redirect('/add')

@app.route('/update/<id>', methods=['GET', 'POST'])
def modify_restaurant(id):
    #Obtener datos del formulario
    name = request.form.get('name')
    cuisine = request.form.get('cuisine')
    borough = request.form.get('borough')
    street = request.form.get('street')
    zipcode = request.form.get('zipcode')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    
    coord = [longitude, latitude]
    restaurant = {
        'address': {
            'coord': coord,
            'street': street,
            'zipcode': zipcode
        },
        'borough': borough,
        'cuisine': cuisine.capitalize(),
        'name': name
    }
    try:
        update_restaurant(restaurant, id)
        flash('Restaurant updated successfully!')
        return redirect('/restaurant/' + id)
    except Exception as err:
        print("An exception occurred :", err)
        flash('An error has occurred...')
        return redirect('/restaurant/' + id)

@app.route('/delete/<id>', methods=['GET'])
def remove_restaurant(id):
    try:
        delete_restaurant(id)
        flash('Restaurant deleted successfully!')
        return redirect(url_for('index'))
    except Exception as err:
        print("An exception occurred :", err)
        flash('An error has occurred...')
        return redirect('/restaurant/' + id)
    
    
#En caso de error de ruta
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status': 404 
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(host='localhost', port='5000', debug=True)