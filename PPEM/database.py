import psycopg2
from psycopg2 import Error
import pandas as pd

class postgreSQL_database:

	def __init__(self, credentials):
		self.credentials = credentials


	def query(self, object_id):
	    try:
	        connection = psycopg2.connect(**self.credentials)

	        cursor = connection.cursor()
	        cursor.execute(
	            'select oid, candid, mjd, fid, magpsf, sigmapsf, magpsf_corr, sigmapsf_corr_ext from detection where oid = %s', (object_id,))
	        results = cursor.fetchall()

	    except (Exception, Error) as error:
	        print("Error while connecting to PostgreSQL", error)
	    finally:
	        if connection:
	            cursor.close()
	            connection.close()
	            print("PostgreSQL connection is closed")
	    return pd.DataFrame(
	        results, 
	        columns=['oid', 'candoid','mjd','fid', 'magpsf', 'sigmapsf', 'magpsf_corr', 'sigmapsf_corr_ext']).set_index("oid")