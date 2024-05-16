from flask import Flask, render_template, request, jsonify, redirect, flash, session
from datetime import datetime
from database import opendb, Sensor, get_all, add, User

app = Flask(__name__)
app.secret_key = 'iot pr'

@app.route('/')
def index():
    return render_template('index.html')

# login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = opendb()
        user = db.query(User).filter_by(name=username).first()
        db.close()
        if user and user.password == password:
            session['id'] = user.id
            session['email'] = user.email
            session['isauth'] = True
            return redirect('/dashboard')
        else:
            flash('Invalid email or password')
    return render_template('login.html')

# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/api/sensor',methods=['GET','POST'])
def api_sensor():
    data = request.get_json()
    print(data)
    add(Sensor(
        name = data.get('sensor'),
        location = data.get('location'),
        tempf = data.get('temperaturef'),
        temp = data.get('temperature'),
        humidity = data.get('humidity'),
    ))
    response = {
        'status': 'updated',
        'created_on': datetime.now(),
    }
    return jsonify(response), 200

@app.route('/dashboard')
def dashboard():
    if not session.get('isauth'):
        return redirect('/login')
    db = opendb()
    sensor1 = db.query(Sensor).filter_by(name='1').all()
    sensor2 = db.query(Sensor).filter_by(name='2').all()
    db.close()
    return render_template('dashboard.html', 
        sensor1=sensor1, 
        sensor2=sensor2, 
        sensor1_latest = sensor1[-10:],
        sensor2_latest = sensor2[-10:],
    )

@app.route('/api/get/sensor/')
def api_get_sensor():
    db = opendb()
    sensor1 = db.query(Sensor).filter_by(name='1').order_by(Sensor.created_on.desc()).limit(200).all()
    sensor2 = db.query(Sensor).filter_by(name='2').order_by(Sensor.created_on.desc()).limit(200).all()
    sensor1_dict = []
    for s in sensor1:
        sensor1_dict.append({
            'id': s.id,
            'name': s.name,
            'location': s.location,
            'tempf': s.tempf,
            'temp': s.temp,
            'humidity': s.humidity,
            'created_on': s.created_on,
        })
    sensor2_dict = []
    for s in sensor2:
        sensor2_dict.append({
            'id': s.id,
            'name': s.name,
            'location': s.location,
            'tempf': s.tempf,
            'temp': s.temp,
            'humidity': s.humidity,
            'created_on': s.created_on,
        })
    db.close()
    response = {
        'sensor1': sensor1_dict,
        'sensor2': sensor2_dict,
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    