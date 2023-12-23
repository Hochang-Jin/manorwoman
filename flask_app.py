from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
import config 
import requests
from datetime import date, timedelta

ID = config.config["id"]

app = Flask(__name__)



@app.route('/')
def home():
    return redirect(url_for('main_page'))

@app.route('/index')
def main_page():
    return render_template('index.html')

@app.route('/result', methods=['POST','GET'])
def result():
    characterName = '채수린'
    if request.method=='POST':
        characterName = request.form.get('name')
    urlString = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + characterName
    response = requests.get(urlString, headers = headers)
    if response.status_code != 200:
        flash('캐릭터 이름을 정확히 입력해 주세요.')
        return redirect(url_for('main_page'))
    ocid = response.json()["ocid"]
    
    date_yesterday = date.today() - timedelta(days = 1)
   
    urlString = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={date_yesterday}"
    response = requests.get(urlString, headers = headers)

    gender = response.json()["character_gender"]
    img = response.json()["character_image"]

    return render_template('result.html',gender=gender,img=img, name=characterName)

if __name__ == '__main__':
    headers = {
            "x-nxopen-api-key": ID
            }
    app.secret_key = 'ssssss'
    app.run(host="0.0.0.0",debug=True)
