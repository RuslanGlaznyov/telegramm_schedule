from app import db

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    entity = db.Column(db.String(128), default="faculty")
    spec = db.relationship('Specialty', backref='faculty',lazy='dynamic')
    
    def __str__(self):
        return self.name

class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    entity = db.Column(db.String(128), default="specialty")
        
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
    course = db.relationship('Course', backref='spec',lazy='dynamic')

    def __str__(self):
        return self.name

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_course = db.Column(db.Integer)
    entity = db.Column(db.String(128), default="course")
    

    spec_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))

    group = db.relationship('Group', backref='cource',lazy='dynamic')

    def __str__(self):
        return str(self.number_of_course) + " "+str(self.spec) 

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_of_group = db.Column(db.String(128))
    group_p = db.Column(db.String(128))
    entity = db.Column(db.String(128), default="group")
    

    cource_id  = db.Column(db.Integer, db.ForeignKey('course.id'))

    users = db.relationship('User', backref='group',lazy='dynamic')

    def __str__(self):
        return str(self.number_of_group)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(128))

    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    