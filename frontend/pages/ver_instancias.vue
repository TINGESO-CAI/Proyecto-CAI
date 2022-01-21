<template>
    <v-container class="test" >
      <div v-if="page==1">
        <v-card>
            <v-data-table
              :headers="headers"
              :items="instancias"
              dense
              :search="search"
            >
            <template v-slot:[`item.malla`]="{ item }">
                <span>{{ mostrarMalla(item.malla) }}</span>
              </template>
              <template v-slot:top>
              <v-toolbar
                flat
              >
        <v-toolbar-title> VER INSTANCIAS</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
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
              <v-btn to="/instancia_curso"
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                + Instancia
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
                      v-model="editedItem.direccion"
                      label="Dirección"
                    ></v-text-field>
                  </v-col>
                <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.malla"
                      label="Malla"
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
                      v-model="editedItem.fecha_inicio"
                      label="Fecha inicio"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.fecha_termino"
                      label="Fecha termino"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-autocomplete
                      v-model="editedItem.estado"
                      :items="estados"
                      label="estado"
                      item-text="estado"
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
        @click="detalles(item)"
      >
        mdi-shape-square-plus
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
          </div>
          <div v-else-if="page==2">
          <v-card>
          <v-data-table
              :headers="headers2"
              :items="relatores"
              :search="search2"
              dense
            >
              <template v-slot:[`item.genero`]="{ item }">
                <span>{{ mostrarGenero(item.genero) }}</span>
              </template>
              <template v-slot:[`item.action`]="{item }">
                    <v-icon
                      small
                      class="mr-2"
                      @click="permitirEditar(item)"
                    >
                      mdi-pencil
                    </v-icon>
                    <v-icon
                      small
                      @click="verBorrarContacto(item)"
                    >
                      mdi-delete
                    </v-icon> 
              </template>

              <template v-slot:top>
                <v-toolbar
                flat
                class="test2"

              >
        <v-toolbar-title> Ver relatores de la instancia {{instancia.id_instancia}} </v-toolbar-title>
            <v-spacer></v-spacer>
          <v-text-field
                v-model="search2"
                append-icon="mdi-magnify"
                label="Busqueda"
                single-line
                hide-details
          ></v-text-field>
          <v-spacer></v-spacer>
                </v-toolbar>
              </template>
          </v-data-table>
          </v-card>       
          <br>
          <v-card>
          <v-data-table
              :headers="headers3"
              :items="participantes"
              :search="search3"
              dense
            >

              <template v-slot:[`item.genero`]="{ item }">
                <span>{{ mostrarGenero(item.genero) }}</span>
              </template>

              <template v-slot:[`item.emitidaS`]="{item }">
                    <v-icon
                      v-if="item.creada"
                      class="mr-2"
                      color="green darken-2"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.creada==false"
                      center
                      class="mr-2"
                      color="red darken-2"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>
              <template v-slot:[`item.emitidasF`]="{item }">
                    <v-icon
                      v-if="item.mandada"
                      class="mr-2"
                      color="green darken-2"
                      @click="confirmacion(item,1)"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.mandada==false"
                      center
                      class="mr-2"
                      color="red darken-2"
                      @click="confirmacion(item,1)"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>
              <template v-slot:[`item.facturasP`]="{item }">
                    <v-icon
                      v-if="item.pagada"
                      class="mr-2"
                      color="green darken-2"
                      @click="confirmacion(item,2)"
                    >
                      mdi-check-circle
                    </v-icon>
                    <v-icon
                      v-if="item.pagada==false"
                      center
                      class="mr-2"
                      color="red darken-2"
                      @click="confirmacion(item,2)"
                    >
                      mdi-close-circle
                    </v-icon>
              </template>

              <template v-slot:top>
                <v-toolbar
                flat
                class="test2"

              >
        <v-toolbar-title> Ver participantes de la instancia {{instancia.id_instancia}} </v-toolbar-title>
            <v-spacer></v-spacer>
          <v-text-field
                v-model="search3"
                append-icon="mdi-magnify"
                label="Busqueda"
                single-line
                hide-details
          ></v-text-field>
          <v-spacer></v-spacer>
                </v-toolbar>
              </template>
          </v-data-table>
          </v-card>   
          
            <v-btn  color="blue lighten-1" class="mr-3" @click="volver">Ver instancias</v-btn>        
        </div>
        <v-dialog v-model="cambiarEstado" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">¿Quiere cambiar el estado de esto?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="cerrar">Cancelar</v-btn>
              <v-btn color="blue darken-1" text @click="confirmarCambiarEstado">OK</v-btn>
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
    estados:["abierto","cerrado"],
    busqueda: null,
    search: '',
    search2:'',
    search3:'',
    page:1,
    instanciaEditar:{},
    cambiarEstado:false,
    headers: [
      { text: 'Editar/Detalles/Borrar', value: 'actions', sortable: false },
      {
        text: 'Id instancia',
        align: 'start',
        filterable: true,
        value: 'id_instancia',
      },
      { text: 'Sence', value: 'sence' },
      { text: 'Dirección', value: 'direccion'},
      { text: 'Malla', value: 'malla' },
      { text: 'Fecha inicio', value: 'fecha_inicio'},
      { text: 'Fecha termino', value: 'fecha_termino'},  
      { text: 'estado', value: 'estado'},
    ],
    headers2: [
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
    headers3: [
      { text: 'Solicitud emitida', value: 'emitidaS', sortable: false, align: 'center' },
      { text: 'Factura emitida', value: 'emitidasF', sortable: false, align: 'center' },
      { text: 'Factura pagada', value: 'facturasP', sortable: false, align: 'center' },
      { text: 'Factura', value: 'id_factura' },
      { text: 'Fecha emision S. factura', value: 'fecha_emision' },
      { text: 'Fecha vencimiento S. factura', value: 'fecha_vencimiento' },
      { text: 'Rut', value: 'rut' },
      { text: 'nombre', value: 'nombre' },
      { text: 'apellido_paterno', value: 'apellido_paterno'},
      { text: 'apellido_materno', value: 'apellido_materno' },
      { text: 'correo corporativo', value: 'correo_corporativo'},
      { text: 'fono corporativo', value: 'fono_corporativo'},
      { text: 'razon_social', value: 'razon_social'},
      { text: 'nacionalidad', value: 'nacionalidad'},
      { text: 'tipo_inscripcion', value: 'tipo_inscripcion'},
      { text: 'correo_personal', value: 'correo_personal'},
      { text: 'fono_personal', value: 'fono_personal'},
      { text: 'ocupacion', value: 'ocupacion'},
      { text: 'nivel_educacional', value: 'nivel_educacional'},
      { text: 'fecha_nacimiento', value: 'fecha_nacimiento'},
      { text: 'genero', value: 'genero'},
    ],

    instancias:[],

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
    instancia:{},
    participantes:[{genero:1,emitirS:false, emitirF:false, facturaPagada:true}],
    participante:{},
    relatores:[{genero:1}],
    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {
      id_instancia:'',
      sence:'',
      direccion:'',
      malla:'',
      fecha_inicio:'',
      fecha_termino:'',
      estado:'',
    },
    defaultItem: {
      id_instancia:'',
      sence:'',
      direccion:'',
      malla:'',
      fecha_inicio:'',
      fecha_termino:'',
      estado:'',
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nueva instancia' : 'Editar instancia'
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
    mostrarGenero(valor){
      if (valor == '1' ) return 'femenino'
      else if (valor == '2' ) return 'masculino'
      else return null
    },
    getInstancias: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/instancia/obtener?');
        this.instancias = response.data;

        
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    volver(){
      this.page=1
    },
    mostrarMalla(valor){
      if (valor == true ) return 'SI'
      else if (valor == false ) return 'NO'
      else return null
    },
    permisos:async function(){
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
    permisosFacturacion:async function(){
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
    editItem: async function(item) {
        if(await this.permisos()){
          this.editedIndex = this.instancias.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialog = true
        }
        else{
          alert("No cuenta con permisos para editar.")
        }
      },
    deleteItem: async function (item) {
      if(await this.permisos()){
        this.editedIndex = this.instancias.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("No cuenta con permisos para borrar.")
      }
    },
    deleteItemConfirm: async function() {
      this.instancias.splice(this.editedIndex, 1)
      try{
      let response= await axios.delete('http://localhost:5000/instancia/eliminar?id_instancia='+this.editedItem.id_instancia.toString())
      console.log(response.data)
      }
      catch(error){
        console.log(error)
        alert("Instancia no puede ser borrada")
      }
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
    detalles: async function(item){
      
      try{
        console.log(item)
        this.instancia=item
        this.page=2
        let response=await axios.get('http://localhost:5000/instancia/obtener_todo/'+this.instancia.id_instancia.toString())
        console.log(response.data)
        this.participantes=response.data.participante
        this.relatores=response.data.relatores
      }
      catch(error){
        console.log(error)
        alert("ocurrio un error")
      }
    },
    cerrar(){
      this.cambiarEstado=false
    },
    confirmacion: async function(item,token){
      if(await this.permisosFacturacion()){
        if(item.id_factura!=null){
        this.token=token
        console.log(item)
        this.cambiarEstado=true
        this.participante=item
        }
      }
      else{
        alert("No cuenta con permisos para edicion.")
      }
    },
    confirmarCambiarEstado(){
      if(this.token==1){
        this.cambiarEmisionFactura()
      }
      else{
        this.cambiarFacturaPagada()
      }
      this.cerrar()
    },
    cambiarEmisionFactura: async function(){
     if(this.participante.mandada){
        this.participante.mandada=false
      }
      else{
        this.participante.mandada=true
      }
      try{
        let response=await axios.put('http://localhost:5000/factura/editar?id_factura='+this.participante.id_factura.toString(),{mandada:this.participante.mandada,pagada:this.participante.pagada})
        console.log(response.data)
        let response2=await axios.get('http://localhost:5000/instancia/obtener_todo/'+this.instancia.id_instancia.toString())
        console.log(response.data)
        this.participantes=response2.data.participante

      }
      catch(error){
        console.log(error)
        alert("ocurrio un error")
      }
    },
    cambiarFacturaPagada: async function(){
     if(this.participante.pagada){
        this.participante.pagada=false
      }
      else{
        this.participante.pagada=true
      }
      try{
        let response=await axios.put('http://localhost:5000/factura/editar?id_factura='+this.participante.id_factura.toString(),{mandada:this.participante.mandada,pagada:this.participante.pagada})
        console.log(response.data)
        let response2=await axios.get('http://localhost:5000/instancia/obtener_todo/'+this.instancia.id_instancia.toString())
        console.log(response.data)
        this.participantes=response2.data.participante

      }
      catch(error){
        console.log(error)
        alert("ocurrio un error")
      }
    },
    save: async function() {
      if (this.editedIndex > -1) {
        Object.assign(this.instancias[this.editedIndex], this.editedItem)
        console.log(this.editedItem.malla)
        try{
          let response= await axios.put('http://localhost:5000/instancia/editar?id_instancia='+this.editedItem.id_instancia.toString(),{
            sence:this.editedItem.sence,
            malla:this.editedItem.malla,
            direccion: this.editedItem.direccion,
            fecha_termino:this.editedItem.fecha_termino,
            fecha_inicio:this.editedItem.fecha_inicio,
            estado:this.editedItem.estado
          })
        }
        catch(error){
          console.log(error)
        }
      } else {
        this.instancias.push(this.editedItem)
      }
      this.close()
    },
  },
  created: async function(){
    if(await this.permisosPagina()){
      this.getInstancias()
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
html, body {
  margin: 0px !important;
  padding: 0px !important;
}

</style>