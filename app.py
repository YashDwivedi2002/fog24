from flask import Flask, render_template,request, jsonify
from datetime import datetime
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sensor',methods=['GET','POST'])
def api_sensor():
    data = request.get_json()
    print(data)
    response = {
        'status': 'updated',
        'created_on': datetime.now(),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
  