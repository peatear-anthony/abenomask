import os
import csv
import pandas as pd
from random import randrange
from flasksite import db
from flasksite.models import User, Park



if __name__ ==  '__main__':
    # Create New DB
    db.create_all()

    # Load data from csv
    df_park = pd.read_csv('data/park.csv')
    for index, row in df_park.iterrows():
        park = Park(
            name=row['name'],
            prefecture=row['prefecture'],
            area=row['area'],
            lat=row['lat'],
            lon=row['lon'],
            capacity=row['capacity'],
            count = randrange(5)
            )
        db.session.add(park)
        db.session.commit()
        
    df_user = pd.read_csv('data/user.csv')
    print(df_user.head())
    for index, row in df_user.iterrows():
        user = User(
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            postal_code=row['postal_code'],
            prefecture =row['prefecture'],
            my_number=row['my_number'],
            email=row['email'],
            password=row['password'],
            )
        db.session.add(user)
        db.session.commit()
            











