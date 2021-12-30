<template>
    <v-container class="test" >
      <h1>Ver Participantes</h1>
      <br>
      <div>{{point}}
        <v-card>
            <v-data-table
              :headers="headers"
              :items="participantes"
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
        text: 'Rut',
        align: 'start',
        filterable: true,
        value: 'rut',
      },
      { text: 'nombre', value: 'nombre' },
      { text: 'apellido_paterno', value: 'apellido_paterno'},
      { text: 'apellido_materno', value: 'apellido_materno' },
      { text: 'correo', value: 'correo'},
      { text: 'fono', value: 'fono'},
      { text: 'razon_social', value: 'razon_social'},
      { text: 'genero', value: 'genero'},
  
    ],
    created:function(){
      this.getParticipantes();
      this.getIdData();
    },
    participantes:[
      {     
        rut: null,
        nombre: null,
        apellido_paterno: null,
        apellido_materno: null,
        genero: null,
        nivel_educacional: null,
        fecha_nacimiento: null,
        nacionalidad: null,
        tipo_inscripcion: null,
        ocupacion: null,
        correo: null,
        fono: null,
        razon_social: null,
      }
    ],

    rut: null,
    nombre: null,
    apellido_paterno: null,
    apellido_materno: null,
    genero: null,
    nivel_educacional: null,
    fecha_nacimiento: null,
    nacionalidad: null,
    tipo_inscripcion: null,
    ocupacion: null,
    correo: null,
    fono: null,
    razon_social: null,
  }),
  methods:{
    forEach: async function(){

    },
    getParticipantes: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/participante/obtener?');
        this.participantes = response.data;

        
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
    this.getParticipantes()
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