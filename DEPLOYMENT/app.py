import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import script 

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def predict():
    return render_template("index.html")

@app.route('/predict',methods=["POST"])

def y_predict():
    url = request.form['url']
    checkprediction = script.main(url)
    prediction = model.predict(checkprediction)

    if(prediction==-1):
        pred="Your are safe!!  This is a Legitimate Website."
    elif(prediction==1):
        pred="You are in the Phishing site.Don't trust!"    
    else:
        pred="You are in a suspecious site. Be Cautious!"
    return render_template("index.html", prediction_text='{ }'.format(pred),url=url)

@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.y_predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(output)
if __name__=='__main__':
    app.run(debug=True)