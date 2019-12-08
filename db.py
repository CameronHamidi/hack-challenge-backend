from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

# Your classes here

# trip_day_association = db.Table('trip_day_association', db.Model.metadata,
#     db.Column('tripId', db.Integer, db.ForeignKey('trip.id')),
#     db.Column('dayId', db.Integer, db.ForeignKey('day.id'))
# )

# day_event_association = db.Table('day_event_association', db.Model.metadata,
#     db.Column('dayId', db.Integer, db.ForeignKey('day.id')),
#     db.Column('eventId', db.Integer, db.ForeignKey('event.id'))
# )

class Trip(db.Model):
    __tablename__ = "trip"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    days = db.relationship('Day', cascade='delete')

    def __init(self, **kwargs):
      self.name = kwargs.get('name', '')
      self.location = kwargs.get('location', '')

    def serialize(self):
      return {
          'id': self.id,
          'name': self.name,
          'location': self.location,
          'days': [day.serialize() for day in self.days]
      }

class Day(db.Model):
  __tablename__ = "day"
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.String, nullable=False)
  location = db.Column(db.String, nullable=False)
  trip_id = db.Column(db.Integer, db.ForeignKey('trip.id'), nullable=False)
  events = db.relationship('Event', cascade='delete')

  def __init__(self, **kwargs):
    today = datetime.datetime.today()
    self.date = kwargs.get('date', today.strftime('%d/%m/%y'))
    self.location = kwargs.get('location', '')
    self.trip_id = kwargs.get('trip_id', 1)

  def serialize(self):
      return {
          'id': self.id,
          'date': self.date,
          'location': self.location,
          'trip_id': self.trip_id,
          'events': [event.serialize() for event in self.events]
      }

class Event(db.Model):
  __table__name = "event"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  location = db.Column(db.String, nullable=False)
  time = db.Column(db.String, nullable=False)
  directions = db.Column(db.String, nullable=False)
  note = db.Column(db.String, nullable=False)
  day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)

  def __init__(self, **kwargs):
    self.name = kwargs.get('name', '')
    self.location = kwargs.get('location', '')
    self.time = kwargs.get('time', '')
    self.directions = kwargs.get('directions', '')
    self.note = kwargs.get('note', '')
    self.day_id = kwargs.get('day_id', 1)

  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'location': self.location,
      'time': self.time,
      'directions': self.directions,
      'note': self.note,
      'day_id': self.day_id
    }

