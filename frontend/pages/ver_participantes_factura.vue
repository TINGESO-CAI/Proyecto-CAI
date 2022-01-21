<template>
    <v-container class="test" >
      <div v-if="participantes.length==0">
        <h1 class="text-center">Ingrese Id de la solicitud de S. factura</h1>
        <v-autocomplete
                      v-model="factura"
                      :items="facturas"
                      dense
                      filled 
                      rounded
                      item-text="id_factura"
                      label="factura"
                      persistent-hint
                      single-line
                      append-icon="mdi-magnify"
                      @click:append="buscar(factura)"
          ></v-autocomplete>
      </div>
      <div v-if="participantes.length != 0">
        <v-card>
            <v-data-table
              :headers="headers"
              :items="participantes"
              dense
            >
              <template v-slot:[`item.genero`]="{ item }">
                <span>{{ mostrarGenero(item.genero) }}</span>
              </template>
              <template v-slot:top>
                
              <v-toolbar
                flat
              >

        
        <v-toolbar-title> VER PARTICIPANTES</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >

            <template v-slot:activator="{ on, attrs }">
              <v-btn to="/nuevo_participante"
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                + Participante
              </v-btn>
            </template>
          <v-card>
            <v-card-title>
              <span class="text-h5">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <!--replicar desde aqui-->
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.rut"
                      label="rut"
                    ></v-text-field>
                  </v-col>
                <!--hasta aqui-->
                <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.nombre"
                      label="nombre"
                    ></v-text-field>
                  </v-col>
                <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.apellido_paterno"
                      label="apellido paterno"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.apellido_materno"
                      label="apellido materno"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.correo_corporativo"
                      label="correo_corporativo"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.correo_personal"
                      label="correo_personal"
                    ></v-text-field>
                  </v-col>    
                </v-row>
                <v-row>
                  
          
                  
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.fono_personal"
                      label="fono_personal"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.fono_corporativo"
                      label="fono_corporativo"
                    ></v-text-field>
                  </v-col>
                   <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                  
                    <v-select
                      v-model="editedItem.genero"
                      :items="generos"
                      dense
                      item-text="genero"
                      label="genero"
                      persistent-hint
                      return-object
                      single-line   
                      
                    >
                    </v-select>

                  </v-col>
                  
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  ><v-autocomplete
                      v-model="editedItem.razon_social"
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
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="blue darken-1"
                text
                @click="close"
              >
                Cancelar
              </v-btn>
              <v-btn
                color="blue darken-1"
                text
                @click="save"
              >
                Guardar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">¿Quieres eliminar esto?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancelar</v-btn>
              <v-btn color="blue darken-1" text @click="eliminarParticipante">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
            </v-data-table>
          </v-card>

          <v-btn  color="blue lighten-1" class="mr-4" @click="volver">Volver</v-btn>

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
    busqueda: null,
    generos:['-','femenino','masculino'],
    headers: [
      {
        text: 'Rut',
        align: 'start',
        filterable: true,
        value: 'rut',
      },
      { text: 'nombre', value: 'nombre' },
      { text: 'apellido_paterno', value: 'apellido_paterno'},
      { text: 'apellido_materno', value: 'apellido_materno' },
      { text: 'correo corporativo', value: 'correo_corporativo'},
      { text: 'fono corporativo', value: 'fono_corporativo'},
      { text: 'razon_social', value: 'razon_social'},
      { text: 'genero', value: 'genero'},

      { text: 'Editar/Borrar', value: 'actions', sortable: false },
  
    ],

    participantes:[ ],

    rut: null,
    nombre: null,
    apellido_paterno: null,
    apellido_materno: null,
    genero: null,
    nivel_educacional: null,
    fecha_nacimiento: null,
    nacionalidad: null,
    tipo_inscripcion: null,
    ocupacion: null,
    correo: null,
    fono: null,
    razon_social: null,
    facturas:[],
    factura:'',
    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {
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
      correo: '',
      fono: '',
      razon_social: '',
    },
    defaultItem: {
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
      correo_personal:'',
      fono_corporativo: '',
      fono_personal:'',
      razon_social: '',
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nueva participante' : 'Editar participante'
    },
  },
  watch: {
    dialog (val) {
      val || this.close()
    },
    dialogDelete (val) {
      val || this.closeDelete()
    },
  },
  methods:{
    obtenerParticipantes: async function(factura){
      console.log(factura)
      try{
        let response= await axios.get
      }
      catch(error){
        alert("Ocurrio un error.")
        console.log(error)
      }
    },
    volver: function(){
      this.participantes=[]
      this.factura=''
    },
    buscar: async function(factura){
      console.log(factura)
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/participante_factura/obtener/'+factura.toString());
        this.participantes = response.data;
        console.log(this.facturas)

        
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    getFacturas: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/factura/obtener/id');
        this.facturas = response.data;
        console.log(this.facturas)

        
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
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
    mostrarGenero(valor){
      if (valor == '1' ) return 'femenino'
      else if (valor == '2' ) return 'masculino'
      else return null
    },
    permisos:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://localhost:5000/cuenta/permisos?token='+data.token);
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
    permisosPagina:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://localhost:5000/cuenta/permisos?token='+data.token);
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
    editItem: async function (item) {
      if(await this.permisos()){
        this.editedIndex = this.participantes.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      }
      else{
        alert("No cuenta con permisos para editar.")
      }
    },
    deleteItem:async function (item) {
      if(await this.permisos()){
        this.editedIndex = this.participantes.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("no cuenta con permisos para borrar.")
      }
    },
    deleteItemConfirm () {
      this.participantes.splice(this.editedIndex, 1)
      this.closeDelete()
    },
    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    cambiarGenero(valor){
      console.log(valor)
      if (valor ==  'femenino') return '1'
      else if (valor == 'masculino' ) return '2'
      else return null
    },

    transformarVacio: function(valor){
      if(valor==''){
        return null
      }
      else{
        return valor
      }
    },
    save: async function() {
      let newParticipante ={
        rut: this.editedItem.rut,
        nombre: this.transformarVacio(this.editedItem.nombre),
        apellido_paterno: this.transformarVacio(this.editedItem.apellido_paterno),
        apellido_materno: this.transformarVacio(this.editedItem.apellido_materno),
        genero: this.transformarVacio(this.cambiarGenero(this.editedItem.genero)),
        nivel_educacional: this.transformarVacio(this.editedItem.nivel_educacional),
        fecha_nacimiento: this.transformarVacio(this.editedItem.fecha_nacimiento),
        nacionalidad: this.transformarVacio(this.editedItem.nacionalidad),
        tipo_inscripcion: this.transformarVacio(this.editedItem.tipo_inscripcion),
        ocupacion: this.transformarVacio(this.editedItem.ocupacion),
        correo_corporativo: this.transformarVacio(this.editedItem.correo_corporativo),
        correo_personal: this.transformarVacio(this.editedItem.correo_personal),
        fono_personal: this.transformarVacio(this.editedItem.fono_personal),
        fono_corporativo: this.transformarVacio(this.editedItem.fono_corporativo),
        razon_social: this.transformarVacio(this.editedItem.razon_social)
      }
      try {
        let response = await axios.put('http://localhost:5000/participante/editar?rut='+newParticipante.rut,newParticipante);
        console.log(response);
        this.close();

        console.log(this.cambiarGenero(this.editedItem.genero),this.editedItem.genero)
        this.editedItem.genero=this.cambiarGenero(this.editedItem.genero)
        Object.assign(this.participantes[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
    eliminarParticipante: async function(){
      try {
        let response = await axios.delete('http://localhost:5000/participante/eliminar?rut='+this.editedItem.rut);
        console.log(response);
        this.closeDelete();
        Object.assign(this.participantes[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
  },
  created: async function(){
    if(await this.permisosPagina()){
      this.getFacturas()
      this.getRazones()
    }
    else{
      window.location.href='/'
    }
  }
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