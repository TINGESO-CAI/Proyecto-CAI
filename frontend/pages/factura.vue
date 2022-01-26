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
                    v-model="numeroRegistro"
                    label="Numero registro"
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
                <v-text-field
                    v-model=fecha_vencimiento
                    label="fecha_vencimiento"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="observacion"
                    label="observación"
                    required
                ></v-text-field>
                </v-col>
                <input type="checkbox" id="checkbox" v-model="particular" @change="cambiarParticular()">
                  <label for="checkbox"> particular </label>
                 <v-col>
                <v-text-field
                    v-if="particular"
                    v-model="direccion_particular"
                    label="Dirección"
                    required
                ></v-text-field>
                </v-col>
                 <v-col>
                <v-text-field
                    v-if="particular"
                    v-model="comuna_particular"
                    label="Comuna"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-autocomplete
                      v-if="particular==false"
                      v-model="razon_social"
                      :items="razonesV"
                      @change="obtenerContacto"
                      dense
                      item-text="razon_social"
                      label="razon_social"
                      persistent-hint
                      return-object
                      single-line
                ></v-autocomplete>
                </v-col>
                <v-col>
                <v-autocomplete
                      v-if="hide==false"
                      v-model="contacto"
                      :items="contactos"
                      dense
                      item-text="fono"
                      label="fono"
                      persistent-hint
                      return-object
                      single-line
                      @change="obtenerDescripcion"
                ></v-autocomplete>
                </v-col>
                <v-col>
                <v-text-field
                      v-if="hide==false"
                      v-model="descripcion"
                      readonly
                ></v-text-field>
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
    page:1,
    estado:'',
    hide:true,
    descripcion:'',
    numeroRegistro:'',
    fecha_vencimiento:'',
    contactos:[],
    contacto:{contacto:''},
    direccion_particular:'',
    comuna_particular:'',
    curso:[],
    sence:'',
    otic:'',
    observacion:'',
    mostrarMalla:['Si','No'],
    instancias:[],
    instancia:[],
    enviar:'',
    num_hes:'',
    razon_social:{razon_social:''},
    razones: [],
    razonesV: [],
    participantes:[],
    participantesFactura:[],
    sences:[],
    especificar:'',
    num_orden:'',
    particular:false,
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
    obtenerDescripcion: async function(){
      try{
        let response= await axios.get('http://'+process.env.IP_FRONT+':5000/contacto/obtener_descripcion?razon_social='+this.razon_social.razon_social+'&fono='+this.contacto.fono.replace('+','%2B'))
        console.log(response.data)
        this.descripcion=response.data[0].descripcion
      }
      catch(error){
        alert("ocurrio un error")
        console.log(error)
      }
    },
    volver: function(){
      this.page=this.page-1
    },
    avanzarPage2:function(){
        this.page=2
    },
    cambiarParticular(){
      if(this.particular){
        this.hide=true
      }
      else if(this.razon_social.razon_social!=''){
        this.hide=false
      }
    },
    asignar: function(){
      if(this.instancia.length==0){
        alert("Debe seleccionar una instancia.")
      }
      else{
        try{
          this.getRazonesValidas()
          this.page=3
        }
        catch(error){
          console.log("error")
        }
      }
    },
    onlyRut:function(){
      let participantes=[]
      for (let i=0; i<this.participantesFactura.length;i++){
        participantes.push({rut:this.participantesFactura[i].rut})
      }
      return (participantes)
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
    transformarVacio: function(valor){
      if(valor==''){
        return null
      }
      else{
        return valor
      }
    },
    comprobarFecha:function(fecha){
      if (fecha.split('-').length == 3 || fecha==''){
        return true
      }
      else{
        return false
      }
    },
    transformarEstado(){
      if (this.estado==''){
        return null
      }
      else{
        return parseInt(this.estado)
      }
    },
    obtenerContacto:async function(){
      try{
        this.hide=false
        let response= await axios.get('http://'+process.env.IP_FRONT+':5000/contacto/obtener/'+this.razon_social.razon_social)
        console.log(response.data)
        this.contactos=response.data
        this.contacto=this.contactos[0]
        console.log(this.contacto.fono[0])
        if(this.contacto != null){
          let response2= await axios.get('http://'+process.env.IP_FRONT+':5000/contacto/obtener_descripcion?razon_social='+this.razon_social.razon_social+'&fono='+this.contacto.fono.replace('+','%2B'))
          console.log("datos",response2.data)
          if(response2.data!=[]){
            this.descripcion=response2.data[0].descripcion
          }
        }
        else{
          this.contacto={contacto:''}
          this.descripcion=''
        }
        
      }
      catch(error){
        alert("ocurrio un error")
        console.log(error)
      }
      

    },
    generarFactura: async function(){
      if (this.participantesFactura.length==0){
        alert("Debe seleccionar almenos un participante.")
      }
      else{
        try{
          let response= await axios.post('http://'+process.env.IP_FRONT+':5000/factura/agregar',
          {
            num_registro: this.transformarVacio(this.numeroRegistro)
            ,num_hes: this.transformarVacio(this.num_hes)
            ,fecha_vencimiento: this.transformarVacio(this.fecha_vencimiento)
            ,sence: this.transformarVacio(this.curso[0].sence)
            ,id_instancia: this.transformarVacio(this.instancia[0].id_instancia)
            ,razon_social: this.transformarVacio(this.razon_social.razon_social)
            ,enviar_factura: parseInt(this.enviar)
            ,especificar: this.transformarVacio(this.especificar)
            ,num_orden:this.transformarVacio(this.num_orden)
            ,obs:this.transformarVacio(this.observacion)
            ,participantes:this.onlyRut()
            ,fono_empresa:this.transformarVacio(this.contacto.fono)
            ,direccion_particular:this.transformarVacio(this.direccion_particular)
            ,comuna_particular:this.transformarVacio(this.comuna_particular)
          })
          console.log(response)
          window.location.href='http://'+process.env.IP_FRONT+':5000/factura/descargar/'+response.data.id_factura.toString()
          this.page=1
          this.getSences()
          this.curso=[]
          this.sence=''
          this.otic=''
          this.observacion=''
          this.mostrarMalla=['Si','No']
          this.instancias=[]
          this.instancia=[]
          this.enviar=''
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
          console.log(this.razon_social)
        }
      }
    },
    continuarPage4: async function(){
      console.log("razon social:",this.razon_social)
      if(this.enviar!=''){
        if(this.comprobarFecha(this.fecha_vencimiento)==false){
          alert("Mal formato en fecha")
          return 0
        }
        if(this.particular==false){
          this.direccion_particular=''
          this.comuna_particular=''
          let response= await axios.get('http://'+process.env.IP_FRONT+':5000/participante_instancia/obtener?razon_social='+this.razon_social.razon_social+'&id_instancia='+this.instancia[0].id_instancia)
          this.participantes=response.data
          console.log(this.razon_social.razon_social)
          if(this.participantes.length==0){
            alert("No existen participantes en esta instancia que tengan esta razon social.")
            this.razon_social.razon_social=''
          }
          else{
            this.page=4
          }
        }
        else{
          this.razon_social.razon_social=''
          this.contacto.fono=''
          let response= await axios.get('http://'+process.env.IP_FRONT+':5000/participante/obtener/independientes')
          this.participantes=response.data          
          if(this.participantes.length==0){
            alert("No existen participantes independientes.")
            this.razon_social.razon_social=''
          }
          else{
            this.page=4
          }
        }

      }
      else{
        alert("Debe seleccionar a donde se quiere enviar.")
      }
    },
    async getRazones(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://'+process.env.IP_FRONT+':5000/empresa/obtener/razon_social');
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
        let response = await axios.get('http://'+process.env.IP_FRONT+':5000/instancia/obtener_razones_sociales/'+this.instancia[0].id_instancia);
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
        let response = await axios.get('http://'+process.env.IP_FRONT+':5000/curso/obtener/sences_con_instancia');
        this.sences = response.data;
        console.log(response);
        
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    getEmpresa: async function(value){
      let response= axios.get('http://'+process.env.IP_FRONT+':5000/curso/obtener?sence='+value)
      this.empresa=response.data;
      console.log(response);
    },
    handleClick: function(value){
      console.log(value)
    },
    obtenerCurso: async function(value){
      let response= axios.get('http://'+process.env.IP_FRONT+':5000/curso/obtener?sence='+value)
      return response
    },

    obtenerInstancias: async function(value){
      let response= axios.get('http://'+process.env.IP_FRONT+':5000/instancia/obtener?sence='+value)
      return response
    },
    obtenerDatos: async function(value){
      let response= axios.get('http://'+process.env.IP_FRONT+':5000/empresa/obtener?razon_social='+value)
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
    },
    permisos:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://'+process.env.IP_FRONT+':5000/cuenta/permisos?token='+data.token);
          return (response.data.nivel_acceso <2)
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
  created(){
    if(this.permisos()){
      this.getRazones();
      this.getEmpresa();
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