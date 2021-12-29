<template>
    <v-container class="test">
      <div v-if="page==1">
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
        <v-btn v-if="instancias.length!=0" color="blue lighten-1" class="mr-4" @click="avanzarPage2">Continuar</v-btn>
      </div>
    <div v-else-if="page==2">
      <h1>Seleccione Instancia</h1>
      <div>
        <v-data-table
          v-model="instancia"
          :headers="headers"
          :items="instancias"
          item-key="id_instancia"
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
    <div v-else-if="page==3">
      <v-container >
        <v-divider></v-divider>
        <v-row >
        <v-col>
        <h1 class="text-center"> Datos del curso/instancia</h1>
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
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Id Instancia:</p>
                </v-col>               
                <v-col>
                        {{instancia[0].id_instancia}}
                </v-col>
                
                </v-row>
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Dirección:</p>
                </v-col>               
                <v-col>
                        {{instancia[0].direccion}}
                </v-col>
                
                </v-row>
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Fecha inicio:</p>
                </v-col>               
                <v-col>
                        {{instancia[0].fecha_inicio}}
                </v-col>
                
                </v-row>
                <v-row>
                <v-col>
                    <p class="font-weight-bold">Fecha termino:</p>
                </v-col>               
                <v-col>
                        {{instancia[0].fecha_termino}}
                </v-col>
                
                </v-row>

        </v-container>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col>
        <h1 class="text-center">Ingrese datos de la factura</h1>
        <v-container class="half"> 
            <v-form v-model="valid">
                  <input type="radio" id="0" value="0" v-model="enviar">
                  <label for="0">Usach</label>
                  <input type="radio" id="1" value="1" v-model="enviar">
                  <label for="1">Empresa</label>
                  <input type="radio" id="2" value="2" v-model="enviar">
                  <label for="2">Otro</label>
                <v-col>
                <v-text-field
                    v-model="otic"
                    label="Numero Otic"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="razon_social"
                    label="Razon social"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-if="enviar==2"
                    v-model="observacion"
                    label="Observación"
                    required
                ></v-text-field>
                </v-col> 
                <v-row>
                <v-btn  color="blue lighten-1" class="mr-4" @click="volver">Volver</v-btn>

                <v-btn  color="blue lighten-1" class="mr-4" @click="continuarPage4">Continuar</v-btn>
                </v-row>         
            </v-form>
        </v-container>
        </v-col>
        </v-row>
        </v-container>
        <v-divider></v-divider>
    </div>
    <div v-else-if="page==4">
      <h1>Seleccione Instancia</h1>
      <div>
        <v-data-table
          v-model="participantesFactura"
          :headers="headers2"
          :items="participantes"
          item-key="rut"
          show-select
          @click:row="handleClick"
          class="elevation-1"
        >
        
        </v-data-table>
        <v-btn  color="blue lighten-1" class="mr-4" @click="volver">Volver</v-btn>
        <v-btn  color="blue lighten-1" class="mr-4" @click="generarFactura">Generar factura</v-btn>
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
    page:1,
    curso:[],
    sence:'',
    otic:'',
    observacion:'',
    mostrarMalla:['Si','No'],
    instancias:[],
    instancia:[],
    enviar:[],
    razon_social:'',
    participantes:[],
    participantesFacturas:[],
    headers: [
      {
        text: 'Id',
        align: 'start',
        filterable: true,
        value: 'id_instancia',
      },
      { text: 'Sence', value: 'sence' },
      { text: 'Dirección', value: 'direccion'},
      { text: 'Malla', value: 'malla' },
      { text: 'Fecha inicio', value: 'fecha_inicio'},
      { text: 'Fecha termino', value: 'fecha_termino'},
  
    ],
    headers2: [
      {
        text: 'Rut',
        align: 'start',
        filterable: true,
        value: 'rut',
      },
      { text: 'Nombre', value: 'nombre' },
      { text: 'Apellido Paterno', value: 'apellido_paterno'},
      { text: 'Apellido Materno', value: 'apellido_materno' },
      { text: 'Fecha nacimiento', value: 'fecha_nacimiento'},
      { text: 'Tipo inscripcion', value: 'tipo_inscripcion'},
  
    ],
  }),
  methods:{
    obtenerCurso: async function(value){
      let response= axios.get('http://localhost:5000/curso/obtener?sence='+value)
      return response
    },
    volver: function(){
      this.page=this.page-1
    },
    avanzarPage2:function(){
      this.page=2
    },
    asignar: function(){
      if(this.instancia.length==0){
        alert("Debe seleccionar una instancia.")
      }
      else{
        this.page=3
      }
    },
    continuarPage4: async function(){
      let response= await axios.get('http://localhost:5000/participante/obtener?razon_social='+this.razon_social)
      this.participantes=response.data
      if(this.participantes.length==0){
        alert("No existen participantes en esta instancia que tengan esta razon social.")
        this.razon_social=''
      }
      else{
        this.page=4
      }
    },
    handleClick: function(value){
      console.log(value)
    },

    obtenerInstancias: async function(value){
      let response= axios.get('http://localhost:5000/instancia/obtener?sence='+value)
      return response
    },
    buscar: async function(value){
      console.log(value)
      try{
        let response= await this.obtenerCurso(value)
        if(response.data.length !=1){
          alert('No existe curso.')
        }
        else{
          this.curso=response.data
          let response2= await this.obtenerInstancias(value)
          this.instancias=response2.data
          console.log(this.instancias)
          this.page=2
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