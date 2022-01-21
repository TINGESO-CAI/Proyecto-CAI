<template>
  <v-container class="test">
    <v-col class="text-center">
      <h1>Bienvenidos al Sistema de gestión administrativa para la capacitación CAI </h1>
          <img
              src="/logoCai.png"
              class="mb-5"
          >
        
          </v-col>
  </v-container>
</template>
<script>
if(localStorage.getItem("user")== null){
  localStorage.setItem("user",JSON.stringify({token:null}))
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