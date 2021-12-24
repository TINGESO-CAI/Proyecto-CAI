<template>
<v-container class="test">
    <div v-if="page==1">
      <h1>Seleccione participantes</h1>
      <div>
        <v-container >
        <v-row >
        <v-col>
        <v-text-field
            hide-details 
            v-model="rut"
            label="Rut"
            filled 
            rounded 
            dense 
            single-line 
            append-icon="mdi-account-plus"
            class="shrink mx-4"
            @click:append="agregarParticipante(rut)"
        ></v-text-field>
        </v-col>
        </v-row>
        </v-container>
      <v-data-table :headers="headers1" :items="matriculados">
      <template v-slot:item="row">
          <tr>
            <td>{{row.item.rut}}</td>
            <td>{{row.item.nombre}}</td>
            <td>{{row.item.apellido_paterno}}</td>
            <td>{{row.item.apellido_materno}}</td>
            <td>{{row.item.correo}}</td>
            <td>{{row.item.fono}}</td>
            <td>{{row.item.razon_social}}</td>
            <td>{{row.item.nacionalidad}}</td>
            <td>
                <v-btn class="mx-2" fab dark small color="red" @click="handleClick(row.item)">
                    <v-icon dark>mdi-account-minus</v-icon>
                </v-btn>
            </td>
          </tr>
      </template>
    </v-data-table>

        <!--
        <v-data-table
          v-model="matriculados"
          :headers="headers1"
          :items="participantes"
          item-key="rut"
          @click:row="handleClick"
          class="elevation-1"
        >
        <tr>
        <v-btn  color="blue lighten-1" class="mr-4" @click="volver">Volver</v-btn>
        </tr>
        </v-data-table>
        !-->
        <v-btn  color="blue lighten-1" class="mr-4" @click="escogerParticipantes">Continuar</v-btn>
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
        <v-btn  color="blue lighten-1" class="mr-4" @click="matricular">Matricular</v-btn>
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
    matriculados:[],
    cursos:[],
    curso:[],
    rut:''
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
    volver: function(){
      this.page=1
    },
    async matricular(){
      //let viejos=''
      for (var i=0; i< this.matriculados.length; i++){
        try{
          let response = await axios.post('http://localhost:5000/participante_curso/agregar',{rut:this.matriculados[i].rut, sence:this.curso[0].sence});
          console.log('response', response.data);
        }
        catch (error){
          console.log(error)
          alert('Ocurrio un error.')
        }
      }
      alert('Participante/s inscrito/s con exito.')
      this.matriculados=[]
      this.curso=[]
      this.page=1
    },
    handleClick: function(value){
      console.log(value)
      var index = this.matriculados.indexOf(value);
      if (index !== -1) {
        this.matriculados.splice(index, 1);
      }
      console.log(index)
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
    getParticipantes: async function(){
      try {
        let response = await axios.get('http://localhost:5000/participante/obtener?');
        this.participantes = response.data;
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
    obtenerParticipante: async function(value){
      let response= axios.get('http://localhost:5000/participante/obtener?rut='+value)
      return response
    },
    agregarParticipante: async function(value){
      try{
        console.log(value)
        let response= await this.obtenerParticipante(value)
        console.log('la data es ',response.data)
        if(response.data.length == 0){
          alert('No existe participante.')
        }
        else{
          this.matriculados.push(response.data[0])
          console.log('la respuesta es: ',response.data[0])
        }
      }
      catch(error){
        console.log('error', error); 
      }
    }
  },
  created(){
    this.getParticipantes()
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