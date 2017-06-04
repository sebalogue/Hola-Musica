import cmd

import reproductor
#-----------------------------------------------------------------------
puede_ser_flotante = reproductor.se_puede_convertir_a_flotante
Reproductor = reproductor.Reproductor
#-----------------------------------------------------------------------

class Shell(cmd.Cmd): 
	
	intro = "Bienvenido a 'Sounds of Cyber City'\n Ingrese help o ? para listar los comandos.\n"
	prompt = "->> "
	
	funciones_sonido = ["noise","silence","sine","square","triangular"]
	reproductor = Reproductor()
	canales = reproductor.dar_canales()
	cancion = reproductor.dar_cancion()
	posicion = 0

	def do_NEW(self, parametro):
		"""
		Inicia una nueva cancion vacia. 
		Se recomienda guardar la cancion actual, 
		ya que la misma se borrara caso contrario.
		"""
		self.reproductor.reiniciar()

		self.canales = self.reproductor.dar_canales()
		self.cancion = self.reproductor.dar_cancion()
		self.posicion = 0

	def do_LOAD(self, cancion): 
		"""
		Pre: recibe un archivo de formato plp.
		Post: Carga la cancion desde el archivo. 
		Reemplaza la cancion en edicion actual si es que la hay.
		Se recomienda guardar antes utilizar esta funcion.
		
		El programa garantiza que todo archivo generado por
		el mismo, sin mdificacion externa, podra ser cargado
		con normalidad.
		Atencion! El programa tambien puede recibir archivos 
		con formato plp no genrados por el mismo, pero es 
		muy sensible a los espacios y al tipo de letra, por 
		lo que no siempre podra cargar estos otros archivos.
		"""
		try:
			self.reproductor.cargar(cancion)
		except IOError:
			print("Comando Invalido")
			return
		except ValueError:
			print("Comandos invalido: Error en la lectura del archivo.")
		self.canales = self.reproductor.dar_canales()
		self.cancion = self.reproductor.dar_cancion()
		self.posicion = 0

	def do_STORE (self, nombre_archivo):
		"""
		Pre: recibe el nombre con que se desea guardar la cancion.
		Post: Guarda la cancion con formato plp. 
		Atencion! Si el archivo ya existe lo sobre escribira.
		"""
		self.reproductor.guardar(nombre_archivo)

	def do_STEP (self, parametro):
		"""
		Avanza a la siguiente marca de tiempo, 
		si solo si existe.
		"""
		if not (self.posicion < len(self.cancion) - 1):
			print("Comando invalido")
			return
		self.reproductor.avanzar()
		self.posicion += 1

	def do_BACK(self, parametro):
		"""
		Retrocede a la anterior marca de tiempo,
		si solo si existe.
		"""
		if self.posicion == 0:
			print("Comando invalido")
			return
		self.reproductor.retroceder()
		self.posicion -= 1
		
	def do_STEPM (self, pasos):
		"""
		Pre: recibe la cantidad de pasos (entero) a realizar.
		Post: avanza N marcas de tiempo hacia adelante.
		Si no hay tanta marcas, se queda es un posicion original.
		"""
		if not pasos.isdigit():
			print("Comando invalido")
			return
		if not (self.posicion + int(pasos) <= len(self.cancion) - 1):
			print("Comando invalido")
			return
		self.reproductor.avanzar(int(pasos))
		self.posicion += int(pasos)
		
	def do_BACKM(self, pasos):
		"""
		Pre: recibe la cantidad de pasos (entero) a realizar.
		Retrocede N marcas de tiempo hacia atras.
		Si no hay tanta marcas, se queda es un posicion original.
		"""
		if not pasos.isdigit():
			print("Comando Invalido")
			return
		if (not (self.posicion - int(pasos) >= 0)):
			print("Comando invalido")
			return
		self.reproductor.retroceder(int(pasos))
		self.posicion -= int(pasos)

	def do_TRACKADD(self, funcion_frecuencia_volumen):
		"""
		Pre: recibe una cadena de la forma tal: funcion,frecuencia,volumen.
		Donde frecuencia y volumen son numeros (enteros o decimales), y 
		donde funcion es una de las siguiente funciones de sondido:
		"noise","silence","sine","square","triangular".
		Post: Agrega un track con el sonido indicado.
		"""
		comas = 0
		for caracter in funcion_frecuencia_volumen:
			if caracter == ",":
				comas += 1
		if comas != 2:
			print("Comando invalido")
			return			
		funcion, frecuencia, volumen = funcion_frecuencia_volumen.split(",")
		if (not puede_ser_flotante(frecuencia)) or (not puede_ser_flotante(volumen)):
			print("Comando invalido")
			return
		frecuencia = float(frecuencia)
		volumen = float(volumen)
		if not funcion.lower() in self.funciones_sonido:
			print("Comando invalido")
			return
		self.reproductor.track_agregar(funcion.lower(), float(frecuencia), float(volumen))
		self.canales += 1

	def do_TRACKDEL(self, indice):
		"""
		Pre: recibe el indice de un track existente.
		Post: Elimina el track del indice recibido.
		"""
		if not indice.isdigit():
			print("Comando invalido")
			return
		numero = int(indice) - 1 
		if not (numero >= 0) or not (numero <= self.canales - 1):
			print("Comando invalido")
			return
		self.reproductor.track_eliminar(numero)
		self.canales -= 1

	def do_MARKADD(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal).
		Post: agrega una marca de tiempo de la duracion establecida.
		"""
		if not puede_ser_flotante(tiempo):
			print("Comando Invalido")
			return
		tiempo = float(tiempo)
		self.reproductor.marca_agregar(tiempo)

	def do_MARKADDNEXT(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal).
		Post: agrega una marca de tiempo de la duracion establecida 
		luego de la marca en la cual esta actualmente el cursor.
		"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		if not puede_ser_flotante(tiempo):
			print("Comando Invalido")
			return
		tiempo = float(tiempo)
		self.reproductor.marca_agregar_siguiente(tiempo)

	def do_MARKADDPREV(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal).
		Post: agrega una marca de tiempo de la duracion establecida 
		antes de la marca en la cual esta actualmente el cursor.
		"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		if not puede_ser_flotante(tiempo):
			print("Comando Invalido")
			return
		tiempo = float(tiempo)
		self.posicion += 1
		self.reproductor.marca_agregar_previo(tiempo)


	def do_TRACKON(self, indice):
		"""
		Pre: recibe un indice de track existente (entero).
		Post: Habilita al track en la marca de tiempo
		en la cual esta parada el cursor.
		"""
		if not indice.isdigit():
			print("Comando invalido")
			return
		numero = int(indice) - 1
		if not (numero >= 0) or not (numero <= self.canales - 1):
			print("Comando invalido")
			return
		self.reproductor.track_activar(numero) 


	def do_TRACKOFF(self, indice):
		"""
		Pre: recibe un indice de track existente (entero).
		Post: deshabilita al track en la marca de tiempo
		en la cual esta parada el cursor.
		"""
		if not indice.isdigit():
			print("Comando Invalido")
			return
		numero = int(indice) - 1
		if not (numero >= 0) or not (numero <= self.canales - 1):
			print("Comando invalido")
			return
		self.reproductor.track_desactivar(numero)

	def do_PLAY(self, parametro):
		"""
		Reproduce la marca en la que se encuentra el cursor actualmente.
		"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		self.reproductor.reproducir_marca()

	def do_PLAYALL(self, parametro):
		"""
		Reproduce la cancion completa desde el inicio.
		"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		self.reproductor.reproducir_completa()

	def do_PLAYMARKS(self, marcas):
		"""
		Pre: recibe un cantidad marcas (entero).
		Post: reproduce las proximas marcas dadas por parametro desde donde se
		encuentra el cursor actualmente.
		Atencion! Si se dan mas marcas de las que hay a continuacion, no se 
		reproduce ninguna.
		"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		if not marcas.isdigit() or (int(marcas)) <= 0:
			print("Comando Invalido")
			return
		if not (self.posicion + int(marcas) - 1 <= len(self.cancion) -1):
			print("Comando invalido")
			return
		self.reproductor.reproducir_marcas(int(marcas))

	def do_PLAYSECONDS(self, segundos):
		"""
		Pre: recibe una cantidad de sugundos (entero o decimal).
		Post: reproduce los proximos segundos dados desde donde esta el cursor.
		"""
		if len(self.cancion) == 0:
			print("Comando Invalido")
			return
		if not puede_ser_flotante(segundos):
			print("Comando Invalido")
			return
		tiempo = float(segundos)
		if tiempo <= 0:
			print("Comandos Invalido")
			return
		self.reproductor.reproducir_segundos(tiempo)

Shell().cmdloop()




