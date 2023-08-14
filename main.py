import io
import zipfile

from flask import Flask, request, jsonify,send_file,render_template
import pandas as pd
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
def genReport1(csv):
    data = pd.read_csv(csv)
    avg_util_report = data[data['Avg_Util_(%)'] >= 80]
    avg_util_report = avg_util_report[
        ['Date', 'Device', 'Resource', 'Avg_Util_(%)', 'Peak_Hourly_Avg_Util_(%)', 'Peak_Util_(%)', 'Avg_Discards_(%)']]
    # print(avg_util_report)
    # print(os.getcwd())
    avg_util_report.to_csv(os.getcwd()+'\\csv_files\\avg_util.csv', index=False)

def genReport2(csv):
    data = pd.read_csv(csv)
    avg_util_report = data[data['Peak_Util_(%)'] >= 100]
    avg_util_report = avg_util_report[
        ['Date', 'Device', 'Resource', 'Avg_Util_(%)', 'Peak_Hourly_Avg_Util_(%)', 'Peak_Util_(%)', 'Avg_Discards_(%)']]
    # print(avg_util_report)
    # print(os.getcwd())
    avg_util_report.to_csv(os.getcwd()+'\\csv_files\\peak_util.csv', index=False)

def genReport3(csv):
    data = pd.read_csv(csv)
    avg_util_report = data[data['Avg_Discards_(%)'] >= 20]
    avg_util_report = avg_util_report[
        ['Date', 'Device', 'Resource', 'Avg_Util_(%)', 'Peak_Hourly_Avg_Util_(%)', 'Peak_Util_(%)', 'Avg_Discards_(%)']]
    print(avg_util_report)

    avg_util_report.to_csv(os.getcwd() + '\\csv_files\\avg_discards.csv', index=False)

def cleanUp():
    print("Yo")
    dir_path = os.getcwd() + '\\csv_files'
    files = os.listdir(dir_path)
    for file in files:
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


@app.route('/',methods=['GET'])
def index():
    return render_template("frontend.html")

@app.route('/upload',methods=['POST'])
def upload():
    if 'csv_file' not in request.files:
        return "No CSV file provided", 400

    csv_file = request.files['csv_file']
    if csv_file.filename == '':
        return "No selected file", 400

    # Process the CSV file
    csv_data = pd.read_csv(csv_file)
    csv_data.to_csv(os.getcwd() + '\\csv_files\\input.csv', index=False)
    csv_file = os.getcwd() + '\\csv_files\\input.csv'
    if csv_file:
        genReport1(csv_file)
        genReport2(csv_file)
        genReport3(csv_file)

        csv_file_path = os.getcwd() + '\\csv_files\\avg_util.csv'
        with open(csv_file_path, 'r') as csv_file:
            csv_data1 = csv_file.read()

        csv_file_path = os.getcwd() + '\\csv_files\\peak_util.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_data2 = csv_file.read()

        csv_file_path = os.getcwd() + '\\csv_files\\avg_discards.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_data3 = csv_file.read()

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.writestr('file1.csv', csv_data1)
            zip_file.writestr('file2.csv', csv_data2)
            zip_file.writestr('file3.csv', csv_data3)
        zip_buffer.seek(0)

        response = send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='data.zip'
        )

        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'

        return response




app.run(debug=True)