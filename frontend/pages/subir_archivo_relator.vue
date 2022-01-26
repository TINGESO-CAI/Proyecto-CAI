<template>
<v-container class="test">
<div class="flex w-full h-screen items-center justify-center text-center" id="app">
<h1>Ingresar Excel con relatores</h1>
  <div class="p-12 bg-gray-100 border border-gray-300" @dragover="dragover" @dragleave="dragleave" @drop="drop">
    <input type="file" multiple name="fields[assetsFieldHandle][]" 
      class="w-px h-px opacity-0 overflow-hidden absolute" @change="onChange" ref="file" accept=".xlsx" />
  
    <label for="assetsFieldHandle" class="block cursor-pointer">
      
        <v-col class="text-center">
         <blockquote class="blockquote">
            Arrastre el excel con los usuarios aqui.
        </blockquote>
        <img
            src="/logoCai.png"
            class="mb-5"
        >
       
        </v-col>
    </label>
    <ul class="mt-4" v-if="this.filelist.length" v-cloak>
      <li class="text-sm p-1" v-for="file in filelist">
        {{file.name }} <button class="ml-2" type="button" @click="ingresar(filelist.indexOf(file))" title="Ingresar datos">Ingresar</button>
        <button class="ml-2" type="button" @click="remove(filelist.indexOf(file))" title="Eliminar datos">Eliminar</button> 
        
      </li>
    </ul>
  </div>
</div>
</v-container>
</template>


<script>
    import readXlsxFile from 'read-excel-file'
    import axios from 'axios'
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
        data: function() {
            return {
                filelist: [] 
            }
        },
        methods: {
            onChange: function(e) {
            this.filelist = [...this.$refs.file.files];
            },
            remove: function(i) {
            this.filelist.splice(i, 1);
            },
            todate: function(fecha){
              if (fecha != null){
                var date = new Date(Math.round((fecha - (25567 + 1)) * 86400 * 1000));
                var converted_date = date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString()
                //var converted_date = date.toISOString().split('T')[0];
              }
              return converted_date
            },            
            cambiarGenero(valor){
              if (valor == 'f' ) return 1
              else if (valor == 'm' ) return 2
              else return null
            },

            comprobarTelefono(fono){
              if (fono==null){
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
            ingresar: async function(i){
              let errores=[]
              let archivo=await readXlsxFile(this.filelist[i])
                for (let j=1; j< archivo.length; j++){  
                  try{
              //let response=await axios.post('http://52.188.153.77:5000/participante/agregar',
                  let NewRelator={
                   rut:archivo[j][0]
                  ,nombre:archivo[j][1]
                  ,apellido_paterno:archivo[j][2]
                  ,apellido_materno:archivo[j][3]
                  ,titulo:archivo[j][4]
                  ,cv:archivo[j][6]
                  ,fecha_nacimiento: this.todate(archivo[j][7])
                  ,numero_cuenta:archivo[j][8].toString()
                  ,banco: archivo[j][9]
                  ,tipo_cuenta: archivo[j][10]
                  ,fono_personal: archivo[j][11]
                  ,fono_corporativo: archivo[j][12]
                  ,correo_personal: archivo[j][13]
                  ,correo_corporativo: archivo[j][14]
                  ,genero: this.cambiarGenero(archivo[j][5])}//)
                  if(this.validaRut(archivo[j][0]) && this.comprobarTelefono(archivo[j][11]) && this.comprobarTelefono(archivo[j][12]) ){
                    await axios.post('http://52.188.153.77:5000/relator/agregar',NewRelator)
                    
                    }
                  else{
                      console.log(archivo[j][11],archivo[j][12])
                      errores.push(j)
                    }                 
                  }
                  catch(error){
                    errores.push(j)
                  }                  
                }
                let mensaje="Se ha ingresado archivo "+this.filelist[i].name+" con exito."
                if (errores.length!=0){
                  mensaje=mensaje +'\n errores en los relatores de las lineas:\n'
                  for (let indice in errores){
                    mensaje=mensaje + (errores[indice]+1).toString()+'\n'
                  }
                }
                this.remove(i)
                alert(mensaje)
            },
            dragover: function(event) {
            event.preventDefault();
            if (!event.currentTarget.classList.contains('bg-green-300')) {
                event.currentTarget.classList.remove('bg-gray-100');
                event.currentTarget.classList.add('bg-green-300');
            }
            },
            dragleave: function(event) {
            event.currentTarget.classList.add('bg-gray-100');
            event.currentTarget.classList.remove('bg-green-300');
            },
            drop: function(event) {
            event.preventDefault();
            this.$refs.file.files = event.dataTransfer.files;
            this.onChange(); 
            event.currentTarget.classList.add('bg-gray-100');
            event.currentTarget.classList.remove('bg-green-300');
            },
            permisos:async function(){
            let data=localStorage.getItem("user")
            data=JSON.parse(data)      
            if(data!=null){
              try{
                let response = await axios.get('http://52.188.153.77:5000/cuenta/permisos?token='+data.token);
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
            
        },
        created: async function(){
          if(await this.permisos()==false){
            window.location.href='/'
          }
        }
        
    }
</script>
<style>
    .v-cloak {
  display: none;
}

.test{
  border-top: 3px solid;
  border-bottom: 3px solid;
  border-color: #4e99fc
}
</style>

