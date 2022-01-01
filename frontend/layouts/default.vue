<template>
  <v-app dark>
    <v-navigation-drawer color="#436899"
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
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
    <v-app-bar color="#EA7600"
      :clipped-left="clipped"
      fixed
      app
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
    <v-navigation-drawer
      v-model="rightDrawer"
      :right="right"
      temporary
      fixed
    >
      <v-list>
        <v-list-item @click.native="right = !right">
          <v-list-item-action>
            <v-icon light>
              ROL
            </v-icon>
          </v-list-item-action>
          <v-list-item-title>*Datos del perfil*</v-list-item-title>
        </v-list-item>
      </v-list>
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
export default {
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
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
      ['Subir archivo', 'mdi-file-plus','/subir_archivo']
      ],
      cursos:[
      ['Crear curso', 'mdi-account-multiple-plus','/crear_curso'],
      ['Ver cursos','mdi-format-list-bulleted-type','/ver_cursos'],
      ['Subir archivo', 'mdi-file-plus','/subir_archivo_curso'],
      ['Asignar Instancia','mdi-loupe','/Instancia_curso'],
      ['Asignar relatores','mdi-account-multiple','/asignar_relator_curso'],
      ['Asignar participantes','mdi-account-multiple','/matricular_participantes']
      ],
      empresas:[
      ['Nueva empresa', 'mdi-account-multiple-plus','/nueva_empresa'],
      ['Ver empresas','mdi-format-list-bulleted-type','/ver_empresas']
      ],
      finanzas:[
      ['Generar boleta', 'mdi-account-multiple-plus','/generar_boleta'],
      ['Ver boletas','mdi-format-list-bulleted-type','/ver_boletas'],
      ['Ver facturas','mdi-account-multiple','/ver_facturas'],
      ['Asignar pagos','mdi-account-multiple','/asignar_pagos'],
      ['Generar Factura','mdi-file-plus','/factura']
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
  }
}
</script>
