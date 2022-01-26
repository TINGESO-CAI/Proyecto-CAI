<template>
    <v-container class="test" >
        <v-card>
            <v-data-table
              :headers="headers"
              :items="relatores"
              :search="search"
              dense
            >
              <template v-slot:[`item.genero`]="{ item }">
                <span>{{ mostrarGenero(item.genero) }}</span>
              </template>
              <template v-slot:top>
              <v-toolbar
                flat
              >
        <v-toolbar-title> VER RELATORES</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Busqueda"
                single-line
                hide-details
          ></v-text-field>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="dialog"
            max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              
              <v-btn to="/nuevo_relator"
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Añadir Manual
                
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn to="/subir_archivo_relator"
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Subir planilla
              </v-btn>
            </template>
          <v-card max-width="1000px">
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
                </v-row>

                <v-row>

                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-select
                  v-model="editedItem.banco"
                  :items="bancos"
                  item-text="banco"
                  label="banco"
                  persistent-hint
                  return-object
                  single-line
                ></v-select>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-autocomplete
                  v-model="editedItem.tipo_cuenta"
                  :items="tipos"
                  item-text="tipo_cuenta"
                  label="tipo_cuenta"
                  persistent-hint
                  return-object
                  single-line   
                ></v-autocomplete>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-text-field
                  v-model="editedItem.numero_cuenta"
                  item-text="numero_cuenta"
                  label="numero_cuenta"

                ></v-text-field>
                </v-col>

                </v-row>

                 <v-row>
                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-text-field
                  v-model="editedItem.cv"
                  item-text="CV"
                  label="CV"

                ></v-text-field>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-text-field
                  v-model="editedItem.titulo"
                  item-text="titulo"
                  label="titulo"

                ></v-text-field>
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
                @click="editarRelator"
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
              <v-btn color="blue darken-1" text @click="eliminarRelator">OK</v-btn>
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
    search: '',
    generos:['femenino','masculino'],
    paises: [ "Chile","Desconocido","Afganistán","Albania","Alemania","Andorra","Angola","Antigua y Barbuda","Arabia Saudita","Argelia","Argentina","Armenia","Australia","Austria","Azerbaiyán","Bahamas","Bangladés","Barbados","Baréin","Bélgica","Belice","Benín","Bielorrusia","Birmania","Bolivia","Bosnia y Herzegovina","Botsuana","Brasil","Brunéi","Bulgaria","Burkina Faso","Burundi","Bután","Cabo Verde","Camboya","Camerún","Canadá","Catar","Chad","China","Chipre","Ciudad del Vaticano","Colombia","Comoras","Corea del Norte","Corea del Sur","Costa de Marfil","Costa Rica","Croacia","Cuba","Dinamarca","Dominica","Ecuador","Egipto","El Salvador","Emiratos Árabes Unidos","Eritrea","Eslovaquia","Eslovenia","España","Estados Unidos","Estonia","Etiopía","Filipinas","Finlandia","Fiyi","Francia","Gabón","Gambia","Georgia","Ghana","Granada","Grecia","Guatemala","Guyana","Guinea","Guinea ecuatorial","Guinea-Bisáu","Haití","Honduras","Hungría","India","Indonesia","Irak","Irán","Irlanda","Islandia","Islas Marshall","Islas Salomón","Israel","Italia","Jamaica","Japón","Jordania","Kazajistán","Kenia","Kirguistán","Kiribati","Kuwait","Laos","Lesoto","Letonia","Líbano","Liberia","Libia","Liechtenstein","Lituania","Luxemburgo","Madagascar","Malasia","Malaui","Maldivas","Malí","Malta","Marruecos","Mauricio","Mauritania","México","Micronesia","Moldavia","Mónaco","Mongolia","Montenegro","Mozambique","Namibia","Nauru","Nepal","Nicaragua","Níger","Nigeria","Noruega","Nueva Zelanda","Omán","Países Bajos","Pakistán","Palaos","Palestina","Panamá","Papúa Nueva Guinea","Paraguay","Perú","Polonia","Portugal","Reino Unido","República Centroafricana","República Checa","República de Macedonia","República del Congo","República Democrática del Congo","República Dominicana","República Sudafricana","Ruanda","Rumanía","Rusia","Samoa","San Cristóbal y Nieves","San Marino","San Vicente y las Granadinas","Santa Lucía","Santo Tomé y Príncipe","Senegal","Serbia","Seychelles","Sierra Leona","Singapur","Siria","Somalia","Sri Lanka","Suazilandia","Sudán","Sudán del Sur","Suecia","Suiza","Surinam","Tailandia","Tanzania","Tayikistán","Timor Oriental","Togo","Tonga","Trinidad y Tobago","Túnez","Turkmenistán","Turquía","Tuvalu","Ucrania","Uganda","Uruguay","Uzbekistán","Vanuatu","Venezuela","Vietnam","Yemen","Yibuti","Zambia","Zimbabue"],
    bancos: ["BANCOESTADO","BANCO DE CHILE/EDWARDS","BANCO INTERNACIONAL","SCOTIABANK CHILE/Desarrollo",
      "BCI","BANCO BICE","HSBC BANK","BANCO SANTANDER/Banefe",
      "ITAÚ CORPBANCA","BANCO SECURITY","BANCO FALABELLA","BANCO RIPLEY","BANCO CONSORCIO",
      "SCOTIABANK AZUL","BANCO BTG"
    ],
    tipos: ["corriente","vista","chequera electrónica","ahorro"],
    headers: [
      { text: 'Editar/Borrar', value: 'actions', sortable: false },
      {
        text: 'Rut',
        align: 'start',
        filterable: true,
        value: 'rut',
      },
      { text: 'Nombre', value: 'nombre' },
      { text: 'Apellido_paterno', value: 'apellido_paterno'},
      { text: 'Apellido_materno', value: 'apellido_materno' },
      { text: 'Titulo', value: 'titulo'},
      { text: 'Numero cuenta', value: 'numero_cuenta'},
      { text: 'Banco', value: 'banco'},
      { text: 'Tipo cuenta', value: 'tipo_cuenta'},
      { text: 'numero_cuenta', value: 'numero_cuenta'},
      { text: 'correo corporativo', value: 'correo_corporativo'},
      { text: 'fono corporativo', value: 'fono_corporativo'},
      { text: 'correo_personal', value: 'correo_personal'},
      { text: 'fono_personal', value: 'fono_personal'},
      { text: 'fecha_nacimiento', value: 'fecha_nacimiento'},
      { text: 'genero', value: 'genero'},
      { text: 'CV', value: 'cv'},
    ],
    relatores:[],
    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {
      rut: '',
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      titulo: '',
      cv: '',
      fecha_nacimiento: '',
      numero_cuenta: '',
      banco: '',
      tipo_cuenta: '',
      genero:'',
      correo_corporativo: '',
      correo_personal: '',
      fono_personal: '',
      fono_corporativo: '',
    },
    defaultItem: {
      rut: '',
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      titulo: '',
      cv: '',
      fecha_nacimiento: '',
      numero_cuenta: '',
      banco: '',
      tipo_cuenta: '',
      genero:'',
      correo_corporativo: '',
      correo_personal: '',
      fono_personal: '',
      fono_corporativo: '',
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nueva relator' : 'Editar relator'
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
    getRelatores: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://52.188.153.77:5000/relator/obtener?');
        this.relatores = response.data;

        
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
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
    editarRelator: async function(){
      let newRelator ={
        rut: this.editedItem.rut,
        nombre: this.transformarVacio(this.editedItem.nombre),
        apellido_paterno: this.transformarVacio(this.editedItem.apellido_paterno),
        apellido_materno: this.transformarVacio(this.editedItem.apellido_materno),
        titulo: this.transformarVacio(this.editedItem.titulo),
        cv: this.transformarVacio(this.editedItem.cv),
        genero: this.transformarVacio(this.cambiarGenero(this.editedItem.genero)),
        fecha_nacimiento: this.transformarVacio(this.editedItem.fecha_nacimiento),
        numero_cuenta: this.transformarVacio(this.editedItem.numero_cuenta),
        banco: this.transformarVacio(this.editedItem.banco),
        tipo_cuenta: this.transformarVacio(this.editedItem.tipo_cuenta),
        correo_corporativo: this.transformarVacio(this.editedItem.correo_corporativo),
        correo_personal: this.transformarVacio(this.editedItem.correo_personal),
        fono_personal: this.transformarVacio(this.editedItem.fono_personal),
        fono_corporativo: this.transformarVacio(this.editedItem.fono_corporativo),
      }
      try {
        let response = await axios.put('http://52.188.153.77:5000/relator/editar?rut='+newRelator.rut,newRelator);
        console.log(response);
        this.close();

        console.log(this.cambiarGenero(this.editedItem.genero),this.editedItem.genero)
        this.editedItem.genero=this.cambiarGenero(this.editedItem.genero)
        Object.assign(this.relatores[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
    eliminarRelator: async function(){
      try {
        let response = await axios.delete('http://52.188.153.77:5000/relator/eliminar?rut='+this.editedItem.rut);
        console.log(response);
        this.closeDelete();
        Object.assign(this.relatores[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
    cambiarGenero(valor){
      console.log(valor)
      if (valor ==  'femenino') return '1'
      else if (valor == 'masculino' ) return '2'
      else return null
    },
    mostrarGenero(valor){
      if (valor == '1' ) return 'femenino'
      else if (valor == '2' ) return 'masculino'
      else return 'desconocido'
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
    permisosPagina:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://52.188.153.77:5000/cuenta/permisos?token='+data.token);
          return (response.data.nivel_acceso <4)
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
        this.editedIndex = this.relatores.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.editedItem.genero=this.mostrarGenero(this.editedItem.genero)
        this.dialog = true
      }
      else{
        alert("No cuenta con permisos para editar.")
      }
    },
    deleteItem: async function (item) {
      if(await this.permisos()){
        this.editedIndex = this.relatores.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("No cuenta con permisos para borrar.")
      }
    },
    deleteItemConfirm () {
      this.relators.splice(this.editedIndex, 1)
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
    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.relatores[this.editedIndex], this.editedItem)
      } else {
        this.relatores.push(this.editedItem)
      }
      this.close()
    },

  },
  created: async function(){
    if(await this.permisosPagina()){
      this.getRelatores()
      this.getRazones()
      //this.mostrarGenero(valor)
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