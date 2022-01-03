<template>
    <v-container class="test">
        <v-card>
            <v-data-table
              :headers="headers"
              :items="empresas"
              dense
            >
             <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-toolbar-title> VISOR EMPRESAS</v-toolbar-title>
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
                      v-model="editedItem.id_empresa"
                      label="id_empresa"
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
    contador:0,
    departamentos : ["ingenieria","ciencias","humanidades"],
    nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
    paises: [ "Chilena","Otra"],
    razones: ["ninguna"],
    empresas:[
      {     
        razon_social: '',
        giro: '',
        atencion: '',
        departamento: '',
        rut: '',
        direccion: '',
        comuna: '',
        descripcion: '',
      }
    ],
    contacto:{     
        id_contacto: 'test',
        razon_social: 'test',
        correo: 'test',
        fono: 'test',
        descripcion: 'test',
    },
    contactos:[
      {     
        id_contacto: 'test',
        razon_social: 'test',
        correo: 'test',
        fono: 'test',
        descripcion: 'test',
      }
    ],
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
      { text: 'razon_social', value: 'razon_social', align: 'start',
        filterable: true},
      { text: 'giro', value: 'giro'},
      { text: 'atencion', value: 'atencion'},
      { text: 'departamento', value: 'departamento'},
      { text: 'rut', value: 'rut'},
      { text: 'direccion', value: 'direccion'},
      { text: 'comuna', value: 'comuna'},
      { text: 'contacto', value: 'contacto'},
      { text: 'Editar/Borrar', value: 'actions', sortable: false },
    ],
    //datos para editar
    dialog: false,
    dialogDelete: false,
    editedIndex: -1,
    editedItem: {
      id_empresa: 'test',
      sence: 'test',
      estado: 'test',
      num_hes: 'test',
      fecha_emision: 'test',
      fecha_vencimiento: 'test',
      enviar_empresa: 'test',
      especificar: 'test',
      num_orden: 'test',
      observacion: 'test',
      num_cai:'test'
    },
    defaultItem: {
      id_empresa: 'test',
      sence: 'test',
      estado: 'test',
      num_hes: 'test',
      fecha_emision: 'test',
      fecha_vencimiento: 'test',
      enviar_empresa: 'test',
      especificar: 'test',
      num_orden: 'test',
      observacion: 'test',
      num_cai:'test'
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
    getContactos: async function(){
      try {
        //se llama el servicio para obtener las emergencias 
        let response = await axios.get('http://localhost:5000/contacto/obtener?');
        this.contactos = response.data;
        console.log(response);
      }
      catch (error) {
        console.log('error', error); 
      }
    },
    editItem (item) {
        this.editedIndex = this.empresas.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
    deleteItem (item) {
      this.editedIndex = this.empresas.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
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
    save () {
      if (this.editedIndex > -1) {
        Object.assign(this.empresas[this.editedIndex], this.editedItem)
      } else {
        this.empresas.push(this.editedItem)
      }
      this.close()
    },
  },
  created(){
    this.getEmpresas()
    this.getContactos()
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