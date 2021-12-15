<template>
<v-container class="test">
    <div v-if="page==1">
      <h1>Seleccione relatores</h1>
      <div>
        <v-data-table
          v-model="relatoresCurso"
          :headers="headers1"
          :items="relatores"
          item-key="rut"
          show-select
          @click:row="handleClick"
          class="elevation-1"
        >
        
        </v-data-table>
        <v-btn  color="blue lighten-1" class="mr-4" @click="escogerRelatores">Continuar</v-btn>
      </div>
    </div>
    <div v-else-if="page==2">
      <h1>Seleccione curso</h1>
      <div>
        <v-data-table
          v-model="curso"
          :headers="headers2"
          :items="cursos"
          item-key="sence"
          show-select
          single-select
          @click:row="handleClick"
          class="elevation-1"
        >
        
        </v-data-table>
        <v-btn  color="blue lighten-1" class="mr-4" @click="volver">Volver</v-btn>
        <v-btn  color="blue lighten-1" class="mr-4" @click="asignar">Asignar</v-btn>
      </div>
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
    headers1: [
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
    headers2: [
      {
        text: 'Sence',
        align: 'start',
        filterable: true,
        value: 'sence',
      },
      { text: 'nombre', value: 'nombre' },
      { text: 'modalidad', value: 'modalidad'},
      { text: 'categoria', value: 'categoria' },
      { text: 'horas_curso', value: 'horas_curso'},
  
    ],
		selectAll: false,
    page:1,
    relatores:[],
    relatoresCurso:[],
    cursos:[],
    curso:[]
  }),
  methods:{
    escogerRelatores: function(){
      if(this.relatoresCurso.length==0){
        alert('Debe seleccionar almenos 1 relator.')
      }
      else{
        this.page=2
      }
      
    },
    volver: function(){
      this.page=1
    },
    async matricular(){
      //let viejos=''
      for (var i=0; i< this.relatoresCurso.length; i++){
        try{
          let response = await axios.post('http://localhost:5000/relator_curso/agregar',{rut:this.relatoresCurso[i].rut, sence:this.curso[0].sence});
          console.log('response', response.data);
        }
        catch (error){
          console.log(error)
          alert('Ocurrio un error.')
        }
      }
      alert('Relatore/s asignado/s con exito.')
      this.relatoresCurso=[]
      this.curso=[]
      this.page=1
    },
    handleClick: function(value){
      console.log(value)
    },
    /*
    select: function() {
			this.matriculados = [];
			if (!this.selectAll) {
				for (let i in this.items) {
					this.matriculados.push(this.items[i].id);
				}
			}
		},
    */
    getRelatores: async function(){
      try {
        let response = await axios.get('http://localhost:5000/relator/obtener?');
        this.relatores = response.data;
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    getCursos: async function(){
      try {
        let response = await axios.get('http://localhost:5000/curso/obtener?');
        this.cursos = response.data;
      }
      catch (error) {
        console.log('error', error); 
      }
    },
  },
  created(){
    this.getRelatores()
    this.getCursos()
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
body{
	padding: 50px
}

</style>