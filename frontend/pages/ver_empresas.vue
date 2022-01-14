<template>
    <v-container class="test">
    <div v-if="page==1">
        <v-card>
            <v-data-table
              :headers="headers"
              :items="empresas"
              dense
              :search="search"
            >
             <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title> VISOR EMPRESAS</v-toolbar-title>
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
            <v-btn to="/nueva_empresa"
              color="primary"
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              Agregar empresa
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
                      v-model="editedItem.razon_social"
                      label="razon_social"
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
                      v-model="editedItem.giro"
                      label="giro"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.atencion"
                      label="atencion"
                    ></v-text-field>
                  </v-col>
                </v-row>
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
                <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.departamento"
                      item-text="departamento"
                      label="departamento"
                ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                    <v-text-field
                      v-model="editedItem.direccion"
                      label="direccion"
                    ></v-text-field>
                  </v-col>
                </v-row>

                <v-row>
                  <v-col
                    cols="12"
                    sm="6"
                    md="4"
                  >
                  <v-autocomplete
                      v-model="editedItem.comuna"
                      :items="comunas"
                      item-text="comuna"
                      label="comuna"
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
                @click="editarEmpresa"
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
              <v-btn color="blue darken-1" text @click="eliminarEmpresa">OK</v-btn>
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
        @click="paginaContactos(item)"
      >       
        mdi-cellphone-basic
      </v-icon>
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
      
        </div>
        <div v-else-if="page==2">
          <v-card>
          <v-data-table
              :headers="headers2"
              :items="contactos"
              :search="search2"
              dense
            >
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
        <v-toolbar-title> Ver contactos de {{razon_social}} </v-toolbar-title>
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
          <div v-if="permisos()">
          <v-row>
              <h3>Ingresar nuevo contacto</h3>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="razon_social"
                    :rules="razon_socialRules"
                    :counter="20"
                    label="razon_social"
                    required
                    readonly
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="correo"
                    :rules="correoRules"
                    :counter="20"
                    label="correo"
                    required
                    dense
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="fono"
                    :rules="fonoRules"
                    :counter="15"
                    label="fono"
                    required
                    dense
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="descripcion"
                    :rules="descripcionRules"
                    :counter="20"
                    label="descripcion"
                    required
                    dense
                ></v-text-field>
                </v-col>
                
            </v-row>
            </div>
            <v-btn  color="blue lighten-1" class="mr-3" @click="volver">Ver empresas</v-btn>
            <v-btn  v-if="permisos()" color="blue lighten-1" class="mr-3" @click="createContacto">Agregar contacto</v-btn>
            
            <v-dialog v-model="confirmarEliminarContacto" max-width="500px">
              <v-card>
                <v-card-title class="text-h5">¿Quieres eliminar esto?</v-card-title>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="cancelar">Cancelar</v-btn>
                  <v-btn color="blue darken-1" text @click="borrarContacto">OK</v-btn>
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
            <v-dialog v-model="editar" max-width="500px">
              <v-card>
            <v-card-title class="text-h5">Editar contacto</v-card-title>
                <v-card-text>
                <v-row>
                    <v-text-field
                        v-model="razon_social"
                        :rules="razon_socialRules"
                        :counter="20"
                        label="razon_social"
                        required
                        readonly
                    ></v-text-field>
                    <v-text-field
                        v-model="contactoEditar.correo"
                        :rules="correoRules"
                        :counter="20"
                        label="correo"
                        required
                        dense
                    ></v-text-field>
                </v-row>
                <v-row>
                    <v-text-field
                        v-model="contactoEditar.fono"
                        :rules="fonoRules"
                        :counter="15"
                        label="fono"
                        required
                        dense
                    ></v-text-field>
                    <v-text-field
                        v-model="contactoEditar.descripcion"
                        :rules="descripcionRules"
                        :counter="20"
                        label="descripcion"
                        required
                        dense
                    ></v-text-field>
                </v-row>
                </v-card-text>
                <v-card-actions>
                <v-row>
                <v-btn  color="blue lighten-1" class="mr-3" @click="ocultar">Ocultar</v-btn>
                <v-btn  color="blue lighten-1" class="mr-3" @click="editarContacto">Editar contacto</v-btn>
                </v-row>
                </v-card-actions>
              </v-card>
            </v-dialog>
        </div>
    </v-container>
</template>
<script>
//Importaciones

//librería axios
import axios from 'axios';
export default {

  data:()=>( {
    busqueda: null,
    confirmarEliminarContacto:false,
    editar:false,
    search:'',
    search2:'',
    page:1,
    contador:0,
    departamentos : ["ingenieria","ciencias","humanidades"],
    nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
    paises: [ "Chilena","Otra"],
    razones: ["ninguna"],
    empresas:[],
    contacto:{     
        id_contacto: 'test',
        razon_social: 'test',
        correo: 'test',
        fono: 'test',
        descripcion: 'test',
    },
    contactos:[ ],
    contactoEditar:{},
    valid: false,
    message:'',
    comunas:["Arica","Camarones","General Lagos","Putre", "Alto Hospicio","Camiña","Colchane","Huara","Iquique","Pica","Pozo Almonte","Antofagasta","Calama","María Elena","Mejillones","Ollagüe","San Pedro de Atacama","Sierra Gorda","Taltal","Tocopilla","Alto del Carmen","Caldera","Chañaral","Copiapó","Diego de Almagro","Freirina","Huasco","Tierra Amarilla","Vallenar","Andacollo","Canela","Combarbalá","Coquimbo","Illapel","La Higuera","La Serena","Los Vilos","Monte Patria","Ovalle","Paiguano","Punitaqui","Río Hurtado","Salamanca","Vicuña","Algarrobo","Cabildo","Calera","Calle Larga","Cartagena","Casablanca","Catemu","Concón","El Quisco","El Tabo","Hijuelas","Isla de Pascua","Juan Fernández","La Cruz","La Ligua","Limache","Llaillay","Los Andes","Nogales","Olmué","Panquehue","Papudo","Petorca","Puchuncaví","Putaendo","Quillota","Quilpué","Quintero","Rinconada","San Antonio","San Esteban","San Felipe","Santa María","Santo Domingo","Valparaíso","Villa Alemana","Viña del Mar","Zapallar","Alhué","Buin","Calera de Tango","Cerrillos","Cerro Navia","Colina","Conchalí","Curacaví","El Bosque","El Monte","Estación Central","Huechuraba","Independencia","Isla de Maipo","La Cisterna","La Florida","La Granja","La Pintana","La Reina","Lampa","Las Condes","Lo Barnechea","Lo Espejo","Lo Prado","Macul","Maipú","María Pinto","Melipilla","Ñuñoa","Padre Hurtado","Paine","Pedro Aguirre Cerda","Peñaflor","Peñalolén","Pirque","Providencia","Pudahuel","Puente Alto","Quilicura","Quinta Normal","Recoleta","Renca","San Bernardo","San Joaquín","San José de Maipo","San Miguel","San Pedro","San Ramón","Santiago","Talagante","Tiltil","Vitacura","Chimbarongo","Chépica","Codegua","Coinco","Coltauco","Doñihue","Graneros","La Estrella","Las Cabras","Litueche","Lolol","Machalí","Malloa","Marchihue","Nancagua","Navidad","Olivar","Palmilla","Paredones","Peralillo","Peumo","Pichidegua","Pichilemu","Placilla","Pumanque","Quinta de Tilcoco","Rancagua","Rengo","Requínoa","San Fernando","San Francisco de Mostazal","San Vicente de Tagua Tagua","Santa Cruz", "Cauquenes","Chanco","Colbún","Constitución","Curepto","Curicó","Empedrado","Hualañé","Licantén","Linares","Longaví","Maule","Molina","Parral","Pelarco","Pelluhue","Pencahue","Rauco","Retiro","Romeral","Río Claro","Sagrada Familia","San Clemente","San Javier de Loncomilla","San Rafael","Talca","Teno","Vichuquén","Villa Alegre","Yerbas Buenas","Bulnes","Chillán Viejo","Chillán","Cobquecura","Coelemu","Coihueco","El Carmen","Ninhue","Ñiquén","Pemuco","Pinto","Portezuelo","Quillón","Quirihue","Ránquil","San Carlos","San Fabián","San Ignacio","San Nicolás","Treguaco","Yungay","Alto Biobío","Antuco","Arauco","Cabrero","Cañete","Chiguayante","Concepción","Contulmo","Coronel","Curanilahue","Florida","Hualpén","Hualqui","Laja","Lebu","Los Álamos","Los Ángeles","Lota","Mulchén","Nacimiento","Negrete","Penco","Quilaco","Quilleco","San Pedro de la Paz","San Rosendo","Santa Bárbara","Santa Juana","Talcahuano","Tirúa","Tomé","Tucapel","Yumbel", "Angol","Carahue","Cholchol","Collipulli","Cunco","Curacautín","Curarrehue","Ercilla","Freire","Galvarino","Gorbea","Lautaro","Loncoche","Lonquimay","Los Sauces","Lumaco","Melipeuco","Nueva Imperial","Padre las Casas","Perquenco","Pitrufquén","Pucón","Purén","Renaico","Saavedra","Temuco","Teodoro Schmidt","Toltén","Traiguén","Victoria","Vilcún","Villarrica","Corral","Futrono","La Unión","Lago Ranco","Lanco","Los Lagos","Mariquina","Máfil","Paillaco","Panguipulli","Río Bueno","Valdivia", "Ancud","Calbuco","Castro","Chaitén","Chonchi","Cochamó","Curaco de Vélez","Dalcahue","Fresia","Frutillar","Futaleufú","Hualaihué","Llanquihue","Los Muermos","Maullín","Osorno","Palena","Puerto Montt","Puerto Octay","Puerto Varas","Puqueldón","Purranque","Puyehue","Queilén","Quellón","Quemchi","Quinchao","Río Negro","San Juan de la Costa","San Pablo", "Aisén","Chile Chico","Cisnes","Cochrane","Coihaique","Guaitecas","Lago Verde","O’Higgins","Río Ibáñez","Tortel", "Antártica","Cabo de Hornos (Ex Navarino)","Laguna Blanca","Natales","Porvenir","Primavera","Punta Arenas","Río Verde","San Gregorio","Timaukel","Torres del Paine"],
    razon_social: '',
    giro: '',
    atencion: '',
    departamento: '',
    rut: '',
    direccion: '',
    comuna: '',
    id_contacto: '',
    razon_social: '',
    correo: '',
    fono: '',
    descripcion: '',

    headers: [

      { text: 'Contacto/Editar/Borrar', value: 'actions', sortable: false },
      { text: 'razon_social', value: 'razon_social', align: 'start',
        filterable: true},
      { text: 'giro', value: 'giro'},
      { text: 'atencion', value: 'atencion'},
      { text: 'departamento', value: 'departamento'},
      { text: 'rut', value: 'rut'},
      { text: 'direccion', value: 'direccion'},
      { text: 'comuna', value: 'comuna'},
    ],
    headers2: [

      { text: 'Editar/Borrar', value: 'action', sortable: false},
      { text: 'Id contacto', value: 'id_contacto', align: 'start',
        filterable: true},
      { text: 'Correo', value: 'correo'},
      { text: 'Fono', value: 'fono'},
      { text: 'Descripción', value: 'descripcion'},
    ],
    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {
      razon_social: '',
      giro: '',
      atencion: '',
      departamento: '',
      rut: '',
      direccion: '',
      comuna: '',
    },
    defaultItem: {
      razon_social: '',
      giro: '',
      atencion: '',
      departamento: '',
      rut: '',
      direccion: '',
      comuna: '',
    }, 
  }),
  //funciones para editar
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Nueva empresa' : 'Editar empresa'
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
    getEmpresas: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/empresa/obtener?');
        this.empresas = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    verBorrarContacto(item){
      if(this.permisos()){
        this.contactoEditar=item
        this.confirmarEliminarContacto=true
      }
      else{
        alert("No cuenta con permisos para borrar")
      }
    },
    cancelar(){
      this.confirmarEliminarContacto=false
    },
    borrarContacto:async function(){
      try{
        let response = await axios.delete('http://localhost:5000/contacto/eliminar?id_contacto='+this.contactoEditar.id_contacto)
        console.log(response.data)
        this.getContactos(this.editedItem)
        this.cancelar()
      }
      catch(error){
        alert("Ocurrio un error")
        console.log(error)
      }
    },
    editarEmpresa: async function(item){
      console.log(item)
      let newEmpresa ={
        razon_social: this.editedItem.razon_social,
        giro: this.transformarVacio(this.editedItem.giro),
        atencion: this.transformarVacio(this.editedItem.atencion),
        departamento: this.transformarVacio(this.editedItem.departamento),
        rut: this.transformarVacio(this.editedItem.rut),
        direccion: this.transformarVacio(this.editedItem.direccion),
        comuna: this.transformarVacio(this.editedItem.comuna)
      }
      try{ 
        let response = await axios.put('http://localhost:5000/empresa/editar?razon_social='+newEmpresa.razon_social,newEmpresa);
        console.log(response);
        this.close();
        Object.assign(this.empresas[this.editedIndex], this.editedItem)
        this.editar=false
      }
      catch(error){
        console.log(error)
        alert("ocurrio un error")
      }
    },
    eliminarEmpresa: async function(){
      try {
        let response = await axios.delete('http://localhost:5000/empresa/eliminar?razon_social='+this.editedItem.razon_social);
        console.log(response);
        this.closeDelete();
        Object.assign(this.empresas[this.editedIndex], this.editedItem)
      }
      catch (error) {
        console.log('error', error);
      }
    },
    ocultar: function(){
      this.editar=false
    },
    permitirEditar: function(item){
      if(this.permisos()){
        this.editar=true
        this.contactoEditar=item
      }
      else{
        alert("No cuenta con permisos para editar.")
      }
    },
    paginaContactos:function(item){
      this.editedIndex = this.empresas.indexOf(item)
      this.editedItem = Object.assign({}, item)
      if(this.getContactos(this.editedItem)){
        console.log("contactos:",this.contactos)
        this.razon_social=this.editedItem.razon_social
        this.page=2
      }
    },
    getContactos: async function(item){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/contacto/obtener?razon_social='+item.razon_social);
        this.contactos = response.data;
        console.log(response);
        return true
      }
      catch (error) {
        console.log('error', error);
        return false
      }
    },
    editItem (item) {
        if(this.permisos()){
          this.editedIndex = this.empresas.indexOf(item)
          this.editedItem = Object.assign({}, item)
          this.dialog = true
        }
        else{
          alert("No cuenta con permisos para editar.")
        }
      },
    deleteItem (item) {
      if(this.permisos()){
        this.editedIndex = this.empresas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialogDelete = true
      }
      else{
        alert("No cuenta con permisos para borrar.")
      }
    },
    deleteItemConfirm () {
      this.empresas.splice(this.editedIndex, 1)
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
    editarContacto: async function () {
      console.log((this.contactoEditar))
      let newContacto ={
        correo: this.transformarVacio(this.contactoEditar.correo),
        fono: this.transformarVacio(this.contactoEditar.fono),
        descripcion: this.transformarVacio(this.contactoEditar.descripcion),
        razon_social: this.transformarVacio(this.razon_social)
      }
      try{ 
        let response = await axios.put('http://localhost:5000/contacto/editar?id_contacto='+this.contactoEditar.id_contacto,newContacto);
        console.log(response);

      }
      catch(error){
        console.log(error)
        alert("ocurrio un error")
      }
      this.editar=false
    },
    permisos(){
      let data=localStorage.getItem("user")
      console.log(data)
        if(data!=null){
          return true
            /*data=JSON.parse(data)
            if(data.permiso==3){
              return true
            }
            else{
              return false
            }
            */
        }
        else{
          return false
        }
    },
    volver(){
      this.page=1
      this.editar=false
    },
    comprobarTelefono(fono){
      if (fono==''){
        return true
      }
      if(fono.length!=9){
        if(fono[0]=='+' && fono.length==12){
          return true
        }
        else{
          return false
        }
      }
      else{
        if(fono[0]!='+'){
          return true
        }
        else{
          return false
        }
      }
    },


    async createContacto(){ //Crear un nuevo contacto apra empresa
      this.message = '';

      console.log(this.razon_social != '')
      let newContacto={ 
        correo: this.transformarVacio(this.correo),
        fono: this.transformarVacio(this.fono),
        descripcion: this.transformarVacio(this.descripcion),
        razon_social: this.razon_social
      }
      let check= await axios.get('http://localhost:5000/empresa/obtener?razon_social='+this.razon_social)
      console.log(check.data)
      if (check.data.length==1){
        if(this.comprobarTelefono(this.fono)==false){
          alert("Error en formato de telefono.")
          return 0
        }
        try {
          //se llama el servicio para crear un nuevo contacto
          let response = await axios.post('http://localhost:5000/contacto/agregar',newContacto);
          console.log('response', response.data);
          let id = response.data.id;
          this.message = `${this.id_contacto} fue creado con éxito con id: ${id}`;
          //limpiar
          this.correo=''
          this.fono=''
          this.descripcion=''
          alert("Contacto creado con exito.")
          this.getContactos(this.editedItem)
        }
        catch (error) {
        console.log('error', error); 
        alert('Ocurrió un error')
        }
      }
      else{
        alert('Debe ingresar una razon social valida')
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
  },
  created(){
    this.getEmpresas()
    //this.getContactos()
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