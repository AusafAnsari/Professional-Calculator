from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db

# Initial flask app
app = Flask(__name__)

# Firebase config
cred = credentials.Certificate('new-python-b010f-firebase-adminsdk-fbsvc-e4e0096baf.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://new-python-b010f-default-rtdb.firebaseio.com/'
})

@app.route('/',methods=['GET','POST'])
def calculator():
    result = ''
    if request.method == 'POST':
        num1 = float(request.form['num1'])
        num2 = float(request.form['num2'])
        op = request.form['operation']


        if op== 'add':
            result = num1 + num2
            operation = f"{num1}+{num2}={result}"
        elif op == 'sub':
            result = num1 - num2
            operation = f"{num1}-{num2}={result}"
        elif op == 'mul':
            result = num1 * num2
            operation = f"{num1}*{num2}={result}"
        elif op == 'div':
            result = num1 / num2 if num2 != 0 else 'Error'
            operation = f"{num1}/{num2}={result}"

        # Push to firebase Realtime Database
        if result != 'Error':
            ref = db.reference('calculations')
            ref .push({
                'result':result,
                'operation':operation
            })

    return render_template('index.html', result=result)

#run the app
if __name__=='__main__':
    app.run(debug=True)
