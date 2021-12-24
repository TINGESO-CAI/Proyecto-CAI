<template>
    <v-container class="test">
        <h1 class="text-center">Ingrese sence del curso</h1>
        <v-text-field
            hide-details 
            v-model="sence"
            label="Sence"
            filled 
            rounded 
            dense 
            single-line 
            append-icon="mdi-magnify"
            class="center"
            @click:append="buscar(sence)"
        ></v-text-field>
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
                <v-col>
                    <p class="font-weight-bold">Estado:</p>
                </v-col>                
                <v-col>
                        {{curso[0].estado}}
                </v-col>
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
                <v-col>
                <v-text-field
                    v-model="malla"
                    label="Malla"
                    required
                ></v-text-field>
                </v-col>  
                <v-col>
                <v-text-field
                    v-model="fecha_inicio"
                    label="Fecha de inicio"
                    required
                ></v-text-field>
                </v-col> 
                <v-col>
                <v-text-field
                    v-model="fecha_termino"
                    label="Fecha de termino"
                    required
                ></v-text-field>
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

export default {
  data:()=>( {
    page:1,
    curso:[1],
    sense:''
  }),
  methods:{
    escogerParticipantes: function(){
      if(this.matriculados.length!=1){
        alert('Debe seleccionar almenos 1 participante para matricular')
      }
      else{
        this.page=2
      }
      
    },
    obtenerCurso: async function(value){
      let response= axios.get('http://localhost:5000/curso/obtener?sence='+value)
      return response
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