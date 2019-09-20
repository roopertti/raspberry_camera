from flask import Flask, jsonify, Response, request
app = Flask(__name__)
from database import ImageDatabase
import os

@app.route("/")
def hello():
    return "Tereve!"
    
@app.route("/dates")
def get_dates():
    try:
        database = ImageDatabase()
        database.create_connection()
        rows = database.fetch_many("SELECT * FROM days")
        if len(rows) <= 0:
            response = { 'message': "No dates saved", 'dates': [] }
            return jsonify(response)
        dates_formatted = list(map(lambda r: {'id': r[0], 'date': r[1]}, rows))
        print(dates_formatted)
        response = {'message': "Dates fetched", 'dates': dates_formatted}
        return jsonify(response)    
    except Exception as e:
        print(e)
        return Response("{'message': 'Problem with server'}", status=500, mimetype='application/json')
        
@app.route("/photos")
def get_photos():
    try:
        day_id = request.args.get('id', default = -1, type = int)
        date_str = request.args.get('date', default = '', type = str)
        # TODO finish photos request endpoint
        

if __name__ == "__main__":
    app.run()
