<template>
<v-container class="test">
<div class="flex w-full h-screen items-center justify-center text-center" id="app">
<h1>Ingresar Excel con Cursos</h1>
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
                var converted_date = date.getFullYear().toString()+'-'+(date.getMonth()+1).toString()+'-'+date.getDate().toString()  //date.toISOString().split('T')[0];
              }
              return converted_date
            },
            postParticipante: async function(archivo,j){
              
              
            },
            ingresar: async function(i){
              let errores=[]
              let archivo=await readXlsxFile(this.filelist[i])
                for (let j=1; j< archivo.length; j++){  
                  try{
              //let response=await axios.post('http://localhost:5000/participante/agregar',
                  let NewCurso={
                   sence:archivo[j][0].toString()
                  ,nombre:archivo[j][1]
                  ,modalidad:archivo[j][2]
                  ,categoria:archivo[j][3]
                  ,horas_curso:archivo[j][4].toString()
                  ,valor_efectivo_participante:archivo[j][5].toString()
                  ,valor_imputable_participante: archivo[j][6].toString()
                  ,resolucion_sence:archivo[j][7].toString()
                  ,resolucion_usach: archivo[j][8].toString()
                  ,f_vigencia: this.todate(archivo[j][10])}
                  let response=await axios.post('http://localhost:5000/curso/agregar',NewCurso)
                  }
                  catch(error){
                    console.log(error)
                    errores.push(j)
                  }                  
                }
                let mensaje="Se ha ingresado archivo "+this.filelist[i].name+" con exito."
                if (errores.length!=0){
                  mensaje=mensaje +'\n errores en los cursos de las lineas:\n'
                  for (let indice in errores){
                    mensaje=mensaje + (errores[indice]+1).toString()+'\n'
                  }
                }
                this.remove(i)
                console.log('errores: ',errores)
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
            window.history.back()
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

