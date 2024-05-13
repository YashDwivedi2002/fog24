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
    sensors = get_all(Sensor)
    return render_template('dashboard.html', sensors=sensors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
    