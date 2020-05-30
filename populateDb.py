import os
from flasksite import db
from flasksite.models import User, Park

if __name__ ==  '__main__':
    db.create_all()
