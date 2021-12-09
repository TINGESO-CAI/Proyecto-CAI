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
                <v-text-field
                    v-model="genero"
                    :rules="generoRules"
                    :counter="20"
                    label="genero"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="nivel_educacional"
                    :rules="nivel_educacionalRules"
                    :counter="20"
                    label="nivel_educacional"
                    required
                ></v-text-field>
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
                <v-text-field
                    v-model="nacionalidad"
                    :rules="nacionalidadRules"
                    :counter="20"
                    label="nacionalidad"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="tipo_inscripcion"
                    :rules="tipo_inscripcionRules"
                    :counter="20"
                    label="tipo_inscripcion"
                    required
                ></v-text-field>
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
                    v-model="correo"
                    :rules="correoRules"
                    :counter="20"
                    label="correo"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fono"
                    :rules="fonoRules"
                    :counter="20"
                    label="fono"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="razon_social"
                    :rules="razon_socialRules"
                    :counter="20"
                    label="razon_social"
                    required
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
      /*FALTAN REGLAS
      nameRules: [
        v => !!v || 'Nombre es requerido',
        v => v.length <= 100 || 'Nombre debe contener menos de 100 caracteres',
      ],
      rutRules: [
        v => !!v || 'Rut es requerido',
        v => v.length <= 12 || 'Rut debe contener menos de 12 caracteres',
      ],
      emailRules: [
        v => !!v || 'E-mail es requerido',
        v => /.+@.+/.test(v) || 'E-mail debe ser válido',
      ],
      telefonoRules: [
        v => !!v || 'Teléfono es requerido',
        v => v.length <= 12 || 'Teléfono debe contener menos de 12 caracteres',
      ],*/
    }
  },
  methods:{
    successMessage:function(){
      alert("El participante se creo exitosamente.")
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
        let response = await axios.post('http://localhost:5000/crear_participante' ,newParticipante);
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