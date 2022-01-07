<template>
    <v-container class="test">
    <div class="home">
        <h1>Ingresar Nuevo relator</h1>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >
                <v-col>
                <v-text-field
                    v-model="rut"
                    :rules="rutRules"
                    :counter="16"
                    label="Rut"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="nombre"
                    :rules="nombreRules"
                    :counter="20"
                    label="Nombre"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="apellido_paterno"
                    :rules="apellido_paternoRules"
                    :counter="20"
                    label="Apellido paterno"
                    required
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="apellido_materno"
                    :rules="apellido_maternoRules"
                    :counter="20"
                    label="Apellido materno"
                    required
                ></v-text-field>
                </v-col>
                <v-col>
                <v-select
                    v-model="genero"
                    :items="generos"
                    item-text="genero"
                    label="genero"
                    persistent-hint
                    return-object
                    single-line   
                    
                ></v-select>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="titulo"
                    :rules="tituloRules"
                    :counter="40"
                    label="titulo"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fecha_nacimiento"
                    :rules="fecha_nacimientoRules"
                    :counter="20"
                    label="fecha_nacimiento (YYYY-MM-DD)"
                    required
                ></v-text-field>
                </v-col>
                
              </v-row>
              <v-row>
                

                <v-col>
                <v-text-field
                    v-model="numero_cuenta"
                    :rules="numero_cuentaRules"
                    :counter="20"
                    label="numero_cuenta"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-select
                  v-model="banco"
                  :items="bancos"
                  item-text="banco"
                  label="banco"
                  persistent-hint
                  return-object
                  single-line   
                ></v-select>
                </v-col>
                <v-col>
                <v-select
                    v-model="tipo_cuenta"
                    :items="tipos"
                    item-text="tipo_cuenta"
                    label="tipo_cuenta"
                    persistent-hint
                    return-object
                    single-line
                ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="correo_personal"
                    :rules="correo_personalRules"
                    :counter="30"
                    label="correo_personal"
                    required
                ></v-text-field>
                </v-col>

                <v-col>
                <v-text-field
                    v-model="fono_personal"
                    :rules="fono_personalRules"
                    :counter="15"
                    label="fono_personal"
                    required
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                  <v-col>
              <v-text-field
                      v-model="correo_corporativo"
                      :rules="correo_corporativoRules"
                      :counter="20"
                      label="correo_corporativo"
                ></v-text-field>
                </v-col>
                <v-col>
                <v-text-field
                    v-model="fono_corporativo"
                    :rules="fono_corporativoRules"
                    :counter="15"
                    label="fono_corporativo"
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="cv"
                    :rules="cvss"
                    :counter="100"
                    label="link curriculo"
                    required
                ></v-text-field>
                </v-col>
                
            </v-row>
            </v-container>
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="createRelator">Crear</v-btn>
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
      bancos: ["BANCOESTADO","BANCO DE CHILE/EDWARDS","BANCO INTERNACIONAL","SCOTIABANK CHILE/Desarrollo",
      "BANCO DE CREDITO E INVERSIONES","BANCO BICE","HSBC BANK","BANCO SANTANDER/Banefe",
      "ITAÚ CORPBANCA","BANCO SECURITY","BANCO FALABELLA","BANCO RIPLEY","BANCO CONSORCIO",
      "SCOTIABANK AZUL","BANCO BTG",
      ],
      paises: [ "Chilena","Otra"],
      tipos: ["corriente","vista","chequera electrónica","ahorro"],
      //FORMULARIO
      valid: false,
      message:'',

      rut: '',
      nombre: '',
      apellido_paterno: '',
      apellido_materno: '',
      titulo: '',
      cv: '',
      fecha_nacimiento: '',
      numero_cuenta: '',
      banco: '',
      tipo_cuenta: '',
      genero:'',
      generos : ["masculino","femenino"],
      correo_corporativo: '',
      correo_personal: '',
      fono_personal: '',
      fono_corporativo: '',
      //reglas
      rutRules: [
        v => !!v || 'Rut es requerido',
        v => v.length <= 12 || 'Rut debe contener menos de 12 caracteres',
      ],
      nombreRules: [
        v => !!v || 'Nombre es requerido',
        v => v.length <= 100 || 'Nombre debe contener menos de 100 caracteres',
      ],
      apellido_paternoRules: [
        v => !!v || 'apellido_paterno es requerido',
        v => v.length <= 100 || 'apellido_paterno debe contener menos de 100 caracteres',
      ],
      apellido_maternoRules: [
        v => !!v || 'apellido_materno es requerido',
        v => v.length <= 100 || 'apellido_materno debe contener menos de 100 caracteres',
      ],
      tituloRules: [
        v => !!v || 'titulo es requerido',
        v => v.length <= 100 || 'titulo debe contener menos de 100 caracteres',
      ],
      //fecha_nacimientoRules: [
        //v => !!v || 'fecha_nacimiento es requerido',
        //v => /.+-+/+-+/test(v) || 'fecha_nacimiento debe ser válido',
      //]
    }
  },
  methods:{
    successMessage:function(){
      alert("El relator se creo exitosamente.")
    },
    mostrarGenero(valor){
      if (valor == 'femenino' ) return 1
      else if (valor == 'masculino' ) return 2
      else return ''
    },
    comprobarFecha:function(fecha){
      if (fecha.split('-').length == 3){
        return true
      }
      else{
        return false
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
    async createRelator(){ //Crear un nuevo PARTICIPANTE
      this.message = '';
      let newRelator ={
        rut: this.rut,
        nombre: this.transformarVacio(this.nombre),
        apellido_paterno: this.transformarVacio(this.apellido_paterno),
        apellido_materno: this.transformarVacio(this.apellido_materno),
        titulo: this.transformarVacio(this.titulo),
        cv: this.transformarVacio(this.cv),
        fecha_nacimiento: this.transformarVacio(this.fecha_nacimiento),
        numero_cuenta: this.transformarVacio(this.numero_cuenta),
        banco: this.transformarVacio(this.banco),
        tipo_cuenta: this.transformarVacio(this.tipo_cuenta),
        genero:this.transformarVacio(this.mostrarGenero(this.genero)),
        fono_personal:this.transformarVacio(this.fono_personal),
        fono_corporativo:this.transformarVacio(this.fono_corporativo),
        correo_personal:this.transformarVacio(this.correo_personal),
        correo_corporativo:this.transformarVacio(this.correo_corporativo)
      }
      if(this.rut.split('-').length==2){
        if(this.comprobarFecha(this.fecha_nacimiento) || this.fecha_nacimiento==''){        
          try {
            //se llama el servicio para crear un nuevo relator
            let response = await axios.post('http://localhost:5000/relator/agregar',newRelator);
            console.log('response', response.data);
            let id = response.data.id;
            this.message = `${this.rut} fue creado con éxito con id: ${id}`;
            
            //limpiar
            this.rut= ''
            this.nombre= ''
            this.apellido_paterno= ''
            this.apellido_materno= ''
            this.titulo= ''
            this.cv= ''
            this.fecha_nacimiento= ''
            this.numero_cuenta= ''
            this.banco= ''
            this.tipo_cuenta= ''
            this.genero=''
            this.correo_corporativo= ''
            this.correo_personal= ''
            this.fono_personal= ''
            this.fono_corporativo= ''
            if(response.data.respuesta=="El relator ya ha sido ingresado"){
              alert("El relator ya existe.")
            }
            else{
              this.successMessage();
            }
          }
          catch (error) {
          console.log('error', error); 
          this.message = 'Ocurrió un error'
          }
        }
        else{
          alert("Error formato fecha.")
        }
      }
      else{
        alert("Debe ingresar el rut de manera correcta")
      }
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