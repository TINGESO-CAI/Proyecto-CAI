<template>
    <v-container class="test">
        <v-card>
            <v-data-table
              :headers="headers"
              :items="facturas"
              dense
              :search="search"
            >
             <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title> VISOR SOLICITUD FACTURAS</v-toolbar-title>
        <v-spacer></v-spacer>
          <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Busqueda"
                single-line
                hide-details
          ></v-text-field>
          <v-spacer></v-spacer>
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
            <v-btn to="/factura"
              color="primary"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              Agregar factura
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
                      v-model="editedItem.id_factura"
                      label="id_factura"
                    ></v-text-field>
                  </v-col>

                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.id_factura"
                      label="id_factura"
                    ></v-text-field>
                  </v-col>
                <!--hasta aqui-->
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
        @click="descargar(item)"
      >
        mdi-download
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
    facturas:[
      {     
        id_factura: 'test',
        sence: 'test',
        estado: 'test',
        num_hes: 'test',
        fecha_emision: 'test',
        fecha_vencimiento: 'test',
        enviar_factura: 'test',
        especificar: 'test',
        num_orden: 'test',
        observacion: 'test',
        num_cai:'test'
        
      }
    ],
    id_factura: 'test',
    sence: 'test',
    estado: 'test',
    num_hes: 'test',
    fecha_emision: 'test',
    fecha_vencimiento: 'test',
    enviar_factura: 'test',
    especificar: 'test',
    num_orden: 'test',
    observacion: 'test',
    num_cai:'test', 
    headers: [
      { text: 'Descargar/Borrar', value: 'actions', sortable: false },
      {
        text: 'id_factura',
        align: 'start',
        filterable: true,
        value: 'id_factura',
      },
      { text: 'sence', value: 'sence' },
      { text: 'estado', value: 'estado'},
      { text: 'num_hes', value: 'num_hes'},
      { text: 'f_emision', value: 'fecha_emision'},
      { text: 'f_vencimiento', value: 'fecha_vencimiento'},
      { text: 'enviar', value: 'enviar_factura'},
      { text: 'especif', value: 'especificar'},
      { text: 'N orden', value: 'num_orden'},
      { text: 'obs', value: 'observacion'},
      { text: 'num_cai', value: 'num_cai' },
      
      

  
    ],
    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    search: '',
    editedItem: {
      id_factura: '',
      sence: '',
      estado: '',
      num_hes: '',
      fecha_emision: '',
      fecha_vencimiento: '',
      enviar_factura: '',
      especificar: '',
      num_orden: '',
      observacion: '',
      num_cai:''
    },
    defaultItem: {
      id_factura: '',
      sence: '',
      estado: '',
      num_hes: '',
      fecha_emision: '',
      fecha_vencimiento: '',
      enviar_factura: '',
      especificar: '',
      num_orden: '',
      observacion: '',
      num_cai:''
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nueva factura' : 'Editar factura'
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
    getFacturas: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://'+process.env.IP_FRONT+':5000/factura/obtener?');
        this.facturas = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    descargar: async function (item) {
      if(await this.permisosPagina()){  
        window.location.href='http://'+process.env.IP_FRONT+':5000/factura/descargar/'+item.id_factura.toString()
      }
      else{
        alert("No cuenta con permisos para descargar.")
      }
    },
    deleteItem:async function (item) {
      if(await this.permisos()){
        this.editedIndex = this.facturas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("No cuenta con permisos para borrar.")
      }

    },
    deleteItemConfirm: async function() {
      try{
        let response= await axios.delete('http://'+process.env.IP_FRONT+':5000/factura/eliminar?id_factura='+this.editedItem.id_factura.toString())
        console.log(response)
        this.facturas.splice(this.editedIndex, 1)
        this.closeDelete()
      }
      catch(error){
        alert('No se puede eliminar la factura')
      }
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
        Object.assign(this.facturas[this.editedIndex], this.editedItem)
      } else {
        this.facturas.push(this.editedItem)
      }
      this.close()
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
    permisosPagina:async function(){
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
  created: async function(){
    if(await this.permisosPagina()){
      this.getFacturas()
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