from app import app, db
from app.models import Faculty, Specialty, Course, Group

@app.shell_context_processor
def make_shell_context():
    return{
        'db': db, 
        'Faculty': Faculty,
        'Specialty': Specialty,
        'Course': Course,
        'Group': Group,
    }