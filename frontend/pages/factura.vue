<template>
    <v-container class="test">
      <div v-if="page==1">
        <h1 class="text-center">Ingrese sence del curso</h1>
        <v-autocomplete
                      v-model="sence"
                      :items="sences"
                      dense
                      filled 
                      rounded
                      class="center"
                      item-text="sence"
                      label="sence"
                      persistent-hint
                      single-line
                      append-icon="mdi-magnify"
                      @click:append="buscar(sence)"
                ></v-autocomplete>
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
                    v-if="enviar==2"
                    v-model="especificar"
                    label="Especificar"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="otic"
                    label="Numero Otic"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="num_hes"
                    label="Numero hes"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="num_orden"
                    label="Numero orden"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-autocomplete
                      v-model="razon_social"
                      :items="razonesV"
                      dense
                      item-text="razon_social"
                      label="razon_social"
                      persistent-hint
                      return-object
                      single-line
                ></v-autocomplete>
                </v-col>
                 <!--
                <v-col>
                <h2 class="text-center"> Datos de la empresa</h2>
                    <v-col>
                    <p class="font-weight-bold">Sence:</p>
                    </v-col>                
                    <v-col>{{empresa.sence}}</v-col>
                    <v-col>
                    <p class="font-weight-bold">Nombre:</p>
                    </v-col>                
                    <v-col>{{empresa.nombre}}</v-col>
                </v-col>
                -->
                <v-col>
                <v-text-field
                    v-model="observacion"
                    label="observación"
                    required
                ></v-text-field>
                </v-col> 
                <v-row>
                <v-col>
                <v-btn  color="blue lighten-1" class="mr-4" @click="volver">Volver</v-btn>
                </v-col>
                <v-col>
                <v-btn  color="blue lighten-1" class="mr-4" @click="continuarPage4">Continuar</v-btn>
                </v-col>
                </v-row>         
            </v-form>
        </v-container>
        </v-col>
        </v-row>
      </v-container>
        <v-divider></v-divider>
    </div>
    <div v-else-if="page==4">
      <h1>Seleccione Participantes</h1>
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
//import func from 'vue-editor-bridge';
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
    num_hes:'',
    razon_social:'',
    razones: [],
    razonesV: [],
    participantes:[],
    participantesFactura:[],
    sences:[],
    especificar:'',
    num_orden:'',
    factura:[],
    empresa:{
      razon_social: 'test',
      giro: '',
      atencion: '',
      departamento: '',
      rut: '',
      direccion: '',
      comuna: '',
      correo: '',
      fono: '',
    },
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
    onlyRut:function(){
      let participantes=[]
      for (let i=0; i<this.participantesFactura.length;i++){
        participantes.push({rut:this.participantesFactura[i].rut})
      }
      return (participantes)
    },
    generarFactura: async function(){
      if (this.participantesFactura.length==0){
        alert("Debe seleccionar almenos un participante.")
      }
      else{
        try{
          let response= await axios.post('http://localhost:5000/factura/agregar',
          {
            num_registro: '1'
            ,estado: 0
            ,num_hes: this.num_hes
            ,fecha_emision: '10/12/2021'
            ,fecha_vencimiento: '21/12/2021'
            ,sence: this.curso[0].sence
            ,id_instancia: this.instancia[0].id_instancia
            ,razon_social: this.razon_social.razon_social
            ,enviar_factura: parseInt(this.enviar)
            ,especificar: this.especificar
            ,num_orden:this.num_orden
            ,obs:this.observacion
            ,participantes:this.onlyRut()
          })
          window.location.href='http://localhost:5000/factura/descargar/'+response.data.id_factura.toString()
          this.page=1
          this.curso=[]
          this.sence=''
          this.otic=''
          this.observacion=''
          this.mostrarMalla=['Si','No']
          this.instancias=[]
          this.instancia=[]
          this.enviar=[]
          this.num_hes=''
          this.razon_social=''
          this.razones= []
          this.razonesV= []
          this.participantes=[]
          this.participantesFactura=[]
          this.sences=[]
          this.especificar=''
          this.num_orden=''
          this.factura=[]
          
        }
        catch(error){
          console.log(error)
          alert("ocurrio un error")
        }
      }
    },
    continuarPage4: async function(){
      let response= await axios.get('http://localhost:5000/participante_instancia/obtener?razon_social='+this.razon_social.razon_social+'&id_instancia='+this.instancia[0].id_instancia)
      this.participantes=response.data
      console.log(this.razon_social.razon_social)
      if(this.participantes.length==0){
        alert("No existen participantes en esta instancia que tengan esta razon social.")
        this.razon_social=''
      }
      else{
        this.page=4
      }
    },
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
    async getRazonesValidas(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/instancia/obtener_razones_sociales/'+this.instancia[0].id_instancia);
        this.razonesV = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    async getSences(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/curso/obtener/sences_con_instancia');
        this.sences = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    getEmpresa: async function(value){
      let response= axios.get('http://localhost:5000/curso/obtener?sence='+value)
      this.empresa=response.data;
      console.log(response);
    },
    handleClick: function(value){
      console.log(value)
    },
    obtenerCurso: async function(value){
      let response= axios.get('http://localhost:5000/curso/obtener?sence='+value)
      return response
    },

    obtenerInstancias: async function(value){
      let response= axios.get('http://localhost:5000/instancia/obtener?sence='+value)
      return response
    },
    obtenerDatos: async function(value){
      let response= axios.get('http://localhost:5000/empresa/obtener?razon_social='+value)
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
  created(){
    this.getRazones();
    this.getEmpresa();
    this.getSences();
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