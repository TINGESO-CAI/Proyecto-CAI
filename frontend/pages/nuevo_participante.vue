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
                    :counter="20"
                    label="fecha_nacimiento <YYYY-MM-DD>"
                    
                ></v-text-field>
                </v-col>

                <v-col>
                <v-autocomplete
                  v-model="nacionalidad"
                  :items="paises"
                  item-text="nacionalidad"
                  label="nacionalidad"
                  persistent-hint
                  return-object
                  single-line   
                ></v-autocomplete>
                </v-col>

                <v-col>
                <v-autocomplete
                  v-model="tipo_inscripcion"
                  :items="inscripciones"
                  item-text="tipo_inscripcion"
                  label="tipo_inscripcion"
                  persistent-hint
                  return-object
                  single-line   
                ></v-autocomplete>
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
                    v-model="correo_personal"
                    :rules="correo_personalRules"
                    :counter="30"
                    label="correo_personal"
                    
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fono_personal"
                    :rules="fono_personalRules"
                    :counter="15"
                    label="fono_personal"
                    
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
axios.interceptors.request.use(function (config) {
  let data=localStorage.getItem("user")
  data=JSON.parse(data)
  config.headers = {
  'token': data.token}
  return config;
}, function (error) {
// Do something with request error
   return Promise.reject(error);
});
export default {
  name: 'Home',
  data:function(){
    return{
      generos : ["masculino","femenino"],
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otra"],
      paises: [ "Chile","Desconocido","Afganistán","Albania","Alemania","Andorra","Angola","Antigua y Barbuda","Arabia Saudita","Argelia","Argentina","Armenia","Australia","Austria","Azerbaiyán","Bahamas","Bangladés","Barbados","Baréin","Bélgica","Belice","Benín","Bielorrusia","Birmania","Bolivia","Bosnia y Herzegovina","Botsuana","Brasil","Brunéi","Bulgaria","Burkina Faso","Burundi","Bután","Cabo Verde","Camboya","Camerún","Canadá","Catar","Chad","China","Chipre","Ciudad del Vaticano","Colombia","Comoras","Corea del Norte","Corea del Sur","Costa de Marfil","Costa Rica","Croacia","Cuba","Dinamarca","Dominica","Ecuador","Egipto","El Salvador","Emiratos Árabes Unidos","Eritrea","Eslovaquia","Eslovenia","España","Estados Unidos","Estonia","Etiopía","Filipinas","Finlandia","Fiyi","Francia","Gabón","Gambia","Georgia","Ghana","Granada","Grecia","Guatemala","Guyana","Guinea","Guinea ecuatorial","Guinea-Bisáu","Haití","Honduras","Hungría","India","Indonesia","Irak","Irán","Irlanda","Islandia","Islas Marshall","Islas Salomón","Israel","Italia","Jamaica","Japón","Jordania","Kazajistán","Kenia","Kirguistán","Kiribati","Kuwait","Laos","Lesoto","Letonia","Líbano","Liberia","Libia","Liechtenstein","Lituania","Luxemburgo","Madagascar","Malasia","Malaui","Maldivas","Malí","Malta","Marruecos","Mauricio","Mauritania","México","Micronesia","Moldavia","Mónaco","Mongolia","Montenegro","Mozambique","Namibia","Nauru","Nepal","Nicaragua","Níger","Nigeria","Noruega","Nueva Zelanda","Omán","Países Bajos","Pakistán","Palaos","Palestina","Panamá","Papúa Nueva Guinea","Paraguay","Perú","Polonia","Portugal","Reino Unido","República Centroafricana","República Checa","República de Macedonia","República del Congo","República Democrática del Congo","República Dominicana","República Sudafricana","Ruanda","Rumanía","Rusia","Samoa","San Cristóbal y Nieves","San Marino","San Vicente y las Granadinas","Santa Lucía","Santo Tomé y Príncipe","Senegal","Serbia","Seychelles","Sierra Leona","Singapur","Siria","Somalia","Sri Lanka","Suazilandia","Sudán","Sudán del Sur","Suecia","Suiza","Surinam","Tailandia","Tanzania","Tayikistán","Timor Oriental","Togo","Tonga","Trinidad y Tobago","Túnez","Turkmenistán","Turquía","Tuvalu","Ucrania","Uganda","Uruguay","Uzbekistán","Vanuatu","Venezuela","Vietnam","Yemen","Yibuti","Zambia","Zimbabue"],
      inscripciones:["presencial","online"],
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
        let response = await axios.get('http://52.188.153.77:5000/empresa/obtener/razon_social');
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
    comprobarTelefono(fono){
      if (fono==''){
        return true
      }
      if(fono.length!=9){
        if(fono[0]=='+' && fono.length==12){
          return true
        }
        else{
          return false
        }
      }
      else{
        if(fono[0]!='+'){
          return true
        }
        else{
          return false
        }
      }
    },
    successMessage:function(){
      alert("El participante se creo exitosamente.")
    },
    comprobarFecha:function(fecha){
      if (fecha.split('-').length == 3 || fecha==''){
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
    validaRut : function (rutCompleto) {
		if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test( rutCompleto ))
			return false;
		var tmp 	= rutCompleto.split('-');
		var digv	= tmp[1]; 
		var rut 	= tmp[0];
		if ( digv == 'K' ) digv = 'k' ;
		return (this.dv(rut) == digv );
    },
    dv : function(T){
      var M=0,S=1;
      for(;T;T=Math.floor(T/10))
        S=(S+T%10*(9-M++%6))%11;
      return S?S-1:'k';
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
      if(this.validaRut(this.rut)){//this.rut.split('-').length==2){
        if(this.comprobarTelefono(this.fono_personal)==false || this.comprobarTelefono(this.fono_corporativo)==false){
          alert("Error en formato de telefono.")
          return 0
        }
        if(this.comprobarFecha(this.fecha_nacimiento) || this.fecha_nacimiento==''){         
          try {
            //se llama el servicio para crear un nuevo participante
            let response = await axios.post('http://52.188.153.77:5000/participante/agregar',newParticipante);
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
        alert("Debe ingresar un rut valido.")
      }
    },
    mostrarGenero(valor){
      if (valor == '1' ) return 'femenino'
      else if (valor == '2' ) return 'masculino'
      else return 'desconocido'
    },
    permisos:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://52.188.153.77:5000/cuenta/permisos?token='+data.token);
          return (response.data.nivel_acceso <3)
        }
        catch(error){
          console.log(error)
        }
      }
      else{
        return false
      }
    },
    
  },

  created:async function(){
    if(await this.permisos()){
      this.getRazones();
    }
    else{
      window.location.href='/'
    }
    
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