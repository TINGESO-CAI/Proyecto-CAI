<template>
    <v-container class="test">
    <div class="home">
        <h1>Ingresar Nuevo Usuario</h1>
        <br>
        <div>
        <v-form v-model="valid">
            <v-container >
            <v-row >
                <v-col>
                <v-text-field
                    v-model="rut"
                    :counter="16"
                    label="Rut"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row >
                <v-col>
                <v-text-field
                    v-model="nombre"
                    :counter="16"
                    label="Nombre"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row >
                <v-col>
                <v-text-field
                    v-model="apellido"
                    :counter="16"
                    label="apellido"
                    required
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                <v-text-field
                    v-model="mail"
                    :counter="20"
                    label="Mail"
                    
                ></v-text-field>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                <v-text-field
                    v-model="password"
                    :counter="20"
                    type="password"
                    label="Contraseña"
                    
                ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                <v-text-field
                    v-model="confirmPassword"
                    :counter="20"
                    type="password"
                    label="Confirmar contraseña"
                    
                ></v-text-field>
                </v-col>
                
                
            </v-row>
            </v-container>
        </v-form>
        
        <v-btn  color="blue lighten-1" class="mr-4" @click="registrarse">Registrarse</v-btn>
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

      rut: '',
      nombre: '',
      apellido: '',
      mail: '',
      password: '',
      confirmPassword: '',
    }
  },
  methods:{
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
    registrarse:async function(){
      if(this.rut=='' || this.nombre=='' || this.apellido=='' || this.mail=='' || this.password=='' || this.confirmPassword==''){
        alert('Debe ingresar todos los campos.')
        return 0
      }
      if(this.validaRut(this.rut)==false){
        alert("Ingrese el rut de manera correcta.")
        return 0
      }
      if(this.comprobarMail()==false){
        alert("Ingrese el correo de manera correcta.")
        return 0
      }
      if(this.password != this.confirmPassword){
        alert("Las contraseñas deben ser iguales.")
        return 0
      }
      try{
      let response = await axios.post('http://'+process.env.IP_FRONT+':5000/registrar',{correo:this.mail,contrasena:this.password,nombre:this.nombre,apellido:this.apellido,rut:this.rut});
      console.log('response', response.data);
      alert("Usuario creado con exito.")
      this.mail=''
      this.password=''
      this.confirmPassword=''
      this.nombre=''
      this.rut=''
      }
      catch(error){
        console.log(error)
        alert("Ocurrio un error.")
      }
      
    },
    comprobarMail(){
      let separacion1=this.mail.split('@')
      if (separacion1.length==2){
        let separacion2=separacion1[1].split('.')
        if(separacion2.length==2){
          return true
        }
        else{
          return false
        }
      }
      else{
        return false
      }
    },
    permisos:async function(){
      let data=localStorage.getItem("user")
      data=JSON.parse(data)      
      if(data!=null){
        try{
          let response = await axios.get('http://'+process.env.IP_FRONT+':5000/cuenta/permisos?token='+data.token);
          return (response.data.nivel_acceso ==0)
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
    if(await this.permisos==false){
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