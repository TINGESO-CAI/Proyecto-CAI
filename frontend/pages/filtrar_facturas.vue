<template>
    <v-container class="test">
    <div class="home">
        <h1>Filtro de facturas</h1>
        <div v-if="facturas.length==0">
        <p class="text-center"> Llene solo los parametros que desea filtrar</p>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >
                

                <v-col>
                <v-text-field
                    v-model="id_factura"
                    :counter="20"
                    label="id_factura"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="sence"
                    :counter="16"
                    label="sence" 
                ></v-text-field>
                </v-col>

                <v-col>
                <v-autocomplete
                    v-model="estado"
                    :items="estados"
                    :counter="16"
                    label="estado" 
                ></v-autocomplete>
                </v-col>

                
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="num_hes"
                    :counter="20"
                    label="num_hes"
                ></v-text-field>
                </v-col>
                
                <v-col>
                <v-text-field
                    v-model="fecha_emision"
                    :counter="20"
                    label="fecha_emision"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fecha_vencimiento"
                    :counter="20"
                    label="fecha_vencimiento"
                ></v-text-field>
                </v-col>

              </v-row>
              <v-row>
                <v-col>
                <v-autocomplete
                  v-model="enviar_factura"
                  :items="enviados"
                  label="envio 0:usach, 1:empresa, 2:otro"
                ></v-autocomplete>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="especificar"
                    :counter="20"
                    label="especificar"
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                  v-model="num_orden"
                  label="num_orden"
 
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="observacion"
                    :counter="20"
                    label="observacion"
                ></v-text-field>
                </v-col>

              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                  v-model="num_cai"
                  label="num_cai"
 
                ></v-text-field>
                </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  v-model="id_instancia"
                  label="id_instancia"
                ></v-text-field>
              </v-col>

            </v-row>
            </v-container>
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="filtro">Filtrar</v-btn>
        </div>
        </div>
        <div v-else>
      <br>
        <div>
          <v-card>
              <v-data-table
                :headers="headers"
                :items="facturas"
                dense
              ></v-data-table>
            </v-card>
        </div>
        <v-btn  color="blue lighten-1" class="mr-4" @click="limpiar">Limpiar</v-btn>
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
  name: 'Home',
  data:function(){
    return{
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
      num_cai:'',
      instancias:'',

      id_instancia: '',
      mandada: '',
      pagada: '',
      estados:["abierto","cerrado"],
      enviados:['0','1','2'], //0: usach, 1: empresa, 2: otro 
      headers: [
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
        
        { text: 'Editar/Borrar', value: 'actions', sortable: false },
  
      ],
      facturas : [],
      //FORMULARIO
      valid: false,
      message:'',
    }
  },
  methods:{
    async getRazones(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://52.188.153.77:5000/empresa/obtener/razon_social');
        this.razones = response.data;
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    limpiar: function(){
      console.log(this.facturas)
      this.facturas=[]
    },
    empyMessage:function(){
      alert("No existen facturas con esas caracteristicas.")
    },
    obtenerInstancias: async function(value){
      let response= axios.get('http://52.188.153.77:5000//instancia/obtener/id')
      return response
    },
    async filtro(){ //Filtrar facturas
      
      try {
       let ruta = 'http://52.188.153.77:5000/factura/obtener?'
       if (this.sence != '' ){
         ruta= ruta + 'sence='+this.sence +'&'
       }
       if (this.id_factura != '' ){
         ruta= ruta + 'id_factura='+this.id_factura +'&'
       }
       if (this.num_hes != '' ){
         ruta= ruta + 'num_hes='+this.num_hes +'&'
       }
       if (this.fecha_emision != '' ){
         ruta= ruta + 'fecha_emision='+this.fecha_emision +'&'
       }
       if (this.fecha_vencimiento != '' ){
         ruta= ruta + 'fecha_vencimiento='+this.fecha_vencimiento +'&'
       }
       if (this.enviar_factura != '' ){
         ruta= ruta + 'enviar_factura='+this.enviar_factura +'&'
       }
       if (this.especificar != '' ){
         ruta= ruta + 'especificar='+this.especificar +'&'
       }
       if (this.num_orden != '' ){
         ruta= ruta + 'num_orden='+this.num_orden +'&'
       }
       if (this.observacion != '' ){
         ruta= ruta + 'observacion='+this.observacion +'&'
       }
       if (this.num_cai != '' ){
         ruta= ruta + 'num_cai='+this.num_cai +'&'
       }
       
      if (ruta[ruta.length -1] == '&'){
        ruta[ruta.length -1]==''
      }
      
      let response = await axios.get(ruta)
      this.facturas= response.data
      console.log('response', response.data);
               
      if(this.facturas.length==0){
        this.empyMessage()
      }
        //limpiar
        this.id_factura = '';
        this.sence = '';
        this.estado = '';
        this.num_hes=''
        this.fecha_emision=''
        this.fecha_vencimiento=''
        this.enviar_factura=''
        this.especificar=''
        this.num_orden=''
        this.fecha_vencimiento=''
        this.num_cai=''
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
          let response = await axios.get('http://52.188.153.77:5000/cuenta/permisos?token='+data.token);
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
  border-color: #4e99fc
}

</style>