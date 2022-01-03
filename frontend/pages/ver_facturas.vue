<template>
    <v-container class="test" >
      <h1>Ver Facturas</h1>
      <br>
      <div>{{point}}
        <v-card>
            <v-data-table
              :headers="headers"
              :items="facturas"
              dense
            >
              <template v-slot:[`item.genero`]="{ item }">
                <span>{{ mostrarGenero(item.genero) }}</span>
              </template>
            </v-data-table>
          </v-card>
      </div>
    
    </v-container>
</template>
<script>
//Importaciones

//librería axios
import axios from 'axios';
export default {

  data:()=>( {
    busqueda: null,
    generos:['-','femenino','masculino'],
    headers: [
      {
        text: 'id_factura',
        align: 'start',
        filterable: true,
        value: 'id_factura',
      },
      { text: 'num_registro', value: 'num_registro' },
      { text: 'estado', value: 'estado'},
      { text: 'tipo_pago', value: 'tipo_pago' },
      { text: 'correo', value: 'correo'},
      { text: 'num_hes', value: 'num_hes'},
      { text: 'razon_social', value: 'razon_social'},
      { text: 'genero', value: 'genero'},
  
    ],
    created:function(){
      this.getFacturas();
      this.getIdData();
    },
    facturas:[
      {     
        id_factura: null,
        num_registro: null,
        estado: null,
        tipo_pago: null,
        num_hes: null,
        fecha_emision: null,
        fecha_vencimiento: null,
        sence: null,
        
      }
    ],

    id_factura: null,
    num_registro: null,
    estado: null,
    tipo_pago: null,
    nivel_educacional: null,
    
    nacionalidad: null,
    tipo_inscripcion: null,
    fecha_emision: null,
    sence: null,
    correo: null,
    num_hes: null,
    razon_social: null,
  }),
  methods:{
    forEach: async function(){

    },
    getFacturas: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/factura/obtener?');
        this.facturas = response.data;

        
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    mostrarGenero(valor){
      if (valor == '1' ) return 'femenino'
      else if (valor == '2' ) return 'masculino'
      else return 'desconocido'
    },
  },
  created(){
    this.getFacturas()
    //this.mostrarGenero(valor)
  }
}
</script>
<style>
.home{
  display:flex;
  flex-direction: column;
  align-items: center;
}
.test{
  border-top: 3px solid;
  border-bottom: 3px solid;
  border-color: #4e99fc
}

</style>