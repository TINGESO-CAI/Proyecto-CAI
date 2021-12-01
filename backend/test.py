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
from sqlalchemy import create_engine

# Set up a connection to the postgres server.
conn_string = "host="+ creds.PGHOST +" port="+ "5432" +" dbname="+ creds.PGDATABASE +" user=" + creds.PGUSER \
+" password="+ creds.PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cursor = conn.cursor()
def insertarDatos(df,tabla):
	for index, row in df.iterrows():
		insertdata = "('"
		i=0
		while i<len(row)-1:
			if str(row[i])=="nan":
				insertdata += str("NULL")+"','"
			else:
				insertdata += str(row[i])+"','"
			i+=1
		insertdata+=str(row[i])+"')"
		print("insertdata :",insertdata)
		try:
			cursor.execute("INSERT INTO "+tabla+" values "+insertdata)
			print( "row inserted:", insertdata)
		except psycopg2.IntegrityError:
			print( "Row already exist ")
			pass
		except Exception as e:
			print( "some insert error:", e, "ins: ", insertdata)
		conn.commit()

def procesamiento(archivo):
	txt='db/data/'+archivo+'.xlsx'
	df = pd.ExcelFile(txt)
	df = df. parse(df.sheet_names[0])
	return df


df=procesamiento("empresa")
insertarDatos(df,"empresa")
df=procesamiento("participante")
df["genero"]=pd.to_numeric(df["genero"],downcast= 'integer')
insertarDatos(df,"participante")
df=procesamiento("orden")
df["id_orden"]=pd.to_numeric(df["id_orden"],downcast= 'integer')
df["cancelacion"]=pd.to_numeric(df["cancelacion"],downcast= 'integer')
insertarDatos(df,"orden")
df=procesamiento("curso")
df["sence"]=pd.to_numeric(df["sence"],downcast= 'integer')
df["resolucion_sence"]=pd.to_numeric(df["resolucion_sence"],downcast= 'integer')
df["resolucion_usach"]=pd.to_numeric(df["resolucion_usach"],downcast= 'integer')
df["horas_curso"]=pd.to_numeric(df["horas_curso"],downcast= 'integer')
df["valor_efectivo_participante"]=pd.to_numeric(df["valor_efectivo_participante"],downcast= 'integer')
df["valor_imputable_participante"]=pd.to_numeric(df["valor_imputable_participante"],downcast= 'integer')
insertarDatos(df,"curso")
df=procesamiento("participante_orden")
df["id_orden"]=pd.to_numeric(df["id_orden"],downcast= 'integer')
insertarDatos(df,"participante_orden")
df=procesamiento("participante_curso")
df["sence"]=pd.to_numeric(df["sence"],downcast= 'integer')
insertarDatos(df,"participante_curso")