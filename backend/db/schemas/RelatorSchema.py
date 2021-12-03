from ...server import ma
class RelatorSchema(ma.Schema):
    class Meta:
        fields = ('rut','nombre',
        'apellido_paterno','apellido_materno',
        'titulo','cv','fecha_nacimiento',
        'numero_cuenta','banco','tipo_cuenta')