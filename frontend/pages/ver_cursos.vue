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
                      v-model="editedItem.modalidad"
                      label="apellido paterno"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.categoria"
                      label="apellido materno"
                    ></v-text-field>
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
                      v-model="editedItem.valor_efectivo_participante"
                      label="valor_efectivo_participante"
                    ></v-text-field>
                  </v-col>
                   <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                  
                    <v-text-field
                      v-model="editedItem.resolucion_sence"
                      label="resolucion_sence"
                    >
                    ></v-text-field>

                  </v-col>
                  
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  ><v-autocomplete
                      v-model="editedItem.valor_imputable_participante"
                      :items="razones"
                      dense
                      item-text="valor_imputable_participante"
                      label="valor_imputable_participante"
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
                @click="editarcurso"
              >
                Guardar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">Quieres archivar esto?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancelar</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
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
export default {

  data:()=>( {
    busqueda: null,
    search: '',
    headers: [
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
      { text: 'res_sence', value: 'resolucion_sence'},

      { text: 'Editar/Borrar', value: 'actions', sortable: false },
  
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
      resolucion_sence: '',
      nivel_educacional: '',
      fecha_nacimiento: '',
      nacionalidad: '',
      tipo_inscripcion: '',
      ocupacion: '',
      horas_curso: '',
      correo_personal: '',
      fono_personal: '',
      valor_efectivo_participante: '',
      valor_imputable_participante: ''
    },
    defaultItem: {
      sence: '',
      nombre: '',
      modalidad: '',
      categoria: '',
      resolucion_sence: '',
      nivel_educacional: '',
      fecha_nacimiento: '',
      nacionalidad: '',
      tipo_inscripcion: '',
      ocupacion: '',
      horas_curso: '',
      correo_personal: '',
      fono_personal: '',
      valor_efectivo_participante: '',
      valor_imputable_participante: ''
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
    forEach: async function(){

    },
    getcursos: async function(){
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
    editarcurso: async function(){
      let newcurso ={
        sence: this.editedItem.sence,
        nombre: this.transformarVacio(this.editedItem.nombre),
        modalidad: this.transformarVacio(this.editedItem.modalidad),
        categoria: this.transformarVacio(this.editedItem.categoria),
        resolucion_sence: this.transformarVacio(this.resolucion_sence),
        nivel_educacional: this.transformarVacio(this.editedItem.nivel_educacional),
        fecha_nacimiento: this.transformarVacio(this.editedItem.fecha_nacimiento),
        nacionalidad: this.transformarVacio(this.editedItem.nacionalidad),
        tipo_inscripcion: this.transformarVacio(this.editedItem.tipo_inscripcion),
        ocupacion: this.transformarVacio(this.editedItem.ocupacion),
        horas_curso: this.transformarVacio(this.editedItem.horas_curso),
        correo_personal: this.transformarVacio(this.editedItem.correo_personal),
        fono_personal: this.transformarVacio(this.editedItem.fono_personal),
        valor_efectivo_participante: this.transformarVacio(this.editedItem.valor_efectivo_participante),
        valor_imputable_participante: this.transformarVacio(this.editedItem.valor_imputable_participante)
      }
      try {
        let response = await axios.put('http://localhost:5000/curso/editar?sence='+newcurso.sence,newcurso);
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
    async getRazones(){
      try {
        let response = await axios.get('http://localhost:5000/empresa/obtener/valor_imputable_participante');
        this.razones = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    
    editItem (item) {
        this.editedIndex = this.cursos.indexOf(item)
        this.editedItem = Object.assign({}, item)
        console.log(this.editedItem.resolucion_sence)
        this.dialog = true
      },
    deleteItem (item) {
      this.editedIndex = this.cursos.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
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
  created(){
    this.getcursos()
    this.getRazones()
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