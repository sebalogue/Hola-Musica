import cmd

import TP3objetos.py

class Shell(cmd.Cmd): #definir nombres cursor, etc,...?

	intro = "Bienvenido a 'Sounds of Cyber City'\n Ingrese help o ? para listar los comandos.\n"
	prompt = "->> "

	def do_LOAD(self, archivo): #falta
		"""Carga la cancion desde el archivo. 
		Reemplaza la cancion en edicion actual si es que la hay."""


	def do_STORE (self, archivo):#falta
		"""Guarda la cancion."""


	def do_STEP (self, parametro):
		"""Avanza a la siguiente marca de tiempo."""
		cursor.step()

	def do_BACK(self, parametro):
		"""Retrocede a la anterior marca de tiempo."""
		cursor.back()

	def do_STEPM (self, n):
		"""Avanza N marcas de tiempo hacia adelante."""
		cursor.step(n)

	def do_BACKM(self, n):
		"""Retrocede N marcas de tiempo hacia atras."""
		cursor.back(n)

	def do_TRACKADD(self, funcion, frecuencia, volumen):
		"""Agrega un track con el sonido indicado."""
		reproductor.track__add()

	def do_TRACKDEL(self, numero_track):
		"""Elimina un track por numero."""
		reproductor.track_del(numero_track)

	def do_MARKADD(self, duracion):
		"""Agrega una marca de tiempo de la duracion establecida."""
		cursor.mark_add(duracion)

	def do_MARKADDNEXT(self, duracion):
		"""Agrega una marca de tiempo de la duracion establecida
		luego de la marca en la cual esta
		actualmente el cursor"""
		cursor.mark_add_next(duracion)

	def do_MARKADDPREV(self, duracion):
		"""Agrega una marca de tiempo de la duracion establecida
		antes de la marca en la cual esta
		actualmente el cursor"""
		cursor.mark_add_prev(duracion)

	def do_TRACKON(self, numero_track):
		"""Habilita al track durante la marca de tiempo
		 en la cual esta parada el cursor."""
		 cursor.activar_track(numero_track)

	def do_TRACKOFF(self, numero_track):
		"""Desabilita al track durante la marca de tiempo
		 en la cual esta parada el cursor."""
		 cursor.desactivar_track(numero_track)

	def do_PLAY(self, parametro):
		"""Reproduce la marca en la que se encuentra el cursor actualmente."""
		cursor.reproducir_marca()

	def do_PLAYALL(self, parametro):
		"""Reproduce la canci´on completa desde el inicio."""
		cursor.reproducir_todo()

	def do_PLAYMARKS(self, marcas):
		"""Reproduce las proximas marcas dadas por parametro desde donde se
		encuentra el cursor actualmente."""
		cursor.reproducir_hasta(marcas)

	def do_PLAYSECONDS(self, segundos):
		"""Reproduce los proximos segundos dados desde donde esta el cursor."""
		cursor.reproducir_segundos(segundos)


Shell().cmdloop()






