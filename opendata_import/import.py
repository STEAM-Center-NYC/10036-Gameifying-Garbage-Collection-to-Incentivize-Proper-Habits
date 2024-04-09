from flask import Flask, g
import pandas as pd
import pymysql
from dynaconf import Dynaconf

app = Flask(__name__)
settings = Dynaconf(settings_file=["settings.toml"])
app.secret_key = "eiewvrijvbeqdivjbnVQDKENWjneqwc"

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user=settings.db_user,
        password=settings.db_pass,
        database=settings.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/importdataGHOST')
def import_data():
    df = pd.read_csv("opendata_import/syringepharma.csv")

    cursor = g.db.cursor()

    for index, row in df.iterrows():
        print(row)
        # Extract the data from the row
        site_location = row['Site Location']
        zipcode = row['Zipcode']
        dsny_zone = row['DSNY Zone']
        dsny_district = row['DSNY District']
        latitude = row['Latitude']
        longitude = row['Longitude']
        bin_type = row['BinType']

        # Prepare the SQL query to insert the data into the database
        sql = f"INSERT INTO Bins (SiteLocation, Zipcode, DSNYZone, DSNYDistrict, Latitude, Longitude, BinType) VALUES ('{site_location}', '{zipcode}', '{dsny_zone}', '{dsny_district}', '{latitude}', '{longitude}', '{bin_type}')"

        # Execute the SQL query
        cursor.execute(sql)

    return 'Data imported successfully!'

if __name__ == "__main__":
    app.run(debug=True)
