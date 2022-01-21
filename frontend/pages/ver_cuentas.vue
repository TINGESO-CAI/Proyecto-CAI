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
                </v-row>
                <v-row>
                <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.apellido"
                      label="apellido"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.correo"
                      label="correo"
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
                @click="editarCuenta"
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
              <v-btn color="blue darken-1" text @click="eliminarCuenta">OK</v-btn>
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
    getCuentas: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/cuenta/obtener/todos');
        
        this.usuarios = response.data;
        console.log(this.usuarios)
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
        this.token=token
        this.cambiarAcceso=true
        this.usuario=item
    },
    validaRut : function (rutCompleto) {
		if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test( rutCompleto ))
			return false;
		var tmp 	= rutCompleto.split('-');
		var digv	= tmp[1]; 
		var rut 	= tmp[0];
		if ( digv == 'K' ) digv = 'k' ;
		return (this.dv(rut) == digv );
    },
    dv : function(T){
      var M=0,S=1;
      for(;T;T=Math.floor(T/10))
        S=(S+T%10*(9-M++%6))%11;
      return S?S-1:'k';
    },
    editarCuenta: async function(){
      let newCuenta ={
        id:this.editedItem.id,
        rut: this.transformarVacio(this.editedItem.rut),
        nombre: this.transformarVacio(this.editedItem.nombre),
        apellido: this.transformarVacio(this.editedItem.apellido),
        correo: this.transformarVacio(this.editedItem.correo)
      }
      if(this.validaRut(this.editedItem.rut)==false){
        alert("rut invalido.")
        return 0
      }
      console.log(this.editedItem.id)
      try {
        await axios.put('http://localhost:5000/cuenta/editar',newCuenta);
        this.close();
        this.editedItem.rut=newCuenta.rut
        this.editedItem.correo=newCuenta.correo
        this.editedItem.apellido=newCuenta.apellido
        this.editedItem.nombre=newCuenta.nombre
        Object.assign(this.usuarios[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }

    },
    eliminarCuenta: async function(){
      try {
        let response = await axios.delete('http://localhost:5000/cuenta/eliminar?id='+this.editedItem.id);
        console.log(response);
        this.closeDelete();
        Object.assign(this.usuarios[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
    editItem (item) {
        this.editedIndex = this.usuarios.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
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
        this.editedIndex = this.usuarios.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
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
        this.usuario.nivel_acceso=this.token
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
      this.getCuentas()
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