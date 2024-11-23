from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

app.config['SECRET_KEY'] = '2eac451658c45531a2cd26601e85c6eb'

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(RestaurantNames = [i.serialize() for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')  # Using .get() is safer than accessing with [] directly
        course = request.form.get('course')  # Optional field
        description = request.form.get('description')  # Optional field
        price = request.form.get('price')

        # Validation: Ensure name and price are provided
        if not name or not price:
            flash('Name and Price are required fields!', 'error')
            return redirect(url_for('newMenuItem', restaurant_id=restaurant_id))

        # Ensure price is a valid float
        try:
            price = float(price)
        except ValueError:
            flash('Invalid price value. Please enter a valid number.', 'error')
            return redirect(url_for('newMenuItem', restaurant_id=restaurant_id))

        # Create a new menu item
        new_item = MenuItem(
            name=name,
            course=course,
            description=description,
            price=price,  # Ensure price is stored as a float
            restaurant_id=restaurant.id
        )

        # Add to session and commit to the database
        session.add(new_item)
        session.commit()
        flash('New menu item added successfully!', 'success')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant.id))

    return render_template('newmenuitem.html', restaurant=restaurant)

@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        name = request.form.get('name')
        restaurant1 = Restaurant(name=name)
        session.add(restaurant1)
        session.commit()
        return redirect(url_for('restaurants'))

    return render_template('newrestaurant.html')

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('Menu item edited successfully!', 'success')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item Deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)


if __name__ == '__main__':
    app.secret_key = '2eac451658c45531a2cd26601e85c6eb'
    app.debug = True
    app.run(host='0.0.0.0', port=8085)
