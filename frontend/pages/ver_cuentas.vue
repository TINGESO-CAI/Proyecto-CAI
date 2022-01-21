<template>
    <v-container class="test" >
        <v-card>

            <v-data-table
              :headers="headers"
              :items="usuarios"
              :search="search"
              dense

            >
              <template v-slot:[`item.administrador`]="{item }">
                    <v-icon
                      v-if="item.nivel_acceso == 0"
                      class="mr-2"
                      color="green darken-2"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.nivel_acceso != 0"
                      center
                      class="mr-2"
                      color="red darken-2"
                      @click="confirmacion(item,0)"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>
              <template v-slot:[`item.jefeAdmin`]="{item }">
                    <v-icon
                      v-if="item.nivel_acceso == 1"
                      class="mr-2"
                      color="green darken-2"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.nivel_acceso != 1"
                      center
                      class="mr-2"
                      color="red darken-2"
                      @click="confirmacion(item,1)"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>
              <template v-slot:[`item.trabajador`]="{item }">
                    <v-icon
                      v-if="item.nivel_acceso == 2"
                      class="mr-2"
                      color="green darken-2"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.nivel_acceso != 2"
                      center
                      class="mr-2"
                      color="red darken-2"
                      @click="confirmacion(item,2)"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>
               <template v-slot:[`item.ejecutivo`]="{item }">
                    <v-icon
                      v-if="item.nivel_acceso == 3"
                      class="mr-2"
                      color="green darken-2"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.nivel_acceso != 3"
                      center
                      class="mr-2"
                      color="red darken-2"
                      @click="confirmacion(item,3)"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>
              <template v-slot:top>
              <v-toolbar
                flat
                class="test"

              >
        <v-toolbar-title> VER USUARIOS</v-toolbar-title>

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
              
              <v-btn to="/nuevo_participante"
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                Añadir Manual
                
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn to="/subir_archivo"
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
                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  ><v-autocomplete
                      v-model="editedItem.razon_social"
                      title="razon social"
                      :items="razones"
                      dense
                      item-text="razon_social"
                      label="razon_social"
                      persistent-hint
                      return-object
                      single-line
                ></v-autocomplete>
                  </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4" >
                <v-autocomplete
                  v-model="editedItem.tipo_inscripcion"
                  :items="inscripciones"
                  item-text="tipo_inscripcion"
                  label="tipo_inscripcion"
                  persistent-hint
                  return-object
                  single-line   
                ></v-autocomplete>
                </v-col>

                <v-col cols="12"
                    sm="6"
                    md="4" >

                <v-text-field
                    v-model="editedItem.ocupacion"
                    label="ocupacion"
                    
                ></v-text-field>
                </v-col>
                </v-row>
  
   
                </v-row>

                <v-row>
                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-autocomplete
                  v-model="editedItem.nacionalidad"
                  :items="paises"
                  item-text="nacionalidad"
                  label="nacionalidad"
                  persistent-hint
                  return-object
                  single-line   
                ></v-autocomplete>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4">
                <v-select
                  v-model="nivel_educacional"
                  :items="nivelesEdu"
                  item-text="nivel_educacional"
                  label="nivel_educacional"
                  persistent-hint
                  return-object
                  single-line
                ></v-select>
                </v-col>
                <v-col cols="12"
                    sm="6"
                    md="4" >

                <v-text-field
                    v-model="editedItem.fecha_nacimiento"
                    label="fecha_nacimiento <YYYY-MM-DD>"
                    
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
                @click="editarParticipante"
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
        v-if="item.nivel_acceso!=0"
        small
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
            </v-data-table>
          </v-card>
        <v-dialog v-model="cambiarAcceso" max-width="500px">
          <v-card>
            <v-card-title v-if="token==0" class="text-h5">¿Quiere cambiar el nivel de acceso a administrador?</v-card-title>
            <v-card-title v-if="token==1" class="text-h5">¿Quiere cambiar el nivel de acceso a Jefe administrativo?</v-card-title>
            <v-card-title v-if="token==2" class="text-h5">¿Quiere cambiar el nivel de acceso a miembro CAI?</v-card-title>
            <v-card-title v-if="token==3" class="text-h5">¿Quiere cambiar el nivel de acceso a ejecutivo?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="cerrar">Cancelar</v-btn>
              <v-btn color="blue darken-1" text @click="confirmarCambiarAcceso">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-container>
</template>
<script>
//Importaciones

//librería axios
import axios from 'axios';
export default {

  data:()=>( {
    busqueda: null,
    cambiarAcceso:false,
    search: '',
    headers: [
      { text: 'Editar/Borrar', value: 'actions', sortable: false },
      { text: 'Administrador', value: 'administrador', sortable: false, align: 'center' },
      { text: 'Jefe administrativo', value: 'jefeAdmin', sortable: false, align: 'center' },
      { text: 'Miembro CAI', value: 'trabajador', sortable: false, align: 'center' },
      { text: 'Ejecutivo', value: 'ejecutivo', sortable: false, align: 'center' },
      {
        text: 'Rut',
        align: 'start',
        filterable: true,
        value: 'rut',
      },
      { text: 'nombre', value: 'nombre' },
      { text: 'apellido', value: 'apellido'},
      { text: 'correo', value: 'correo' },  
  
    ],

    usuarios:[
    ],
    usuario:{},

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
      correo_corporativo: '',
      correo_personal: '',
      fono_personal: '',
      fono_corporativo: '',
      razon_social: ''
    },
    token:'',
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
      correo_personal: '',
      fono_personal: '',
      fono_corporativo: '',
      razon_social: ''
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nuevo participante' : 'Editar participante'
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
    getUsuarios: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/cuenta/obtener/todos');
        this.usuarios = response.data;

        
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
    confirmacion(item,token){
      if(this.permisos()){
        this.token=token
        console.log(item)
        this.cambiarAcceso=true
        this.usuario=item
      }
      else{
        alert("No cuenta con permisos para edicion.")
      }
    },
    editarParticipante: async function(){
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
    eliminarCuenta: async function(){
      return 0
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
    editItem (item) {
      if(this.permisos()){
        this.editedIndex = this.participantes.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.editedItem.genero=this.mostrarGenero(this.editedItem.genero)
        console.log(this.editedItem.genero)
        this.dialog = true
      }
      else{
        alert("No cuenta con permisos para editar.")
      }
    },
    permisos:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://localhost:5000/cuenta/permisos?token='+data.token);
          return (response.data.nivel_acceso == 0)
        }
        catch(error){
          console.log(error)
        }
      }
      else{
        return false
      }
    },
    deleteItem (item) {
      if(this.permisos()){
        this.editedIndex = this.participantes.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("No cuenta con permisos para borrar.")
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
    saveBUP () {
      if (this.editedIndex > -1) {
        Object.assign(this.participantes[this.editedIndex], this.editedItem)
      } else {
        this.participantes.push(this.editedItem)
      }
      this.close()
    },
    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.participantes[this.editedIndex], this.editedItem)
      } else {
        editarParticipante()
      }
      this.close()
    },

    cerrar(){
      this.cambiarAcceso=false
    },
    confirmarCambiarAcceso: async function(){
      try{
        let response = await axios.put('http://localhost:5000/cuenta/editar_acceso', {id_cuenta:this.usuario.id , nivel_acceso: this.token});
        console.log(response);
      }
      catch(error){
        alert("Ocurrio un error.")
        console.log(error)
      }
      this.cerrar()
    },
  },
  created: async function(){
    if(await this.permisos()){
      this.getUsuarios()
    }
    else{
      window.location.href='/'
    }
    //this.mostrarGenero(valor)
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