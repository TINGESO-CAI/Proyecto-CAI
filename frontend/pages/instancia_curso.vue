<template>
    <v-container class="test">
        <h1 class="text-center">Ingrese sence del curso</h1>
        <v-autocomplete
                      v-model="sence"
                      :items="sences"
                      dense
                      filled 
                      rounded
                      item-text="sence"
                      label="sence"
                      persistent-hint
                      single-line
                      append-icon="mdi-magnify"
                      @click:append="buscar(sence)"
          ></v-autocomplete>
    <div v-if="curso.length==1">
        <v-container >
        <v-divider></v-divider>
        <v-row >
        <v-col>
        <h1 class="text-center"> Datos del curso</h1>
        <v-container class="half">
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Sence:</p>
                </v-col>                
                <v-col>
                        {{curso[0].sence}}
                </v-col>
                </v-row>
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Nombre:</p>
                </v-col>                
                <v-col>
                        {{curso[0].nombre}}
                </v-col>
                </v-row>
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Modalidad:</p>
                </v-col>                
                <v-col>
                        {{curso[0].modalidad}}
                </v-col>
                </v-row>
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Categoria:</p>
                </v-col>                
                <v-col>
                        {{curso[0].categoria}}
                </v-col>
                </v-row>
                 <v-row>
                <v-col>
                    <p class="font-weight-bold">Horas curso:</p>
                </v-col>                
                <v-col>
                        {{curso[0].horas_curso}}
                </v-col>
                </v-row>
                <v-row>
                
                </v-row>
        </v-container>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
        <h1 class="text-center">Ingrese datos de la instancia</h1>
        <v-container class="half"> 
            <v-form v-model="valid">
                
                <v-col>
                <v-text-field
                    v-model="direccion"
                    label="Direccion"
                    required
                ></v-text-field>
                </v-col>
                <v-row>    
                <v-col>
                <v-select
                  v-model="malla"
                  :items="mostrarMalla"
                  item-text="mostrarmalla"
                  label="Malla"
                  persistent-hint
                  return-object
                  single-line
                ></v-select>
                </v-col>
                </v-row>
                <v-col>
                <v-text-field
                    v-model="fecha_inicio"
                    label="Fecha de inicio (YYYY-MM-DD)"
                    required
                ></v-text-field>
                </v-col> 
                <v-col>
                <v-text-field
                    v-model="fecha_termino"
                    label="Fecha de termino (YYYY-MM-DD)"
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
                <v-col>
                <v-btn  color="blue lighten-1" class="mr-4" @click="crearInstancia">Crear Instancia</v-btn>
                </v-col>             
            </v-form>
        </v-container>
        </v-col>
        </v-row>
        </v-container>
    </div>
    <v-divider></v-divider>
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
  data:()=>( {
    curso:[],
    sence:'',
    sences:[],
    direccion:'',
    malla:'Malla',
    fecha_inicio:'',
    fecha_termino:'',
    estado:'',
    estados:["abierto","cerrado"],
    mostrarMalla:['Si','No']
  }),
  methods:{
    obtenerCurso: async function(value){
      let response= axios.get('http://localhost:5000/curso/obtener?sence='+value)
      return response
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
    crearInstancia:async function(){
      if(this.comprobarFecha(this.fecha_inicio) && this.comprobarFecha(this.fecha_termino)){ 
       try{
          if(this.malla=='Si'){
            this.malla=true
          }
          else if(this.malla=='No'){
            this.malla=false
          }
          else{
            this.malla=null
          }
          let response = await axios.post('http://localhost:5000/instancia/agregar',{sence: this.sence , direccion: this.transformarVacio(this.direccion) , malla: this.malla , fecha_inicio:this.transformarVacio(this.fecha_inicio) , fecha_termino:this.transformarVacio(this.fecha_termino),estado: this.estado})
          console.log(this.malla)
          console.log(response.data)
          alert("Instancia creada con exito")
          this.sence=''
          this.malla=''
          this.direccion=''
          this.fecha_inicio=''
          this.fecha_termino=''
          this.estado=''
          this.curso=[]
        }
        catch(error){
          console.log(error)
          alert("Ocurrio un error")
        }
      }
      else{
        alert("Error en formato de fecha.")
      }
    },
    async getSences(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/curso/obtener/sence');
        this.sences = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    buscar: async function(value){
      console.log(value)
      try{
        let response= await this.obtenerCurso(value)
        console.log(response.data)
        if(response.data.length !=1){
          alert('No existe curso.')
        }
        else{
          this.curso=response.data
        }
      }
      catch(error){
        console.log('error', error); 
      }
    },
    permisos:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://localhost:5000/cuenta/permisos?token='+data.token);
          return (response.data.nivel_acceso < 3)
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
  created: async function(){
    
    if(await this.permisos()){
      this.getSences();
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
  border-color: #4e99fc;
}
body{
	padding: 50px
}
.center {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50vh;
}
.half {
    width: 50%;
    height: 100%;
}
</style>