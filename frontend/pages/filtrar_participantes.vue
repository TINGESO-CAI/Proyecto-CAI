<template>
    <v-container class="test">
    <div class="home">
        <h1>Filtro de participantes</h1>
        <div> Llene solo los parametros que desea filtrar</div>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >
                <v-col>
                <v-text-field
                    v-model="rut"
                    :rules="rutRules"
                    :counter="16"
                    label="Rut"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="nombre"
                    :rules="nombreRules"
                    :counter="20"
                    label="Nombre"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="apellido_paterno"
                    :rules="apellido_paternoRules"
                    :counter="20"
                    label="Apellido paterno"
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="apellido_materno"
                    :rules="apellido_maternoRules"
                    :counter="20"
                    label="Apellido materno"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-select
                    v-model="genero"
                    :items="generos"
                    item-text="genero"
                    label="genero"
                    persistent-hint
                    return-object
                    single-line   
                ></v-select>
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
                    :rules="fecha_nacimientoRules"
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
                    :rules="ocupacionRules"
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
                    :rules="fonoRules"
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
      participantes : [],
      generos : ["masculino","femenino"],
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
      paises: [ "Chilena","Otra"],
      inscripciones: [ "presencial","online"],
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
      //reglas
      rutRules: [
        v => !!v || 'Rut es requerido',
        v => v.length <= 12 || 'Rut debe contener menos de 12 caracteres',
      ],
      nombreRules: [
        v => !!v || 'Nombre es requerido',
        v => v.length <= 100 || 'Nombre debe contener menos de 100 caracteres',
      ],
      apellido_paternoRules: [
        v => !!v || 'apellido_paterno es requerido',
        v => v.length <= 100 || 'apellido_paterno debe contener menos de 100 caracteres',
      ],
      apellido_maternoRules: [
        v => !!v || 'apellido_materno es requerido',
        v => v.length <= 100 || 'apellido_materno debe contener menos de 100 caracteres',
      ],
      correoRules: [
        v => !!v || 'Correo es requerido',
        v => /.+@.+/.test(v) || 'Correo debe ser válido',
      ],
      fecha_nacimientoRules: [
        v => !!v || 'fecha_nacimiento es requerido',
        //v => /.+.+/.test(v) || 'fecha_nacimiento debe ser válido',
      ],
      fonoRules: [
        v => !!v || 'fono es requerido',
        v => v.length <= 12 || 'fono debe contener menos de 12 caracteres',
      ],
      razon_socialRules: [
        v => !!v || 'razon_social es requerido',
        v => v.length <= 50 || 'razon_social debe contener menos de 50 caracteres',
      ],
    }
  },
  methods:{
    async getRazones(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/empresa/obtener/razon_social');
        this.razones = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    successMessage:function(){
      alert("El participante se creo exitosamente.")
    },

    async filtro(){ //Filtrar participantes
      
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
      console.log(newParticipante) 
      try {
        //se llama el servicio para crear un nuevo participante
        let response = await axios.get('http://localhost:5000/participante',newParticipante);
        this.participantes = response.data
        console.log('response', response.data);
               
        
        //limpiar
        this.nombre = '';
        this.rut = '';
        this.correo = '';
      }
      catch (error) {
       console.log('error', error); 
      }
    },
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