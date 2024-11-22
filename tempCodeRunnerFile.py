
# @app.route('/restaurants/new/', methods=['GET', 'POST'])
# def newRestaurant():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         new_item = Restaurant(name=name)
#         session.add(new_item)
#         session.commit()
#         return redirect(url_for('restaurants'))

#     return render_template('newrestaurant.html')