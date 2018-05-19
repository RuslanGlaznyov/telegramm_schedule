from app import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    spec = db.relationship('Specialty', backref='faculty',lazy='dynamic')

class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
    course = db.relationship('Course', backref='spec',lazy='dynamic')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    
    spec_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))

    group = db.relationship('Group', backref='cource',lazy='dynamic')

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    group_p = db.Column(db.String(128))
    
    cource  = db.Column(db.Integer, db.ForeignKey('course.id'))
