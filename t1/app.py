from flask import Flask, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure the directory for images exists
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Park(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    


    def __repr__(self):
        return f'<Park {self.name}>'

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    parks = Park.query.all()
    return render_template('index.html', parks=parks)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the post request has the file part
    if 'image' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['image']  # This should match the name in the HTML form
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    if file:
        filename = file.filename
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        park_name = request.form['name']
        park_description = request.form['describe']  # Make sure this matches the HTML input name
        
        add_park(park_name, filename, park_description)

        flash('Park added successfully!', 'success')
        return redirect(url_for('index'))

def add_park(name, image_filename, description):
    image_path = os.path.join('images', image_filename)
    new_park = Park(name=name, image=image_path, description=description)
    db.session.add(new_park)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
