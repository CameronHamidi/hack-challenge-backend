import json
from db import db, Trip, Day, Event
from flask import Flask, request

app = Flask(__name__)
db_filename = 'trip.db'

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

@app.route('/api/trip/<int:tid>/days/', methods=['GET'])
def getDays(tid):
    trip = Trip.query.filter_by(id=tid).first()
    if not trip:
        return json.dumps({'success': False, 'data': 'No such trip exists'}), 404
    return json.dumps({'success': True, 'data': trip.serialize()['days']})

@app.route('/api/trip/<int:tid>/day/', methods=['POST'])
def createDay(tid):
    post_body = json.loads(request.data)
    date = post_body['date']
    location = post_body['location']
    trip_id = post_body['trip_id']
    
    if not Trip.query.filter_by(id=tid).first():
        return json.dumps({'success': False, 'data': 'No such trip exists'}), 404

    day = Day(
        date=date,
        location=location,
        trip_id=trip_id
    )
    db.session.add(day)
    db.session.commit()
    return json.dumps({'success': True, 'data': day.serialize()})

@app.route('/api/day/<int:did>/', methods=['DELETE'])
def deleteDay(did):
    day = Day.query.filter_by(id=did).first()

    if not day:
        return json.dumps({'success': False, 'data': 'No such day exists'}), 404

    db.session.delete(day)
    db.session.commit()
    return json.dumps({'success': True, 'data': day.serialize()}), 201 

@app.route('/api/day/<int:did>/event/', methods=['POST'])
def addEvent(did):
    if not Day.query.filter_by(id=did).first():
        return json.dumps({'success': False, 'data': 'No such day exists'}), 404
    
    post_body = json.loads(request.data)
    name = post_body['name']
    location = post_body['location']
    time = post_body['time']
    directions = post_body['directions']
    note = post_body['note']

    event = Event(
        name=name,
        location=location,
        time=time,
        directions=directions,
        note=note,
        day_id=did
    )

    db.session.add(event)
    db.session.commit()

    return json.dumps({'success': True, 'data': event.serialize()})

@app.route('/api/event/<int:eid>/', methods=['POST'])
def deleteEvent(eid):
    event = Event.query.filter_by(id=eid).first()

    if not event:
        return json.dumps({'success': False, 'data': 'No such event exists'}), 404

    db.session.delete(event)
    db.session.commit()

    return json.dumps({'success': True, 'data': event.serialize()})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
