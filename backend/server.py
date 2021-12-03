from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import db.modelos.Participante as Participante
import db.modelos.Relator as Relator
import db.modelos.Orden as Orden
import db.modelos.Factura as Factura
import db.modelos.Empresa as Empresa
import db.modelos.Curso as Curso
import db.schemas.ParticipanteSchema as ParticipanteSchema
import db.schemas.RelatorSchema as RelatorSchema
import db.schemas.OrdenSchema as OrdenSchema
import db.schemas.FacturaSchema as FacturaSchema
import db.schemas.EmpresaSchema as EmpresaSchema
import db.schemas.CursoSchema as CursoSchema
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cai"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow
@app.route('/api/v1.0/test')
def test():
	return jsonify("Probando a ver si devuelve2")
if __name__ == '__main__':
	app.run(debug=True)