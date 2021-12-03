from ...server import ma
class FacturaSchema(ma.Schema):
    class Meta:
        fields = ('id_factura','num_registro',
        'estado','tipo_pago',
        'num_hes','fecha_emision','fecha_vencimiento')
        