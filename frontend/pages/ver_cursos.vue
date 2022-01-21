<template>
    <v-container class="test" >
        <v-card>

            <v-data-table
              :headers="headers"
              :items="cursos"
              :search="search"
              dense
            >
              <template v-slot:top>
              <v-toolbar
                flat
                class="test"

              >
        <v-toolbar-title> VER CURSOS</v-toolbar-title>

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
              
              <v-btn to="/crear_curso"
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Añadir Manual
                
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn to="/subir_archivo_curso"
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
                      v-model="editedItem.sence"
                      label="sence"
                      readonly
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
                    <v-autocomplete
                      v-model="editedItem.modalidad"
                      :items="modalidades"
                      label="modalidad"
                      persistent-hint
                      return-object
                      single-line 
                    ></v-autocomplete>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-autocomplete
                      v-model="editedItem.categoria"
                      label="categoria"
                      :items="categorias"
                     persistent-hint
                      return-object
                      single-line 
                    ></v-autocomplete>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.horas_curso"
                      label="horas_curso"
                    ></v-text-field>
                  </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4"
                  >
                <v-text-field
                    v-model="editedItem.valor_efectivo_participante"
                    :counter="20"
                    label="Valor efec. participante"
                ></v-text-field>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4"
                  >
                <v-text-field
                    v-model="editedItem.valor_imputable_participante"
                    :counter="20"
                    label="Valor imput. participante"
                ></v-text-field>
                </v-col>

              </v-row>
              <v-row>
                <v-col cols="12"
                    sm="6"
                    md="4"
                  >
                <v-text-field
                    v-model="editedItem.f_vigencia"
                    label="f_vigencia (YYYY-MM-DD)"
                ></v-text-field>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4"
                  >
                <v-text-field
                    v-model="editedItem.resolucion_sence"
                    label="resolucion_sence"
                ></v-text-field>
                </v-col>

                <v-col cols="12"
                    sm="6"
                    md="4"
                  >
                <v-text-field
                    v-model="editedItem.resolucion_usach"
                    label="resolucion_usach"
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
                @click="editarCurso"
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
              <v-btn color="blue darken-1" text @click="eliminarCurso">OK</v-btn>
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
    modalidades: [ "presencial","e-learning","a distancia"],
    categorias: [ "sincrono","asincrono","presencial"],
    razones: ["ninguna"],
    search: '',
    headers: [
      { text: 'Editar/Borrar', value: 'actions', sortable: false },
      {
        text: 'sence',
        align: 'start',
        filterable: true,
        value: 'sence',
      },
      { text: 'nombre', value: 'nombre' },
      { text: 'modalidad', value: 'modalidad'},
      { text: 'categoria', value: 'categoria' },
      { text: 'horas curso', value: 'horas_curso'},
      { text: 'valor efec', value: 'valor_efectivo_participante'},
      { text: 'valor imput', value: 'valor_imputable_participante'},
      { text: 'f_vigencia', value: 'f_vigencia'},
      { text: 'res_sence', value: 'resolucion_sence'},
       { text: 'res_usach', value: 'resolucion_usach'},

      
  
    ],

    cursos:[
    ],
    razones:[],

    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {
      sence: '',
      nombre: '',
      modalidad: '',
      categoria: '',
      horas_curso: '',
      valor_efectivo_participante: '',
      valor_imputable_participante: '',
      f_vigencia: '',     
      resolucion_sence: '',
      resolucion_usach: '',
    },
    defaultItem: {
      sence: '',
      nombre: '',
      modalidad: '',
      categoria: '',
      horas_curso: '',
      valor_efectivo_participante: '',
      valor_imputable_participante: '',
      f_vigencia: '',     
      resolucion_sence: '',
      resolucion_usach: '',
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nuevo curso' : 'Editar curso'
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
    getCursos: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/curso/obtener?');
        this.cursos = response.data;

        
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
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
    editarCurso: async function(){
      let newCurso ={
        sence: this.editedItem.sence,
        nombre: this.transformarVacio(this.editedItem.nombre),
        modalidad: this.transformarVacio(this.editedItem.modalidad),
        categoria: this.transformarVacio(this.editedItem.categoria),
        horas_curso: this.transformarVacio(this.editedItem.horas_curso),
        valor_efectivo_participante: this.transformarVacio(this.editedItem.valor_efectivo_participante),
        valor_imputable_participante: this.transformarVacio(this.editedItem.valor_imputable_participante),
        f_vigencia: this.transformarVacio(this.editedItem.f_vigencia),
        resolucion_sence: this.transformarVacio(this.editedItem.resolucion_sence),
        resolucion_usach: this.transformarVacio(this.editedItem.resolucion_usach),
      }
      try {
        //FALTA LA QUERY!!!!!
        let response = await axios.put('http://localhost:5000/curso/editar?sence='+newCurso.sence,newCurso);
        console.log(response);
        this.close();

        console.log(this.editedItem.resolucion_sence,this.editedItem.resolucion_sence)
        this.editedItem.resolucion_sence=this.editedItem.resolucion_sence
        Object.assign(this.cursos[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
    eliminarCurso: async function(){
      try {
        let response = await axios.delete('http://localhost:5000/curso/eliminar?sence='+this.editedItem.sence);
        console.log(response);
        this.closeDelete();
        Object.assign(this.cursos[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
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
          this.editedIndex = this.cursos.indexOf(item)
          this.editedItem = Object.assign({}, item)
          console.log(this.editedItem.resolucion_sence)
          this.dialog = true
        }
        else{
          alert("No cuenta con permisos para editar.")
        }
      },
    deleteItem: async function(item) {
      if(await this.permisos()){
        this.editedIndex = this.cursos.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("No cuenta con permisos para borrar.")
      }
    },
    deleteItemConfirm () {
      this.cursos.splice(this.editedIndex, 1)
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
    saveBUP () {
      if (this.editedIndex > -1) {
        Object.assign(this.cursos[this.editedIndex], this.editedItem)
      } else {
        this.cursos.push(this.editedItem)
      }
      this.close()
    },
    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.cursos[this.editedIndex], this.editedItem)
      } else {
        editarcurso()
      }
      this.close()
    },
  },
  created:async function(){
    if(await this.permisosPagina()){
      this.getCursos()
    }
    else{
      window.location.href='/'
    }
    //this.mostrarresolucion_sence(valor)
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