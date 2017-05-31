import cmd

import TP3objetos
#-----------------------------------------------------------------------

REPRODUCTOR = TP3objetos.Reproductor()

#-----------------------------------------------------------------------

class Shell(cmd.Cmd): #definir nombres cursor, etc,...?

	intro = "Bienvenido a 'Sounds of Cyber City'\n Ingrese help o ? para listar los comandos.\n"
	prompt = "->> "

	def do_LOAD(self, parametro): 
		"""Carga la cancion desde el archivo. 
		Reemplaza la cancion en edicion actual si es que la hay."""
		REPRODUCTOR.load(parametro)

	def do_STORE (self, parametro):
		"""Guarda la cancion."""
		REPRODUCTOR.store(parametroa)

	def do_STEP (self, parametro):
		"""Avanza a la siguiente marca de tiempo."""
		REPRODUCTOR.step()

	def do_BACK(self, parametro):
		"""Retrocede a la anterior marca de tiempo."""
		REPRODUCTOR.back()
		
	def do_STEPM (self, parametro):
		"""Avanza N marcas de tiempo hacia adelante."""
		if not parametro.isdigit():
			print("Comando invalido")
			return
		CURSOR.step(int(parametro))
		
	def do_BACKM(self, parametro):
		"""Retrocede N marcas de tiempo hacia atras."""
		if parametro.isdigit():
			print("Comando Invalido")
			return
		CURSOR.back(int(parametro))

	def do_TRACKADD(self, parametro):
		"""Agrega un track con el sonido indicado."""
		[funcion, frecuencia, volumen] = parametro.split(",")
		if frecuencia.isdigit() and volumen: #validar float volumen
			REPRODUCTOR.track_add(funcion, int(frecuencia), float(volumen))

	def do_TRACKDEL(self, parametro):
		"""Elimina un track por numero."""
		if parametro.isdigit():
			numero = int(parametro) - 1 
			REPRODUCTOR.track_del(numero)

	def do_MARKADD(self, parametro):
		"""Agrega una marca de tiempo de la duracion establecida."""
		if parametro: #validar float
			CURSOR.mark_add(float(parametro))

	def do_MARKADDNEXT(self, parametro):
		"""Agrega una marca de tiempo de la duracion establecida
		luego de la marca en la cual esta
		actualmente el cursor"""
		if parametro:#float
			CURSOR.mark_add_next(float(parametro))

	def do_MARKADDPREV(self, parametro):
		"""Agrega una marca de tiempo de la duracion establecida
		antes de la marca en la cual esta
		actualmente el cursor"""
		if parametro:#float
			CURSOR.mark_add_prev(float(parametro))

	def do_TRACKON(self, parametro):
		"""Habilita al track durante la marca de tiempo
		en la cual esta parada el cursor."""
		if parametro.isdigit():
			CURSOR.activar_track(int(parametro))

	def do_TRACKOFF(self, parametro):
		"""Desabilita al track durante la marca de tiempo
		 en la cual esta parada el cursor."""
		if parametro.isdigit():
			CURSOR.desactivar_track(int(parametro))

	def do_PLAY(self, parametro):
		"""Reproduce la marca en la que se encuentra el cursor actualmente."""
		REPRODUCTOR.reproducir_marca()

	def do_PLAYALL(self, parametro):
		"""Reproduce la cancion completa desde el inicio."""
		REPRODUCTOR.reproducir_completa()

	def do_PLAYMARKS(self, parametro):
		"""Reproduce las proximas marcas dadas por parametro desde donde se
		encuentra el cursor actualmente."""
		if not parametro.isdigit():
			print("Comando Invalido")
			return
		REPRODUCTOR.reproducir_marcas(int(parametro))

	def do_PLAYSECONDS(self, parametro):
		"""Reproduce los proximos segundos dados desde donde esta el cursor."""
		if not parametro.isdigit():
			print("Comando invalido")
			return
		CURSOR.reproducir_segundos(float(parametro))

Shell().cmdloop()




