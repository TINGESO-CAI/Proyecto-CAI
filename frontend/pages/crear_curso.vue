<template>
    <v-container class="test">
    <div class="home">
        <h1>Crear nuevo curso</h1>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >
                <v-col>
                <v-text-field
                    v-model="sence"
                    :rules="senceRules"
                    :counter="16"
                    label="codigo sence"
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
                <v-select
                  v-model="modalidad"
                  :items="modalidades"
                  item-text="modalidad"
                  label="modalidad"
                  persistent-hint
                  return-object
                  single-line   
                ></v-select>
                </v-col>

                <v-col>
                <v-select
                  v-model="categoria"
                  :items="categorias"
                  item-text="categoria"
                  label="categoria"
                  persistent-hint
                  return-object
                  single-line   
                ></v-select>
                </v-col>

                
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="horas_curso"
                    :rules="horas_cursoRules"
                    :counter="20"
                    label="horas_curso"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="valor_efectivo_participante"
                    :rules="valor_efectivo_participanteRules"
                    :counter="20"
                    label="Valor efec. participante"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="valor_imputable_participante"
                    :rules="valor_imputable_participanteRules"
                    :counter="20"
                    label="Valor imput. participante"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-select
                    v-model="estado"
                    :items="estados"
                    item-text="estado"
                    label="estado"
                    persistent-hint
                    return-object
                    single-line   
                ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="f_vigencia"
                    :rules="f_vigenciaRules"
                    :counter="20"
                    label="f_vigencia (YYYY-MM-DD)"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="resolucion_sence"
                    :rules="resolucion_senceRules"
                    :counter="20"
                    label="resolucion_sence"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="resolucion_usach"
                    :rules="resolucion_usachRules"
                    :counter="15"
                    label="resolucion_usach"
                    required
                ></v-text-field>
                </v-col>
              </v-row>
            </v-container>
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="createCurso">Crear</v-btn>
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
      estados : ["activo","inactivo"],
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
      paises: [ "Chilena","Extranjera"],
      modalidades: [ "presencial","e-learning","a distancia"],
      categorias: [ "sincrono","asincrono","presencial"],
      razones: ["ninguna"],
      //FORMULARIO
      valid: false,
      message:'',

      sence: '',
      nombre: '',
      modalidad: '',
      categoria: '',
      horas_curso: '',
      valor_efectivo_participante: '',
      valor_imputable_participante: '',
      estado: '',
      f_vigencia: '',     
      resolucion_sence: '',
      resolucion_usach: '',
      //reglas
      senceRules: [
        v => !!v || 'sence es requerido',
        v => v.length <= 12 || 'sence debe contener menos de 12 caracteres',
      ],
      nombreRules: [
        v => !!v || 'Nombre es requerido',
        v => v.length <= 100 || 'Nombre debe contener menos de 100 caracteres',
      ],
      horas_cursoRules: [
        v => !!v || 'horas_curso es requerido',
        v => v.length <= 3 || 'horas_curso debe contener menos de 3 caracteres',
        //v => v.max<100  || 'deben ser horas validas'
      ],
      valor_efectivo_participanteRules: [
        v => !!v || 'valor_efectivo_participante es requerido',
        v => v.length <= 100 || 'valor_efectivo_participante debe contener menos de 100 caracteres',
      ],
      valor_imputable_participanteRules: [
        v => !!v || 'valor_imputable_participante es requerido',
        v => v.length <= 100 || 'valor_imputable_participante debe contener menos de 100 caracteres',
      ],
      resolucion_senceRules: [
        v => !!v || 'resolucion_sence es requerido',
        v => v.length <= 100 || 'resolucion_sence debe contener menos de 100 caracteres',
      ],
      f_vigenciaRules: [
        v => !!v || 'f_vigencia es requerido',
        v => /.+.+/.test(v) || 'f_vigencia debe ser válido',
      ],
      resolucion_usachRules: [
        v => !!v || 'resolucion_usach es requerido',
        v => v.length <= 12 || 'resolucion_usach debe contener menos de 12 caracteres',
      ],
    }
  },
  methods:{
    
    successMessage:function(){
      alert("El curso se creo exitosamente.")
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
    async createCurso(){ //Crear un nuevo CURSO
      this.message = '';

      let newCurso ={
        sence: this.sence,
        nombre: this.nombre,
        modalidad: this.modalidad,
        categoria: this.categoria,
        horas_curso: this.transformarVacio(this.horas_curso),
        valor_efectivo_participante: this.transformarVacio(this.valor_efectivo_participante),
        valor_imputable_participante: this.transformarVacio(this.valor_imputable_participante),
        resolucion_sence: this.resolucion_sence,
        resolucion_usach: this.resolucion_usach,
        estado: this.transformarVacio(this.estado),
        f_vigencia: this.transformarVacio(this.f_vigencia)
      }
      if(this.sence!=''){
        if(this.comprobarFecha(this.f_vigencia) || this.f_vigencia==''){
          try {
            //se llama el servicio para crear un nuevo curso
            let response = await axios.post('http://localhost:5000/curso/agregar',newCurso);
            console.log('response', response.data);
            let id = response.data.id;
            this.message = `${this.sence} fue creado con éxito con id: ${id}`;
            
            //limpiar
            this.sence= ''
            this.nombre= ''
            this.modalidad= ''
            this.categoria= ''
            this.horas_curso= ''
            this.valor_efectivo_participante= ''
            this.valor_imputable_participante= ''
            this.estado= ''
            this.f_vigencia= ''
            this.resolucion_sence= ''
            this.resolucion_usach= ''
            if(response.data.respuesta=="El curso ya ha sido ingresado"){
              alert("El curso ya existe.")
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
          alert("Error en el formato de fecha")
        }
      }
      else{
        alert("Es necesario ingresar un sence.")
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