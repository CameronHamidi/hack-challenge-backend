import json
from db import db, Trip, Day, Event
from flask import Flask, request

app = Flask(__name__)
db_filename = 'cms.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# Your routes here
@app.route('/api/trips/')
def getTrips():
    trips = Trip.query.all()
    return json.dumps({'success': True, 'data': [t.serialize() for t in trips]}), 200

@app.route('/api/trips/', methods=['POST'])
def createTrip():
    post_body = json.loads(request.data)
    name = post_body['name']
    location = post_body['location']

    trip = Trip(name=name, location=location)
    db.session.add(trip)
    db.session.commit()
    return json.dumps({'success': True, 'data': trip.serialize()}), 201

@app.route('/api/trip/<int:tid>/', methods=['DELETE'])
def deleteTrip(tid):
    trip = Trip.query.filter_by(id=tid).first()
    db.session.delete(trip)
    db.session.commit()
    return json.dumps({'success': True, 'data': trip.serialize()}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
