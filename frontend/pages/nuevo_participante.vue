<template>
    <v-container class="test">
    <div class="home">
        <h1>Ingresar Nuevo participante</h1>
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
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="nombre"
                    :rules="nombreRules"
                    :counter="20"
                    label="Nombre"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="apellido_paterno"
                    :rules="apellido_paternoRules"
                    :counter="20"
                    label="Apellido paterno"
                    required
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
                    required
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
                    required
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
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="correo_personal"
                    :rules="correo_personalRules"
                    :counter="30"
                    label="correo_personal"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fono_personal"
                    :rules="fono_personalRules"
                    :counter="15"
                    label="fono_personal"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-autocomplete
                      v-model="razon_social"
                      :items="razones"
                      dense
                      item-text="razon_social"
                      label="razon_social"
                      persistent-hint
                      return-object
                      single-line
                ></v-autocomplete>
                </v-col>
            </v-row>

            <v-row>
              <v-col>
              <v-text-field
                      v-model="correo_corporativo"
                      :rules="correo_corporativoRules"
                      :counter="20"
                      label="correo_corporativo"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="fono_corporativo"
                    :rules="fono_corporativoRules"
                    :counter="15"
                    label="fono_corporativo"
                ></v-text-field>
                </v-col>
            </v-row>
            </v-container> 
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="createParticipante">Crear</v-btn>
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
      generos : ["masculino","femenino"],
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otra"],
      paises: [ "Chilena","Extranjera"],
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
      correo_corporativo: '',
      correo_personal: '',
      fono_personal: '',
      fono_corporativo: '',
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
      correo_corporativoRules: [
        v => !!v || 'Correo es requerido',
        v => /.+@.+/.test(v) || 'Correo debe ser válido',
      ],
      correo_personalRules: [
        v => !!v || 'Correo es requerido',
        v => /.+@.+/.test(v) || 'Correo debe ser válido',
      ],
      fecha_nacimientoRules: [
        v => !!v || 'fecha_nacimiento es requerido',
        //v => /.+.+/.test(v) || 'fecha_nacimiento debe ser válido',
      ],
      fono_personalRules: [
        v => !!v || 'fono es requerido',
        v => v.length <= 12 || 'fono debe contener menos de 12 caracteres',
      ],
      fono_corporativoRules: [
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
    mostrarGenero(valor){
      if (valor == '1' ) return 'femenino'
      else if (valor == '2' ) return 'masculino'
      else return 'desconocido'
    },
    cambiarGenero(valor){
      if (valor == 'femenino' ) return '1'
      else if (valor == 'masculino' ) return '2'
      else return ''
    },
    successMessage:function(){
      alert("El participante se creo exitosamente.")
    },
    comprobarFecha:function(fecha){
      if (fecha.split('-').length == 3){
        return true
      }
      else{
        return false
      }
    },

    transformarVacio: function(valor){
      if(valor==''){
        return null
      }
      else{
        return valor
      }
    },
    async createParticipante(){ //Crear un nuevo PARTICIPANTE
      this.message = '';

      let newParticipante ={
        rut: this.rut,
        nombre: this.transformarVacio(this.nombre),
        apellido_paterno: this.transformarVacio(this.apellido_paterno),
        apellido_materno: this.transformarVacio(this.apellido_materno),
        genero: this.transformarVacio(this.cambiarGenero(this.genero)),
        nivel_educacional: this.transformarVacio(this.nivel_educacional),
        fecha_nacimiento: this.transformarVacio(this.fecha_nacimiento),
        nacionalidad: this.transformarVacio(this.nacionalidad),
        tipo_inscripcion: this.transformarVacio(this.tipo_inscripcion),
        ocupacion: this.transformarVacio(this.ocupacion),
        fono_personal: this.transformarVacio(this.fono_personal),
        fono_corporativo: this.transformarVacio(this.fono_corporativo),
        correo_corporativo: this.transformarVacio(this.correo_corporativo),
        correo_personal: this.transformarVacio(this.correo_personal),
        razon_social: this.transformarVacio(this.razon_social)
      }
      if(this.rut.split('-').length==2){
        if(this.comprobarFecha(this.fecha_nacimiento) || this.fecha_nacimiento==''){         
          try {
            //se llama el servicio para crear un nuevo participante
            let response = await axios.post('http://localhost:5000/participante/agregar',newParticipante);
            console.log('response', response.data);
            let id = response.data.id;
            this.message = `${this.rut} fue creado con éxito con id: ${id}`;
            
            //limpiar
            this.rut= ''
            this.nombre= ''
            this.apellido_paterno= ''
            this.apellido_materno= ''
            this.genero= ''
            this.nivel_educacional= ''
            this.fecha_nacimiento= ''
            this.nacionalidad= ''
            this.tipo_inscripcion= ''
            this.ocupacion= ''
            this.correo_corporativo= ''
            this.correo_personal= ''
            this.fono_personal= ''
            this.fono_corporativo= ''
            this.razon_social= ''
            if(response.data.respuesta=="El participante ya ha sido ingresado"){
              alert("El participante ya existe.")
            }
            else{
              this.successMessage();
            }
          }
          catch (error) {
          console.log('error', error); 
          this.message = 'Ocurrió un error'
          }
        }
        else{
          alert("Error formato fecha.")
        }
      }
      else{
        alert("Debe ingresar el rut de manera correcta")
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