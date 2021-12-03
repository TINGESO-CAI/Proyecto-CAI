from ...server import ma
class EmpresaSchema(ma.Schema):
    class Meta:
        fields = ('razon_social','giro',
        'atencion','departamento',
        'rut','direccion','comuna',
        'correo','fono')
        