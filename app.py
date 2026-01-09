from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/product_management_db'

mongo = PyMongo(app)

# Home/Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'register' in request.form:
            # Registration
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            
            # Validation
            if not username or not email or not password:
                flash('All fields are required!', 'error')
                return render_template('login.html')
            
            if password != confirm_password:
                flash('Passwords do not match!', 'error')
                return render_template('login.html')
            
            # Check if user exists
            existing_user = mongo.db.users.find_one({'$or': [{'email': email}, {'username': username}]})
            if existing_user:
                flash('User already exists!', 'error')
                return render_template('login.html')
            
            # Create user
            hashed_password = generate_password_hash(password)
            user_data = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'date_created': datetime.utcnow()
            }
            
            result = mongo.db.users.insert_one(user_data)
            flash('Registration successful! Please login.', 'success')
            return render_template('login.html')
        
        else:
            # Login
            email = request.form['email']
            password = request.form['password']
            
            if not email or not password:
                flash('Email and password are required!', 'error')
                return render_template('login.html')
            
            user = mongo.db.users.find_one({'email': email})
            if user and check_password_hash(user['password'], password):
                session['user_id'] = str(user['_id'])
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid credentials!', 'error')
                return render_template('login.html')
    
    return render_template('login.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get user's products
    user_products = list(mongo.db.products.find({'user_id': session['user_id']}).limit(5))
    
    return render_template('dashboard.html', 
                         username=session['username'], 
                         products=user_products)

# Product entry page
@app.route('/enter_product', methods=['GET', 'POST'])
def enter_product():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        description = request.form['description']
        
        # Validation
        if not name or not value or not description:
            flash('All fields are required!', 'error')
            return render_template('product_entry.html')
        
        try:
            value = float(value)
            if value < 0:
                flash('Value must be positive!', 'error')
                return render_template('product_entry.html')
        except ValueError:
            flash('Please enter a valid number for value!', 'error')
            return render_template('product_entry.html')
        
        # Create product
        product_data = {
            'user_id': session['user_id'],
            'name': name,
            'value': value,
            'description': description,
            'date_created': datetime.utcnow(),
            'date_modified': datetime.utcnow()
        }
        
        mongo.db.products.insert_one(product_data)
        flash('Product added successfully!', 'success')
        return render_template('product_entry.html', show_view_button=True)
    
    return render_template('product_entry.html')

# Product view page
@app.route('/view_products')
def view_products():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get all user's products
    user_products = list(mongo.db.products.find({'user_id': session['user_id']}))
    total_value = sum(product['value'] for product in user_products)
    
    return render_template('product_view.html', 
                         products=user_products, 
                         total_value=total_value,
                         product_count=len(user_products))

# Product update page
@app.route('/update_product/<product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get the product
    product = mongo.db.products.find_one({
        '_id': ObjectId(product_id),
        'user_id': session['user_id']
    })
    
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('view_products'))
    
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        description = request.form['description']
        
        # Validation
        if not name or not value or not description:
            flash('All fields are required!', 'error')
            return render_template('product_update.html', product=product)
        
        try:
            value = float(value)
            if value < 0:
                flash('Value must be positive!', 'error')
                return render_template('product_update.html', product=product)
        except ValueError:
            flash('Please enter a valid number for value!', 'error')
            return render_template('product_update.html', product=product)
        
        # Update product
        mongo.db.products.update_one(
            {'_id': ObjectId(product_id)},
            {
                '$set': {
                    'name': name,
                    'value': value,
                    'description': description,
                    'date_modified': datetime.utcnow()
                }
            }
        )
        
        flash('Product updated successfully!', 'success')
        return redirect(url_for('view_products'))
    
    return render_template('product_update.html', product=product)

# Delete product
@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    mongo.db.products.delete_one({
        '_id': ObjectId(product_id),
        'user_id': session['user_id']
    })
    
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('view_products'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)