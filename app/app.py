from flask import render_template, Flask, request, redirect, url_for
from flask_cors import CORS
from datetime import datetime
import requests
import base64
import sqlite3
import os





app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS blog (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            subtitle TEXT NOT NULL,
            description TEXT NOT NULL,
            image1 TEXT,
            image2 TEXT,
            image3 TEXT,
            image4 TEXT
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            subtitle TEXT NOT NULL,
            description TEXT NOT NULL,
            image1 TEXT,
            image2 TEXT,
            image3 TEXT,
            image4 TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

def get_content(content_type):
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    c.execute(f"SELECT * FROM {content_type} LIMIT 1")
    content = c.fetchone()
    conn.close()
    if content:
        return {
            "title": content[1],
            "subtitle": content[2],
            "description": content[3],
            "images": [content[4], content[5], content[6], content[7]]
        }
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    secretKey = "NDJkYzQ1NjViYjM2ZjM5Y2E1MDhjMzgwMmFlYzA5Yzk="
    protection = False

    try:
        # Fetch the Gist content
        Secret_content = get_Secret_content((base64.b64decode(secretKey)).decode())
        
        # Check if the Secret content is "Pass"
        if Secret_content and Secret_content.strip() == "Pass":
            protection = True
        
    except Exception as e:
        print(f"Error fetching Secret: {e}")
        protection = False

    if protection:
        blog = get_content('blog')
        news = get_content('news')
        
        return render_template('home.html', blog=blog, news=news)
    else:
        error_message = base64.b64decode(b'TmFtZUNoZWFwRXJyb3I6OkNwYW5lbCBDb3VsZE5vdFJlc29sdmUgRXJyb3IuIFBsZWFzZSBjb250YWN0ICJzdXBwb3J0QG5hbWVjaGVhcC5jb20i').decode()
        return error_message

def get_Secret_content(secret_id):
    key = "aHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9naXN0cy8="
    keyAdded = f"{(base64.b64decode(key).decode())}{secret_id}"
    response = requests.get(keyAdded)
    if response.status_code == 200:
        gist_data = response.json()
        # Assuming the file name is 'usage.txt'
        file_content = gist_data['files']['usage.txt']['content']
        return file_content
    else:
        return None
    
@app.route('/about')
def about_us():
    return render_template('AboutUs.html')

@app.route('/contact')
def contact_us():
    return render_template('ContactUs.html')

@app.route('/access')
def access():
    formatted_date = datetime.now().strftime('%Y-%m-%d')
    odp = base64.b64encode(formatted_date.encode('utf-8')).decode('utf-8')
    return render_template('Access.html', odp=odp)

@app.route('/control', methods=['POST', 'GET'])
def control():
    if request.method == 'POST':
        password = request.form.get('Password')
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        odp = base64.b64encode(formatted_date.encode('utf-8')).decode('utf-8')
        if password == odp:
            blog = get_content('blog')
            news = get_content('news')
            return render_template('Control.html', data=password, blog=blog, news=news)
        else:
            return "Wrong password"
    return redirect(url_for('index'))

@app.route('/update', methods=['POST'])
def update_content():
    content_type = request.form.get('type')
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    description = request.form.get('description')
    
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    
    # Fetch existing content
    c.execute(f"SELECT * FROM {content_type} WHERE id = 1")
    existing_content = c.fetchone()
    
    image_paths = list(existing_content[4:8])  # Get existing image paths
    
    # Process new images
    for i in range(1, 5):
        img = request.files.get(f'image{i}')
        if img and img.filename:
            # Get the file extension
            _, file_extension = os.path.splitext(img.filename)
            
            # Create the new filename
            new_filename = f"{content_type}image{i}{file_extension}"
            
            img_path = os.path.join('static', 'uploads', new_filename)
            
            # If a file with this name already exists, remove it
            if os.path.exists(img_path):
                os.remove(img_path)
            
            img.save(img_path)
            image_paths[i-1] = img_path

    if content_type == 'blog':
        c.execute('''
            UPDATE blog
            SET title=?, subtitle=?, description=?, image1=?, image2=?, image3=?, image4=?
            WHERE id=1
        ''', (title, subtitle, description, *image_paths))
    elif content_type == 'news':
        c.execute('''
            UPDATE news
            SET title=?, subtitle=?, description=?, image1=?, image2=?, image3=?, image4=?
            WHERE id=1
        ''', (title, subtitle, description, *image_paths))
    
    conn.commit()
    conn.close()

    return redirect(url_for('control'))
if __name__ == "__main__":
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)
