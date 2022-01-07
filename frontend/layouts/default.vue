<template >
  <v-app dark>
    <v-navigation-drawer color="secondary"
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
      fluid
      max-width="50"
    >
     <!--
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
      -->
      <!--
        Seccion de sub menu
        -->

      <v-list-group
            router
            exact
            sub-group
          >
      <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Participantes</v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item
          v-for="([title, icon,to], i) in participantes"
          :key="i"
          :to="to"
          link
        >
           <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="title"></v-list-item-title>

         
        </v-list-item>
        
      </v-list-group>
      <v-list-group
            router
            exact
            sub-group
          >
      <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Relatores</v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item
          v-for="([title, icon,to], i) in relatores"
          :key="i"
          :to="to"
          link
        >
           <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="title"></v-list-item-title>

         
        </v-list-item>
        
      </v-list-group>
      
      <v-list-group
            router
            exact
            sub-group
          >
      <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Cursos</v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item
          v-for="([title, icon,to], i) in cursos"
          :key="i"
          :to="to"
          link
        >
           <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="title"></v-list-item-title>

         
        </v-list-item>
        
      </v-list-group>

      <v-list-group
            router
            exact
            sub-group
          >
      <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Empresas</v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item
          v-for="([title, icon,to], i) in empresas"
          :key="i"
          :to="to"
          link
        >
           <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="title"></v-list-item-title>

         
        </v-list-item>
        
      </v-list-group>

      <v-list-group
            router
            exact
            sub-group
          >
      <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Finanzas</v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item
          v-for="([title, icon,to], i) in finanzas"
          :key="i"
          :to="to"
          link
        >
           <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="title"></v-list-item-title>

         
        </v-list-item>
        
      </v-list-group>
      <v-list-group
            router
            exact
            sub-group
          >
      <template v-slot:activator>
          <v-list-item-content>
            <v-list-item-title>Administracion</v-list-item-title>
          </v-list-item-content>
        </template>

        <v-list-item
          v-for="([title, icon,to], i) in administracion"
          :key="i"
          :to="to"
          link
        >
           <v-list-item-icon>
            <v-icon v-text="icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-title v-text="title"></v-list-item-title>

         
        </v-list-item>
        
      </v-list-group>
    </v-navigation-drawer>
    <v-app-bar color="primary"
      :clipped-left="clipped"

      fixed
      height="40"
      app
      scroll-off-screen="true"
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn
        icon
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="clipped = !clipped"
      >
        <v-icon>mdi-application</v-icon>
      </v-btn>
      <v-btn
        icon
        @click.stop="fixed = !fixed"
      >
        <v-icon>mdi-minus</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-switch
      
      color="secondary"
        height="0"
        v-model="$vuetify.theme.dark"
        prepend-icon='mdi-brightness-4'
      ></v-switch>

      <v-btn
        icon
        @click.stop="rightDrawer = !rightDrawer"
      >
        <v-icon>mdi-account</v-icon>
      </v-btn>
      
    </v-app-bar>
    <v-main>
      <v-container>
        <Nuxt />
      </v-container>
    </v-main>
    <!--login-->
    <v-navigation-drawer
      v-model="rightDrawer"
      :right="right"
      temporary
      fixed
    >
      <v-card >
        <v-toolbar dark color="primary">
          <v-toolbar-title >INGRESO</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-form>
              <v-text-field
                v-model="correo"
                prepend-icon='mdi-email'
                name="login"
                label="Correo"
                type="text"
              ></v-text-field>
              <v-text-field
                v-model="contrasena"
                id="password"
                prepend-icon="mdi-lock"
                name="password"
                label="Contraseña"
                type="password"
              ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="ingresar">INGRESAR</v-btn>
        </v-card-actions>
    </v-card>
    </v-navigation-drawer>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios'
export default {
  name: 'default',
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      message: '',

      correo: '',
      contraseña: '',

      usuario:'',
      rol:'',
      //lista para submenu
      participantes: [
      ['Nuevo participante', 'mdi-account-multiple-plus','/nuevo_participante'],
      ['Ver participantes','mdi-account-multiple','/ver_participantes'],
      ['Subir archivo', 'mdi-file-plus','/subir_archivo'],
      ['Filtrar participantes','mdi-account-multiple','/filtrar_participantes' ]
      ],
      relatores: [
      ['Nuevo relator', 'mdi-account-multiple-plus','/nuevo_relator'],
      ['Ver relatores','mdi-format-list-bulleted-type','/ver_relatores'],
      ['Subir archivo', 'mdi-file-plus','/subir_archivo_relator']
      ],
      cursos:[
      ['Crear curso', 'mdi-account-multiple-plus','/crear_curso'],
      ['Ver cursos','mdi-format-list-bulleted-type','/ver_cursos'],
      ['Subir archivo', 'mdi-file-plus','/subir_archivo_curso'],
      ['Ver Instancias','mdi-format-list-bulleted-type','/ver_instancias'],
      ['Asignar Instancia','mdi-loupe','/Instancia_curso'],
      ['Asignar relatores','mdi-account-multiple','/asignar_relator_instancia'],
      ['Asignar participantes','mdi-account-multiple','/matricular_participantes']
      ],
      empresas:[
      ['Nueva empresa', 'mdi-account-multiple-plus','/nueva_empresa'],
      ['Ver empresas','mdi-format-list-bulleted-type','/ver_empresas']
      ],
      finanzas:[
      ['Generar Factura','mdi-file-plus','/factura'],
      ['Ver facturas','mdi-format-list-bulleted-type','/ver_facturas'],
      ['Filtrar facturas','mdi-book-open-page-variant','/filtrar_facturas'],
      ['Ver participantes','mdi-account-multiple','/ver_participantes_factura'],
      
      ],
      administracion:[
      ['Asignar permisos', 'mdi-account-multiple-plus','/permisos'],
      ['Editar datos','mdi-account-multiple','/editar datos']
      ],
      items: [
        {
          icon: 'mdi-apps',
          title: 'Principal',
          to: '/'
        },        
        {
          icon: 'mdi-account-multiple-plus',
          title: 'Nuevo participante',
          to: '/nuevo_participante'
        },
        {
          icon: 'mdi-file-plus',
          title: 'Subir archivo',
          to: '/subir_archivo'
        },
        {
          icon: 'mdi-plus',
          title: 'Cursos',
          to: '/cursos'
        },
        {
          icon: 'mdi-content-paste',
          title: 'inscribir participantes a cursos',
          to:'/matricular_participantes'
        },
        {
          icon: 'mdi-plus',
          title: 'Finanzas',
          to: '/finanzas'
        },
        {
          icon: 'mdi-plus',
          title: 'Administracion',
          to: '/administracion'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Sistema de gestión administrativa para la capacitación CAI'
    }
  },
  methods:{
    successMessage:function(){
      alert("Ingreso exitoso(REVISAR)")
    },
    async ingresar(){
      this.message = '';
      let credenciales={
        correo: this.correo,
        contrasena: this.contrasena
      }
      try {
        let response = await axios.post('http://localhost:5000/entrar',credenciales);
        //limpiar
        this.correo = '';
        this.contrasena = '';
        this.successMessage();
        console.log('response', response.data);
      }
      catch (error){
        console.log('error', error); 
        this.message = 'Ocurrió un error'
      }
    }
  }
}
</script>
