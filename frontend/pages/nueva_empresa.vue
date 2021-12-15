<template>
    <v-container class="test">
    <div class="home">
        <h1>Ingresar Nueva empresa</h1>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >

                <v-col>
                <v-text-field
                    v-model="razon_social"
                    :rules="razon_socialRules"
                    :counter="20"
                    label="razon_social"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="giro"
                    :rules="giroRules"
                    :counter="20"
                    label="Giro"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="atencion"
                    :rules="atencionRules"
                    :counter="20"
                    label="Atencion"
                    required
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-select
                    v-model="departamento"
                    :items="departamentos"
                    item-text="departamento"
                    label="departamento"
                    persistent-hint
                    return-object
                    single-line   
                ></v-select>
                </v-col>
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
                    v-model="direccion"
                    :rules="direccionRules"
                    :counter="20"
                    label="direccion"
                    required
                ></v-text-field>
                </v-col>
              </v-row>
    
              <v-row>
                <v-col>
                <v-text-field
                    v-model="comuna"
                    :rules="comunaRules"
                    :counter="20"
                    label="comuna"
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
                    :counter="15"
                    label="fono"
                    required
                ></v-text-field>
                </v-col>

            </v-row>
            </v-container>
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="createEmpresa">Crear</v-btn>
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
      departamentos : ["ingenieria","ciencias","humanidades"],
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
      paises: [ "Chilena","Otra"],
      razones: ["ninguna"],
      //FORMULARIO
      valid: false,
      message:'',

      
      razon_social: '',
      giro: '',
      atencion: '',
      departamento: '',
      rut: '',
      direccion: '',
      comuna: '',
      correo: '',
      fono: '',

      //reglas
      rutRules: [
        v => !!v || 'Rut es requerido',
        v => v.length <= 12 || 'Rut debe contener menos de 12 caracteres',
      ],
      razon_socialRules: [
        v => !!v || 'razon_social es requerido',
        v => v.length <= 100 || 'razon_social debe contener menos de 100 caracteres',
      ],
      giroRules: [
        v => !!v || 'giro es requerido',
        v => v.length <= 100 || 'giro debe contener menos de 100 caracteres',
      ],
      atencionRules: [
        v => !!v || 'atencion es requerido',
        v => v.length <= 100 || 'atencion debe contener menos de 100 caracteres',
      ],
      correoRules: [
        v => !!v || 'Correo es requerido',
        v => /.+@.+/.test(v) || 'Correo debe ser válido',
      ],
      direccionRules: [
        v => !!v || 'direccion es requerido',
        //v => /.+.+/.test(v) || 'direccion debe ser válido',
      ],
      fonoRules: [
        v => !!v || 'fono es requerido',
        v => v.length <= 12 || 'fono debe contener menos de 12 caracteres',
      ],
    }
  },
  methods:{
    successMessage:function(){
      alert("La empresa se creo exitosamente.")
    },

    async createEmpresa(){ //Crear un nuevo empresa
      this.message = '';

      let newEmpresa ={
        
        razon_social: this.razon_social,
        giro: this.giro,
        atencion: this.atencion,
        departamento: this.departamento,
        rut: this.rut,
        direccion: this.direccion,
        comuna: this.comuna,
        correo: this.correo,
        fono: this.fono
      }
      
      try {
        //se llama el servicio para crear una nueva empresa
        let response = await axios.post('http://localhost:5000/empresa/agregar',newEmpresa);
        console.log('response', response.data);
        let id = response.data.id;
        this.message = `${this.razon_social} fue creado con éxito con id: ${id}`;
        //limpiar
        this.successMessage();
      }
      catch (error) {
       console.log('error', error); 
       this.message = 'Ocurrió un error'
      }
    },
  },

  created(){
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