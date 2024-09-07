from flask import Flask, jsonify, request
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

DATA_FILE = 'data.csv'

# Ensure the data file exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Description", "Category", "Amount"])
    df.to_csv(DATA_FILE, index=False)

@app.route('/api/data', methods=['GET'])
def get_data():
    df = pd.read_csv(DATA_FILE)
    data = df.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_data():
    content = request.json
    # Convert 'Date' strings back to datetime
    for entry in content:
        entry['Date'] = datetime.fromisoformat(entry['Date']).date()
    
    new_data = pd.DataFrame(content)
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=new_data.columns)

    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return jsonify({"message": "Data added successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
