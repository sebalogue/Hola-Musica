import cmd

import TP3objetos
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------

class Shell(cmd.Cmd): #definir nombres cursor, etc,...?
	
	intro = "Bienvenido a 'Sounds of Cyber City'\n Ingrese help o ? para listar los comandos.\n"
	prompt = "->> "
	
	funciones_sonido = ["noise","silence","sine","square","triangular"]
	reproductor = TP3objetos.Reproductor()
	canales = reproductor.dar_canales()
	cancion = reproductor.dar_cancion()
	posicion = 0

	def do_LOAD(self, parametro): 
		"""Carga la cancion desde el archivo. 
		Reemplaza la cancion en edicion actual si es que la hay."""
		try:
			self.reproductor.load(parametro)
		except IOError:
			print("Comando Invalido")

	def do_STORE (self, parametro):
		"""Guarda la cancion."""
		nombre_archivo = str(parametro)
		self.reproductor.store(parametro)

	def do_STEP (self, parametro):
		"""Avanza a la siguiente marca de tiempo."""
		if not (self.posicion < len(self.cancion) - 1):
			print("Comando invalido")
			return
		self.reproductor.step()
		self.posicion += 1

	def do_BACK(self, parametro):
		"""Retrocede a la anterior marca de tiempo."""
		if self.posicion == 0:
			print("Comando invalido")
			return
		self.reproductor.back()
		self.posicion -= 1
		
	def do_STEPM (self, parametro):
		"""Avanza N marcas de tiempo hacia adelante."""
		if not parametro.isdigit():
			print("Comando invalido")
			return
		if not (self.posicion + int(parametro) <= len(self.cancion) - 1):
			print("Comando invalido")
			return
		self.reproductor.step(int(parametro))
		self.posicion += int(parametro)
		
	def do_BACKM(self, parametro):
		"""Retrocede N marcas de tiempo hacia atras."""
		if not parametro.isdigit():
			print("Comando Invalido")
			return
		if not (self.posicion - int(parametro) >= 0):
			print("Comando invalido")
			return
		self.reproductor.back(int(parametro))
		self.posicion -= int(parametro)

	def do_TRACKADD(self, parametro):
		"""Agrega un track con el sonido indicado."""
		[funcion, frecuencia, volumen] = parametro.split(",")
		try:
			frecuencia = float(frecuencia)
			volumen = float(volumen)
		except ValueError:
			print("Comando invalido")
			return
		if not funcion.lower() in self.funciones_sonido:
			print("Comando invalido")
			return
		self.reproductor.track_add(funcion.lower(), float(frecuencia), float(volumen))
		self.canales += 1

	def do_TRACKDEL(self, parametro):
		"""Elimina un track por numero."""
		if not parametro.isdigit():
			print("Comando invalido")
		numero = int(parametro) - 1 
		if not (numero >= 0) or not (parametro <= self.canales - 1):
			print("Comando invalido")
			return
		self.reproductor.track_del(numero)
		self.canales -= 1

	def do_MARKADD(self, parametro):
		"""Agrega una marca de tiempo de la duracion establecida."""
		try:
			tiempo = float(parametro)
		except ValueError:
			print("Comando Invalido")
			return
		self.reproductor.mark_add(tiempo)

	def do_MARKADDNEXT(self, parametro):
		"""Agrega una marca de tiempo de la duracion establecida
		luego de la marca en la cual esta
		actualmente el cursor"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		try:
			tiempo = float(parametro)
		except ValueError:
			print("Comando inavalido")
			return
		self.reproductor.mark_add_next(tiempo)

	def do_MARKADDPREV(self, parametro):
		"""Agrega una marca de tiempo de la duracion establecida
		antes de la marca en la cual esta
		actualmente el cursor"""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		try:
			tiempo = float(parametro)
		except ValueError:
			print("Comando inavalido")
			return
		self.posicion += 1
		self.reproductor.mark_add_prev(tiempo)


	def do_TRACKON(self, parametro):
		"""Habilita al track durante la marca de tiempo
		en la cual esta parada el cursor."""
		if not parametro.isdigit():
			print("Comando invalido")
			return
		numero = int(parametro) - 1
		if not (numero >= 0) or not (numero <= self.canales - 1):
			print("Comando invalido")
			return
		self.reproductor.track_on(numero) 


	def do_TRACKOFF(self, parametro):
		"""Desabilita al track durante la marca de tiempo
		 en la cual esta parada el cursor."""
		if not parametro.isdigit():
			print("Comando Invalido")
			return
		numero = int(parametro) - 1
		if not (numero >= 0) or not (numero <= self.canales - 1):
			print("Comando invalido")
			return
		self.reproductor.track_off(numero)

	def do_PLAY(self, parametro):
		"""Reproduce la marca en la que se encuentra el cursor actualmente."""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		self.reproductor.reproducir_marca()

	def do_PLAYALL(self, parametro):
		"""Reproduce la cancion completa desde el inicio."""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		self.reproductor.reproducir_completa()

	def do_PLAYMARKS(self, parametro):
		"""Reproduce las proximas marcas dadas por parametro desde donde se
		encuentra el cursor actualmente."""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		if not parametro.isdigit():
			print("Comando Invalido")
			return
		if not (self.posicion + int(parametro) - 1 <= len(self.cancion) -1):
			print("Comando invalido")
			return
		self.reproductor.reproducir_marcas(int(parametro))

	def do_PLAYSECONDS(self, parametro):
		"""Reproduce los proximos segundos dados desde donde esta el cursor."""
		if len(self.cancion) == 0:
			print("Comando invalido")
			return
		try:
			float(parametro)
		except ValueError:
			print("Comando invalido")
			return
		self.reproductor.reproducir_segundos(float(parametro))

Shell().cmdloop()




