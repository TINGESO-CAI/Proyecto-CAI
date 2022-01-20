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
						<v-list-item-title>PARTICIPANTES</v-list-item-title>
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
						<v-list-item-title>RELATORES</v-list-item-title>
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
						<v-list-item-title>CURSOS</v-list-item-title>
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
						<v-list-item-title>EMPRESAS</v-list-item-title>
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
						v-if="permisos()"
					>
			<template v-slot:activator>
					<v-list-item-content>
						<v-list-item-title>FINANZAS</v-list-item-title>
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
						v-if="permisos()"
					>
			<template v-slot:activator>
					<v-list-item-content>
						<v-list-item-title>ADMINISTRACION</v-list-item-title>
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
			fluid
			color="secondary"
				v-model="$vuetify.theme.dark"
				prepend-icon='mdi-brightness-4'
			></v-switch>
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
		<!--login-->
		<v-navigation-drawer
			v-model="rightDrawer"
			:right="right"
			temporary
			fixed
		>
			<v-card v-if="login==0">
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

		<!--usuario logeado-->
    <v-card v-if="login==1">
        <v-toolbar dark color="primary">
          <v-toolbar-title >DATOS USUARIO</v-toolbar-title>
        </v-toolbar>
        <v-card-text>
              <span>Nombre: {{usuario.nombre}}</span><br>
              <span>Rut: {{usuario.rut}}</span><br>
              <span>Correo: {{usuario.correo}}</span><br>

        </v-card-text>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn color="primary" @click="salir">SALIR</v-btn>
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
			login:0,
			//datos usuario
			nombre:'',
			rut:'',
			correo:'',
			nivel_acceso:'',
			usuario:{
				nombre:'',
				rut:'',
				correo:'',
			},
			//lista para submenu
			participantes: [
			['Nuevo participante', 'mdi-account-multiple-plus','/nuevo_participante'],
			['Ver participantes','mdi-account-multiple','/ver_participantes'],
			['Subir archivo', 'mdi-file-plus','/subir_archivo'],
			['Filtrar participantes','mdi-account-filter-outline','/filtrar_participantes' ]
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
			['Nuevo Contacto', 'mdi-cellphone-basic', '/nuevo_contacto'],
			['Ver empresas','mdi-format-list-bulleted-type','/ver_empresas']
			],
			finanzas:[
			['Generar S. Factura','mdi-file-plus','/factura'],
			['Ver S. facturas','mdi-format-list-bulleted-type','/ver_facturas'],
			['Filtrar S. facturas','mdi-book-open-page-variant','/filtrar_facturas'],
			['Ver participantes','mdi-account-multiple','/ver_participantes_factura'],
			
			],
			administracion:[
			['Registrarse', 'mdi-account-multiple-plus','/nuevo_usuario'],
			/*
			['Asignar permisos', 'mdi-account-multiple-plus','/permisos'],
			['Editar datos','mdi-account-multiple','/editar datos']*/
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
			title: 'Sistema de gestión para CAI'
		}
	},
	methods:{
		/*
		successMessage:function(){
			alert("Ingreso exitoso(REVISAR)")
		},
		*/
		async ingresar(){
			//localStorage.setItem("user",JSON.stringify({mail:"jose@gmail.com", password:"password", permiso:3}))
			//this.login=1
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
				localStorage.setItem("user",JSON.stringify({token:response.data.token,nombre:response.data.nombre,correo:response.data.correo,rut:response.data.rut}))
				this.usuario.nombre=response.data.nombre
				this.usuario.rut=response.data.rut
				this.usuario.correo=response.data.correo
				this.login=1;
				this.cambiarMenuPermisos()
				//this.traerDatos();
			}
			catch (error){
				console.log('error', error); 
				alert('Credenciales no validas')
			}
		},
		async traerDatos(){
			this.message = '';
			try {
				let response = await axios.get('http://localhost:5000/cuenta/permisos');
				//limpiar
				this.usuario=response.data;
			}
			catch (error){
				console.log('error', error); 
				this.message = 'Ocurrió un error'
			}
		},
		async salir(){
			localStorage.removeItem("user")
			this.login=0
			this.usuario = {
				nombre:'',
				rut:'',
				correo:'',
			},
			this.contrasena = '';
			this.cambiarMenuSinPermisos()
			window.location.href='/'
			/*
			this.message = '';
			try {
				let response = await axios.post('http://localhost:5000/salir');
				//limpiar
				this.usuario = {};
				this.contrasena = '';
				this.successMessage();
				console.log('response', response.data);
				this.login=0;
			}
			catch (error){
				console.log('error', error); 
				this.message = 'Ocurrió un error'
			}
			*/
		},
		permisos(){
			let data=localStorage.getItem("user")
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
    	},
		cambiarMenuPermisos(){
			this.participantes= [
			['Nuevo participante', 'mdi-account-multiple-plus','/nuevo_participante'],
			['Ver participantes','mdi-account-multiple','/ver_participantes'],
			['Subir archivo', 'mdi-file-plus','/subir_archivo'],
			['Filtrar participantes','mdi-account-filter-outline','/filtrar_participantes' ]
			]
			this.relatores= [
			['Nuevo relator', 'mdi-account-multiple-plus','/nuevo_relator'],
			['Ver relatores','mdi-format-list-bulleted-type','/ver_relatores'],
			['Subir archivo', 'mdi-file-plus','/subir_archivo_relator']
			]
			this.cursos=[
			['Crear curso', 'mdi-account-multiple-plus','/crear_curso'],
			['Ver cursos','mdi-format-list-bulleted-type','/ver_cursos'],
			['Subir archivo', 'mdi-file-plus','/subir_archivo_curso'],
			['Ver Instancias','mdi-format-list-bulleted-type','/ver_instancias'],
			['Asignar Instancia','mdi-loupe','/Instancia_curso'],
			['Asignar relatores','mdi-account-multiple','/asignar_relator_instancia'],
			['Asignar participantes','mdi-account-multiple','/matricular_participantes']
			]
			this.empresas=[
			['Nueva empresa', 'mdi-account-multiple-plus','/nueva_empresa'],
			['Nuevo Contacto', 'mdi-cellphone-basic', '/nuevo_contacto'],
			['Ver empresas','mdi-format-list-bulleted-type','/ver_empresas']
			]
			this.finanzas=[
			['Generar S. Factura','mdi-file-plus','/factura'],
			['Ver S. facturas','mdi-format-list-bulleted-type','/ver_facturas'],
			['Filtrar S. facturas','mdi-book-open-page-variant','/filtrar_facturas'],
			['Ver participantes','mdi-account-multiple','/ver_participantes_factura'],
			
			]
			this.administracion=[
			['Registrarse', 'mdi-account-multiple-plus','/nuevo_usuario'],]
		},
		cambiarMenuSinPermisos(){
			this.participantes= [
			['Ver participantes','mdi-account-multiple','/ver_participantes'],
			['Filtrar participantes','mdi-account-filter-outline','/filtrar_participantes' ]
			]
			this.relatores= [
			['Ver relatores','mdi-format-list-bulleted-type','/ver_relatores'],
			]
			this.cursos=[
			['Ver cursos','mdi-format-list-bulleted-type','/ver_cursos'],
			['Ver Instancias','mdi-format-list-bulleted-type','/ver_instancias'],
			]
			this.empresas=[
			['Ver empresas','mdi-format-list-bulleted-type','/ver_empresas']
			]
			this.administracion=[
			['Registrarse', 'mdi-account-multiple-plus','/nuevo_usuario'],]
		},
		asignarDatos(){
			let data=localStorage.getItem("user")
			data=JSON.parse(data)
			this.usuario.correo=data.correo
			this.usuario.rut=data.rut
			this.usuario.nombre=data.nombre
		}
	},
	created(){
		if(this.permisos()){		
			this.asignarDatos()
			this.login=1
			this.cambiarMenuPermisos()		
		}
		else{
			this.cambiarMenuSinPermisos()
		}
		this.traerDatos();
	}
}
</script>
