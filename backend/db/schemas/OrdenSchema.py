from ...server import ma
class OrdenSchema(ma.Schema):
    class Meta:
        fields = ('id_orden','sence',
        'cancelacion','fecha_emision','fecha_vencimiento')
        