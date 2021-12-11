<template>
<v-container class="test">
<div class="flex w-full h-screen items-center justify-center text-center" id="app">
<h1>Ingresar Excel con participantes</h1>
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
    export default {
        data: function() {
            return {
                filelist: [] 
            }
        },
        methods: {
            onChange: function() {
            this.filelist = [...this.$refs.file.files];
            },
            remove: function(i) {
            this.filelist.splice(i, 1);
            },
            ingresar: function(i){
                console.log(i) //Función temporal
                console.log(this.filelist)
                console.log(this.filelist[i])
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

