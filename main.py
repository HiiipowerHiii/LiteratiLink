from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
logger.addHandler(handler)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('discussions', lazy=True))
    message = db.Column(db.Text, nullable=False)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('meetings', lazy=True))
    date_time = db.Column(db.DateTime, nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    logger.info('New user registered: %s', data['username'])
    return jsonify({'message': 'User registered successfully.'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        logger.info('User login successful: %s', data['username'])
        return jsonify({'access_token': access_token}), 200
    logger.warning('Login attempt failed for: %s', data['username'])
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'])
    db.session.add(book)
    db.session.commit()
    logger.info('New book added: %s by %s', data['title'], data['author'])
    return jsonify({'message': 'Book added successfully.'}), 201

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = [{'title': book.title, 'author': book.author} for book in books]
    logger.info('Books retrieved: %d books', len(output))
    return jsonify({'books': output}), 200

@app.route('/discussions', methods=['POST'])
@jwt_required()
def add_discussion():
    data = request.get_json()
    discussion = Discussion(book_id=data['book_id'], message=data['message'])
    db.session.add(discussion)
    db.session.commit()
    logger.info('New discussion added for book ID: %d', data['book_id'])
    return jsonify({'message': 'Discussion added successfully.'}), 201

@app.route('/discussions/<int:book_id>', methods=['GET'])
def get_discussions(book_id):
    discussions = Discussion.query.filter_by(book_id=book_id).all()
    output = [{'message': discussion.message} for discussion in discussions]
    logger.info('Discussions retrieved for book ID: %d, count: %d', book_id, len(output))
    return jsonify({'discussions': output}), 200

@app.route('/meetings', methods=['POST'])
@jwt_required()
def schedule_meeting():
    data = request.get_json()
    meeting = Meeting(book_id=data['book_id'], date_time=data['date_time'])
    db.session.add(meeting)
    db.session.commit()
    logger.info('Meeting scheduled for book ID: %d', data['book_id'])
    return jsonify({'message': 'Meeting scheduled successfully.'}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)