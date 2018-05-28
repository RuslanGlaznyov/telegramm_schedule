from app import app, db
from app.models import Faculty, Specialty, Course, Group, Admin

@app.shell_context_processor
def make_shell_context():
    return{
        'db': db, 
        'Faculty': Faculty,
        'Specialty': Specialty,
        'Course': Course,
        'Group': Group,
        'Admin':Admin,
    }