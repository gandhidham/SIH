app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
# app.config['MAIL_PORT'] = 587  # Typical for TLS
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'your-email@example.com'  # Replace with your email
# app.config['MAIL_PASSWORD'] = 'your-password'  # Replace with your email password
# app.config['MAIL_DEFAULT_SENDER'] = ('YourAppName', 'your-email@example.com')

# mail = Mail(app)    

# # Initialize database
# with app.app_context():
#     db.create_all()

# # Route for registration (with React integration)
# @app.route('/register', methods=['GET','POST'])
# def register():
#     user_count = db.session.query(Registration1).count()
#     if(user_count > 2):
#         return jsonify({'message': "cannot register more user"})
#     data = request.get_json()  # Assuming JSON data is sent from React
#     email = data['email']
#     user = db.session.query(Registration1).filter(Registration1.email == email)
    
#     if user:
#         return jsonify({'message': 'Email already exists'}), 400

#     hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
#     new_user = Registration1(name=data['name'], email=email, password=hashed_password)
    
#     db.session.add(new_user)
#     db.session.commit()
    
#     return jsonify({'message': 'Registration successful!'}), 201

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
        

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()  # Get JSON data from React
#     email = data.get('email')
#     password = data.get('password')
    
#     # Fetch user from the database
#     result = db.session.execute(db.select(Registration1).where(Registration1.email == email))
#     user = result.scalar()
    
#     if not user:
#         return jsonify({'message': "That email does not exist, please try again."}), 400
    
#     if not check_password_hash(user.password, password):
#         return jsonify({'message': 'Password incorrect, please try again.'}), 400
    
#     return jsonify({'message': 'Login successful!', 'redirect_url': url_for('my_route')}), 200  

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
