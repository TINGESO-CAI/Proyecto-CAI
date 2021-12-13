<template>
    <v-container class="test">
      <h1>Ver Participantes</h1>
      <br>
      <div>{{point}}
        <v-card>

            <v-data-table
              :headers="headers"
              :items="participantes"
            
            ></v-data-table>
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
    desserts: [
      {
        id: 'Frozen Yogurt',
        descrip: 159,
        cant_tareas: 6.0,

      },
      {
        id: 'Ice cream sandwich',
        descrip: 237,
        cant_tareas: 9.0,
      }
    ],
    created:function(){
      this.getParticipantes();
      this.getXRequisitos();
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
      },
      {
        rut: 'a',
        nombre: 'a',
        apellido_paterno: 'a',
        apellido_materno: 'a',
        genero: 'a',
        nivel_educacional: 'a',
        fecha_nacimiento: 'a',
        nacionalidad: 'a',
        tipo_inscripcion: 'a',
        ocupacion: 'a',
        correo: 'a',
        fono: 'a',
        razon_social: 'a',
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
        let response = await axios.get('http://localhost:5000/participante');
        this.participantes = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    async createParticipante(){ //Crear un nuevo PARTICIPANTE
      this.message = '';

      let newParticipante ={
        rut: this.rut,
        nombre: this.nombre,
        apellido_paterno: this.apellido_paterno,
        apellido_materno: this.apellido_materno,
        genero: this.genero,
        nivel_educacional: this.nivel_educacional,
        fecha_nacimiento: this.fecha_nacimiento,
        nacionalidad: this.nacionalidad,
        tipo_inscripcion: this.tipo_inscripcion,
        ocupacion: this.ocupacion,
        correo: this.correo,
        fono: this.fono,
        razon_social: this.razon_social
      }
      
      try {
        //se llama el servicio para crear un nuevo participante
        let response = await axios.post('http://localhost:5000/participante/agregar',newParticipante);
        console.log('response', response.data);
        let id = response.data.id;
        this.message = `${this.rut} fue creado con éxito con id: ${id}`;
        
        //limpiar
        this.nombre = '';
        this.rut = '';
        this.correo = '';
        this.successMessage();
      }
      catch (error) {
       console.log('error', error); 
       this.message = 'Ocurrió un error'
      }
    }
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