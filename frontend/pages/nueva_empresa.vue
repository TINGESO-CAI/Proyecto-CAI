<template>
    <v-container class="test">
    <div class="home">
        <h1>Ingresar Nueva empresa</h1>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >

                <v-col>
                <v-text-field
                    v-model="razon_social"
                    :counter="20"
                    label="razon_social"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="giro"
                    :counter="20"
                    label="Giro"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="atencion"
                    :counter="20"
                    label="Atencion"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                      v-model="departamento"

                      item-text="departamento"
                      label="departamento"
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                
                <v-col>
                <v-text-field
                    v-model="rut"
                    :counter="16"
                    label="Rut"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="direccion"
                    :rules="direccionRules"
                    :counter="20"
                    label="direccion"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-autocomplete
                      v-model="comuna"
                      :items="comunas"
                      item-text="comuna"
                      label="comuna"
                      persistent-hint
                      return-object
                      single-line
                ></v-autocomplete>
                </v-col>
                <v-col>
                <v-btn  color="blue lighten-1" class="mr-4" @click="createEmpresa">Crear empresa</v-btn>
                </v-col>
              </v-row>
                
                <!--contacto agregar-->
              
            </v-container>
        </v-form>
        
        
        </div>
    </div>
    </v-container>
</template>
<script>
//Importaciones

//librería axios
import axios from 'axios';

export default {
  name: 'Home',
  data:function(){
    return{
      contador:0,
      nivelesEdu : ["básica incompleta","básica completa","media incompleta","media completa","técnico profesional","superior completa","desconocido","otro"],
      paises: [ "Chilena","Otra"],
      razones: ["ninguna"],
      //FORMULARIO
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
      correo: '',
      fono: '',
      descripcion: '',
      //reglas
      rutRules: [
        v => !!v || 'Rut es requerido',
        v => v.length <= 12 || 'Rut debe contener menos de 12 caracteres',
      ],
      razon_socialRules: [
        v => !!v || 'razon_social es requerido',
        v => v.length <= 100 || 'razon_social debe contener menos de 100 caracteres',
      ],
      giroRules: [
        v => !!v || 'giro es requerido',
        v => v.length <= 100 || 'giro debe contener menos de 100 caracteres',
      ],
      atencionRules: [
        v => !!v || 'atencion es requerido',
        v => v.length <= 100 || 'atencion debe contener menos de 100 caracteres',
      ],
      correoRules: [
        v => !!v || 'Correo es requerido',
        v => /.+@.+/.test(v) || 'Correo debe ser válido',
      ],
      direccionRules: [
        v => !!v || 'direccion es requerido',
        //v => /.+.+/.test(v) || 'direccion debe ser válido',
      ],
      fonoRules: [
        v => !!v || 'fono es requerido',
        v => v.length <= 12 || 'fono debe contener menos de 12 caracteres',
      ],
    }
  },
  methods:{
    successMessage:function(){
      alert("La empresa se creo exitosamente.")
    },
    successMessageC:function(){
      alert("El contacto se creo exitosamente.")
    },

    transformarVacio: function(valor){
      if(valor==''){
        return null
      }
      else{
        return valor
      }
    },
    async createEmpresa(){ //Crear un nuevo empresa
      this.message = '';
      if(this.razon_social!=''){
        let newEmpresa ={
          
          razon_social: this.razon_social,
          giro: this.transformarVacio(this.giro),
          atencion: this.transformarVacio(this.atencion),
          departamento: this.transformarVacio(this.departamento),
          rut: this.transformarVacio(this.rut),
          direccion: this.transformarVacio(this.direccion),
          comuna: this.transformarVacio(this.comuna)
        }
        
        try {
          //se llama el servicio para crear una nueva empresa
          let response = await axios.post('http://localhost:5000/empresa/agregar' ,newEmpresa);
          console.log('response', response.data);
          let id = response.data.id;
          this.message = `${this.razon_social} fue creado con éxito con id: ${id}`;
          //limpiar
          if(response.data.respuesta == "La empresa ya ha sido ingresada"){
            alert("La empresa ya existe.")
          }
          else{
            this.successMessage();
          }
        }
        catch (error) {
        console.log('error', error); 
        alert('Ocurrió un error')
        }
      }
      else{
        alert("Es necesario ingresar la razon social")
      }
    },
    async createContacto(){ //Crear un nuevo contacto apra empresa
      this.message = '';

      console.log(this.razon_social != '')
      let newContacto={ 
        id_contacto: this.razon_social+'1',
        correo: this.transformarVacio(this.correo),
        fono: this.transformarVacio(this.fono),
        descripcion: this.transformarVacio(this.descripcion),
        razon_social: this.razon_social
      }
      let check= await axios.get('http://localhost:5000/empresa/obtener?razon_social='+this.razon_social)
      console.log(check.data)
      if (check.data.length==1){
        try {
          //se llama el servicio para crear un nuevo contacto
          let response = await axios.post('http://localhost:5000/contacto/agregar',newContacto);
          console.log('response', response.data);
          let id = response.data.id;
          this.message = `El contacto de ${this.razon_social} fue creado con éxito con id: ${id}`;
          //limpiar
          this.correo=''
          this.fono=''
          this.descripcion=''
          alert("Contacto creado con exito.")
          this.contador++;
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
    }
  },

  created(){
    if(this.permisos()==false){
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