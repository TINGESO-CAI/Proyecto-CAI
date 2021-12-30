<template>
    <v-container class="test">
    <div class="home">
        <h1>Filtro de participantes</h1>
        <div v-if="participantes.length==0">
        <p class="text-center"> Llene solo los parametros que desea filtrar</p>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >
                <v-col>
                <v-text-field
                    v-model="rut"
                    :counter="16"
                    label="Rut"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="nombre"
                    :counter="20"
                    label="Nombre"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="apellido_paterno"
                    :counter="20"
                    label="Apellido paterno"
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="apellido_materno"
                    :counter="20"
                    label="Apellido materno"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-select
                    v-model="genero"
                    :items="geneross"
                    item-text="generos"
                    label="genero"
                    persistent-hint
                    return-object
                    single-line   
                >
                <template v-slot:[`item`]="{ item }">
                <span>{{ mostrarGenero(item) }}</span>
              </template></v-select>
                </v-col>

                <v-col>
                <v-select
                  v-model="nivel_educacional"
                  :items="nivelesEdu"
                  item-text="nivel_educacional"
                  label="nivel_educacional"
                  persistent-hint
                  return-object
                  single-line   
                ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="fecha_nacimiento"
                    :counter="20"
                    label="fecha_nacimiento"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-select
                  v-model="nacionalidad"
                  :items="paises"
                  item-text="nacionalidad"
                  label="nacionalidad"
                  persistent-hint
                  return-object
                  single-line   
                ></v-select>
                </v-col>

                <v-col>
                <v-select
                  v-model="tipo_inscripcion"
                  :items="inscripciones"
                  item-text="tipo_inscripcion"
                  label="tipo_inscripcion"
                  persistent-hint
                  return-object
                  single-line   
                ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="ocupacion"
                    :counter="20"
                    label="ocupacion"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="correo"
                    :rules="correoRules"
                    :counter="20"
                    label="correo"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fono"
                    :counter="15"
                    label="fono"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-select
                    v-model="razon_social"
                    :items="razones"
                    item-text="razon_social"
                    label="razon_social"
                    persistent-hint
                    return-object
                    single-line
                ></v-select>
                </v-col>
            </v-row>
            </v-container>
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="filtro">Filtrar</v-btn>
        </div>
        </div>
        <div v-else>
      <br>
        <div>
          <v-card>
              <v-data-table
                :headers="headers"
                :items="participantes"
                dense
              ><template v-slot:[`item.genero`]="{ item }">
                <span>{{ mostrarGenero(item.genero) }}</span>
              </template></v-data-table>
            </v-card>
        </div>
        <v-btn  color="blue lighten-1" class="mr-4" @click="limpiar">Limpiar</v-btn>
        </div>
    </div>
    </v-container>
</template>
<script>
//Importaciones

//librería axios
import axios from 'axios';

export default {
  name: 'Home',
  data:function(){
    return{

      correoRules: [
        v => !!v || 'Correo es requerido',
        v => /.+@.+/.test(v) || 'Correo debe ser válido',
      ],
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
      participantes : [],
      generos : ["femenino","masculino"],
      geneross : ["1","2"],
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
      paises: [ "Chile","Otra"],
      inscripciones: [ "Presencial","Online"],
      razones: ["ninguna"],
      //FORMULARIO
      valid: false,
      message:'',

      rut: '',
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      genero: '',
      nivel_educacional: '',
      fecha_nacimiento: '',
      nacionalidad: '',
      tipo_inscripcion: '',
      ocupacion: '',
      correo: '',
      fono: '',
      razon_social: '',
      
    }
  },
  methods:{
    async getRazones(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/empresa/obtener/razon_social');
        this.razones = response.data;
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    limpiar: function(){
      console.log(this.participantes)
      this.participantes=[]
    },
    empyMessage:function(){
      alert("No existen participantes con esas caracteristicas.")
    },

    async filtro(){ //Filtrar participantes
      
      try {
       let ruta = 'http://localhost:5000/participante/obtener?'
       if (this.rut != '' ){
         ruta= ruta + 'rut='+this.rut +'&'
       }
       if (this.nombre != '' ){
         ruta= ruta + 'nombre='+this.nombre +'&'
       }
       if (this.apellido_paterno != '' ){
         ruta= ruta + 'apellido_paterno='+this.apellido_paterno +'&'
       }
       if (this.apellido_materno != '' ){
         ruta= ruta + 'apellido_materno='+this.apellido_materno +'&'
       }
       if (this.genero != '' ){
         ruta= ruta + 'genero='+this.genero +'&'
       }
       if (this.nivel_educacional != '' ){
         ruta= ruta + 'nivel_educacional='+this.nivel_educacional +'&'
       }
       if (this.fecha_nacimiento != '' ){
         ruta= ruta + 'fecha_nacimiento='+this.fecha_nacimiento +'&'
       }
       if (this.nacionalidad != '' ){
         ruta= ruta + 'nacionalidad='+this.nacionalidad +'&'
       }
       if (this.tipo_inscripcion != '' ){
         ruta= ruta + 'tipo_inscripcion='+this.tipo_inscripcion +'&'
       }
       if (this.ocupacion != '' ){
         ruta= ruta + 'ocupacion='+this.ocupacion +'&'
       }
       if (this.correo != '' ){
         ruta= ruta + 'correo='+this.correo +'&'
       }
       if (this.fono != '' ){
         ruta= ruta + 'fono='+this.fono +'&'
       }
       if (this.razon_social != '' ){
         ruta= ruta + 'razon_social='+this.razon_social.razon_social
       }
      if (ruta[ruta.length -1] == '&'){
        ruta[ruta.length -1]==''
      }
      
      let response = await axios.get(ruta)
      this.participantes= response.data
      console.log('response', response.data);
               
      if(this.participantes.length==0){
        this.empyMessage()
      }
        //limpiar
        this.nombre = '';
        this.rut = '';
        this.correo = '';
        this.apellido_paterno=''
        this.apellido_materno=''
        this.tipo_inscripcion=''
        this.ocupacion=''
        this.genero=''
        this.razon_social=''
        this.fono=''
        this.nivel_educacional=''
        this.fecha_nacimiento=''
        this.nacionalidad=''
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
    this.getRazones();
  },

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