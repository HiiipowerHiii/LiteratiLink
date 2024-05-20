from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

# Initialize app, DB, and bcrypt
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Discussion model
class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('discussions', lazy=True))
    message = db.Column(db.Text, nullable=False)

# Meeting model
class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('meetings', lazy=True))
    date_time = db.Column(db.DateTime, nullable=False)

# User Register Route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully.'}), 201

# User Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Create Book Route
@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'])
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully.'}), 201

# List Books Route
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'title': book.title, 'author': book.author}
        output.append(book_data)
    return jsonify({'books': output}), 200

# Create Discussion Route
@app.route('/discussions', methods=['POST'])
@jwt_required()
def add_discussion():
    data = request.get_json()
    discussion = Discussion(book_id=data['book_id'], message=data['message'])
    db.session.add(discussion)
    db.session.commit()
    return jsonify({'message': 'Discussion added successfully.'}), 201

# List Discussions Route
@app.route('/discussions/<int:book_id>', methods=['GET'])
def get_discussions(book_id):
    discussions = Discussion.query.filter_by(book_id=book_id).all()
    output = []
    for discussion in discussions:
        discussion_data = {'message': discussion.message}
        output.append(discussion_data)
    return jsonify({'discussions': output}), 200

# Schedule Meeting Route
@app.route('/meetings', methods=['POST'])
@jwt_required()
def schedule_meeting():
    data = request.get_json()
    meeting = Meeting(book_id=data['book_id'], date_time=data['date_time'])
    db.session.add(meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting scheduled successfully.'}), 201

# Run Server
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)