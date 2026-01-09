Product Management System (Flask + MongoDB)
A full-stack web application that allows users to register, log in, and manage their own products (add, view, update, and delete) with all data stored in MongoDB.

​
🔧 Tech Stack
Frontend: HTML, CSS, JavaScript
​Backend: Python, Flask
Database: MongoDB (accessed via MongoDB Compass)
​Other: Flask-PyMongo, Werkzeug (password hashing)

​
✨ Features
User registration and login with secure password hashing Session-based authentication, so each user sees only their own products Add products with name, value, and description View list of all products added by the logged-in user Update existing product details Delete products. All data stored in MongoDB and viewable in MongoDB Compass

​
📂 Project Structure


project-root/

├── app.py
# Main Flask backend application

├── requirements.txt
# Python dependencies

├── templates/

│   ├── base.html          # Base layout template

│   ├── login.html         # Login & Register page

│   ├── dashboard.html     # Main menu page

│   ├── product_entry.html # Add product page

│   ├── product_view.html  # View products page

│   └── product_update.html# Update product page

└── static/

    ├── css/
    
    │   └── style.css      # Stylesheet
    
    └── js/
        └── main.js        # Frontend JavaScript
        
        
🚀 Getting Started


Prerequisites

Python 3.x installed

​MongoDB Community Server installed and running locally ​MongoDB Compass (optional, for GUI view of data)

​Git (if you are cloning the repo)

​Clone or download the project


If using Git:

git clone https://github.com/<your-username>/<your-repo-name>.git

cd <your-repo-name>

Or download as ZIP from GitHub and extract, then open the folder in your terminal.


🌏 To Create and activate virtual environment:

➡️ python -m venv venv

    venv\Scripts\activate  # Windows
    
    source venv/bin/activate  # Mac/Linux
    

➡️ Install dependencies

    python -m pip install -r requirements.txt
    

➡️ Configure MongoDB connection

    In app.py, ensure your MongoDB URI is set correctly:
    
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/productapp'
    
    Start the MongoDB service before running the app.
    

🏃‍➡️ ​Run the application

    python app.py
    
    Then open your browser and go to:
    
    http://127.0.0.1:5000
    
    
🔄 Basic Usage Flow

    Register a new user account from the login page.

    Log in with your credentials to access the dashboard.

    On the dashboard:

    Click Enter Product to add a new product.
    
    Click View Products to see all your products.
    
    On the products page:

    Use Update to edit an existing product.
    
    Use Delete to remove a product.
    
    View and verify your data in MongoDB Compass under database productapp, collections users and products.
