import psycopg2
import sys, os
import numpy as np
import pandas as pd
import db.credenciales as creds
import db.schemas.Participante as Participante
import db.schemas.Relator as Relator
import db.schemas.Orden as Orden
import db.schemas.Factura as Factura
import db.schemas.Empresa as Empresa
import db.schemas.Curso as Curso
import pandas.io.sql as psql

# Set up a connection to the postgres server.
conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
+" password="+ creds.PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cursor = conn.cursor()
