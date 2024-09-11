from flask import Flask, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_mail import Mail, Message
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, current_user, logout
from datetime import datetime
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ehtrtrh654554y5443t43t34563453465'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medicinal.db'
db = SQLAlchemy(app)


class Forum(db.Model):
    __tablename__ = "forum"
    id = db.Column(db.Integer, primary_key=True)
    medicine = db.Column(db.String(250),nullable=False)
    effect = db.Column(db.String(250), nullable=False)
    severity = db.Column(db.String(250), nullable=False)
    manufacturer = db.Column(db.String(250), nullable=False)
    batch_number = db.Column(db.Integer, nullable=False)
    expiry_date =  db.Column(db.Date, nullable=False)
    result = db.Column(db.String(250), nullable=False) 
    author = relationship("User", back_populates="jesus")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id")) 

class Forum2(db.Model): 
    __tablename__ = "forum2"
    id = db.Column(db.Integer, primary_key=True)
    prescribed_doses = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    mermaid = relationship("User",back_populates="christ")
    mermaid_2 = db.Column(db.Integer, db.ForeignKey("users.id"))


class User(db.Model,UserMixin):
    __tablename__ = "users" 
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.String(250), nullable=False)
    hospital = db.Column(db.String(250), nullable=False)
    jesus =  relationship("Forum", back_populates="author")   
    christ = relationship("Forum2",back_populates='mermaid')    


with app.app_context():
     db.create_all()   

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)      

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
# app.config['MAIL_PORT'] = 587  # Typical for TLS
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your-email@example.com'  # Replace with your email
# app.config['MAIL_PASSWORD'] = 'your-password'  
# app.config['MAIL_DEFAULT_SENDER'] = ('YourAppName', 'your-email@example.com')

# mail = Mail(app)    

# # Initialize database
# with app.app_context():
#     db.create_all()


@app.route('/register', methods=['GET','POST'])
def register():
    data = request.get_json()  
    id = data['id']
    hospital = data['hospital']
    user = db.session.query(User).filter(User.hospital_id == id, User.hospital == hospital)
    
    if user:
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(hospital_id=id,hospital=hospital)
    
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return jsonify({'message': 'Registration successful!'}), 201

# # Route for forgot password (React integration)
# @app.route('/forgot_password', methods=['POST' 'GET'])
# def forgot_password():
#     if (request.method == "post"):
#         data = request.get_json()
#         session["email"] = data["email"]
#     data = request.get_json()
    
#     if data['action'] == 'generate_otp':
#         session['start_time'] = time.time()
#         session['otp'] = random.randint(100000, 999999) 
#         try:
#             msg = Message('Your OTP Code', recipients=[session["email"]])
#             msg.body = f'Your OTP code is {session["otp"]}. It is valid for 10 minutes.'
#             mail.send(msg)
#             return jsonify({'message': 'OTP sent to your email.'}), 200
#         except Exception as e:
#             return jsonify({'message': 'Failed to send OTP. Please try again later.'}), 500

    
#     elif data['action'] == 'verify_otp':
#         otp = data.get('otp')
#         start_time = session.get('start_time')
#         otp = data['otp']
#         new_time = int(time.time()) - int(start_time)

#         if new_time >= 600:  
#             return jsonify({'message': 'Time limit exceeded.'}), 400
#         elif int(otp) == session.get('otp'):
#             return jsonify({
#                     'message': 'OTP verified successfully!',
#                     'redirect_url': url_for('your_next_route')  
#                 }), 200
#         else:
#             return jsonify({'message': 'Invalid OTP.'}), 400
        

@app.route('/login', methods=['GET','POST'])
def login():
    data = request.get_json()  
    id = data['id']
    
    result = db.session.execute(db.select(User).where(User.id == id))
    user = result.scalar()
    login_user(user)
    if not user:
        return jsonify({'message': "That email does not exist, please try again."}), 400
    
    return jsonify({'message': 'Login successful!', 'redirect_url': url_for('my_route')}), 200  

# @app.route('/change',methods = ['POST' 'GET'])
# def change():
#     email = session["email"]
#     password = request.get('password')
#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
#     result = db.session.execute(db.select(Registration1).where(Registration1.email == email))
#     if result:
#       result.password  = hashed_password
#       db.session.commit()
#       return jsonify({'message': 'Password updated successfully!'}), 200
#     else:
#         return jsonify({'message': 'User not found'}), 404


@app.route('/forum1', methods=['POST', 'GET'])
def forum1():
    data = request.get_json()
    medicine = data["medicine"]
    
    forums = db.session.execute(
        db.select(Forum).where(Forum.medicine == medicine)
    ).scalars().all()
    
    response_data = []
    
    for forum in forums:
      
        if forum.author.id == current_user.id:
           
            forum_data = {
                'id': forum.id,
                'medicine': forum.medicine,
                'effect': forum.effect,
                'severity': forum.severity,
                'manufacturer': forum.manufacturer,
                'batch_number': forum.batch_number,
                'expiry_date': forum.expiry_date.strftime('%Y-%m-%d'),  
                'result': forum.result,
                'author_id': forum.author_id
            }
            response_data.append(forum_data)
      

    if response_data:
        return jsonify(response_data)
    else:
        return jsonify({"message": "No matching records found"}), 404

@app.route('/store1', methods=['POST', 'GET'])
def forum1():
    data = request.get_json()  

    try:
        new_entry = Forum(
            medicine=data['medicine'],
            effect=data['effect'],
            severity=data['severity'],
            manufacturer=data['manufacturer'],
            batch_number=data['batch_number'],
            expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date(),
            result=data['result'],
            author_id=data['author_id']
        )
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Entry created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error creating entry", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)