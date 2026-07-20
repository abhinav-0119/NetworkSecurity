from flask import Flask,render_template,request

import numpy as np
import pandas as pd
from networksecurity.pipelines.batch_prediction import CustomData
from networksecurity.utils.mlutils.model.estimator import NetworkModel
from networksecurity.utils.mainutils.utils import load_object

app=Flask(__name__)
preprocessor=load_object("finalmodel/preprocessor.pkl")
model=load_object("finalmodel/model.pkl")
network_model=NetworkModel(preprocessor,model)





@app.route('/')
def home():
    return render_template("home.html")


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method=='GET':
        return render_template('predict.html')
    else:
        data = CustomData(
        having_IP_Address=int(request.form.get('having_IP_Address')),
        URL_Length=int(request.form.get('URL_Length')),
        Shortining_Service=int(request.form.get('Shortining_Service')),
        having_At_Symbol=int(request.form.get('having_At_Symbol')),
        double_slash_redirecting=int(request.form.get('double_slash_redirecting')),
        Prefix_Suffix=int(request.form.get('Prefix_Suffix')),
        HTTPS_token=int(request.form.get('HTTPS_token')),
        having_Sub_Domain=int(request.form.get('having_Sub_Domain')),
        SSLfinal_State=int(request.form.get('SSLfinal_State')),
        Domain_registeration_length=int(request.form.get('Domain_registeration_length')),
        age_of_domain=int(request.form.get('age_of_domain')),
        DNSRecord=int(request.form.get('DNSRecord')),
        Page_Rank=int(request.form.get('Page_Rank')),
        Google_Index=int(request.form.get('Google_Index')),
        web_traffic=int(request.form.get('web_traffic')),
        Request_URL=int(request.form.get('Request_URL')),
        URL_of_Anchor=int(request.form.get('URL_of_Anchor')),
        Links_in_tags=int(request.form.get('Links_in_tags')),
        Links_pointing_to_page=int(request.form.get('Links_pointing_to_page')),
        Favicon=int(request.form.get('Favicon')),
        SFH=int(request.form.get('SFH')),
        Abnormal_URL=int(request.form.get('Abnormal_URL')),
        Redirect=int(request.form.get('Redirect')),
        Submitting_to_email=int(request.form.get('Submitting_to_email')),
        on_mouseover=int(request.form.get('on_mouseover')),
        RightClick=int(request.form.get('RightClick')),
        popUpWidnow=int(request.form.get('popUpWidnow')),
        Iframe=int(request.form.get('Iframe')),
        port=int(request.form.get('port')),
        Statistical_report=int(request.form.get('Statistical_report'))
    )
        df=data.data_asdf()
        result=network_model.predict(df)
        return render_template('result.html',prediction=result[0])
@app.route('/model')
def model():
    return render_template('model.html')


@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/contact')


def contact():
    return render_template("contact.html")

@app.route('/evaluation')
def evaluation():
    return render_template("evaluation.html")

if __name__=='__main__':
    app.run(debug=True)