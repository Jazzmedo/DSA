from flask import render_template, Flask,request
from flask_cors import CORS, cross_origin
from datetime import datetime
import base64


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('Access.html',odp = odp)

@app.route('/control',methods=['POST'])
def control():
    password = request.form.get('Password')
    formatted_date = datetime.now().strftime('%Y-%m-%d')
    odp = base64.b64encode(formatted_date.encode('utf-8')).decode('utf-8')
    if password == odp:
        return render_template('Control.html',data=password)
    else :
        return "Wrong password"
    
if __name__ == "__main__":
    app.run(debug=True)
    classflask_cors.CORS(app=None, **kwargs)