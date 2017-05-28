import cmd

import TP3objetos
#-----------------------------------------------------------------------


REPRODUCTOR = TP3objetos.Reproductor()
CURSOR = TP3objetos.Cursor(REPRODUCTOR)
#-----------------------------------------------------------------------


class Shell(cmd.Cmd): #definir nombres cursor, etc,...?

	intro = "Bienvenido a 'Sounds of Cyber City'\n Ingrese help o ? para listar los comandos.\n"
	prompt = "->> "

	def do_LOAD(self, archivo): #falta
		"""Carga la cancion desde el archivo. 
		Reemplaza la cancion en edicion actual si es que la hay."""
		REPRODUCTOR.load(archivo)

	def do_STORE (self, archivo):#falta
		"""Guarda la cancion."""
		REPRODUCTOR.store(archivo)

	def do_STEP (self, parametro):
		"""Avanza a la siguiente marca de tiempo."""
		try:
			CURSOR.step()
		except StopIteration:
			print("Este es el fin de la cancion, no puede avanzar mas.")
		except ValueError:
			print("La cancion esta vacia. \n Por favor, cargue una cancion o genere una.")

	def do_BACK(self, parametro):
		"""Retrocede a la anterior marca de tiempo."""
		try:
			CURSOR.back()
		except StopIteration:
			print("Este es el principio de la cancion, no puede retroceder mas.")
		except ValueError:
			print("No hay cancion cargadas o creadas. \n Por favor, cargue una cancion o genera")

	def do_STEPM (self, n):
		"""Avanza N marcas de tiempo hacia adelante."""
		if type(n) != int:
			print("Tipo de dato recibido incorrecto. \n Por favor, ingrese un numero valido.")
			return
		CURSOR.step(n)

	def do_BACKM(self, n):
		"""Retrocede N marcas de tiempo hacia atras."""
		if type(n) != int:
			print("Tipo de dato recibido incorrecto. \n Por favor, ingrese un numero valido.")
			return
		CURSOR.back(n)

	def do_TRACKADD(self, funcion, frecuencia, volumen):
		"""Agrega un track con el sonido indicado."""
		REPRODUCTOR.track_add()

	def do_TRACKDEL(self, numero_track):
		"""Elimina un track por numero."""
		REPRODUCTOR.track_del(numero_track)

	def do_MARKADD(self, duracion):
		"""Agrega una marca de tiempo de la duracion establecida."""
		CURSOR.mark_add(duracion)

	def do_MARKADDNEXT(self, duracion):
		"""Agrega una marca de tiempo de la duracion establecida
		luego de la marca en la cual esta
		actualmente el cursor"""
		CURSOR.mark_add_next(duracion)

	def do_MARKADDPREV(self, duracion):
		"""Agrega una marca de tiempo de la duracion establecida
		antes de la marca en la cual esta
		actualmente el cursor"""
		CURSOR.mark_add_prev(duracion)

	def do_TRACKON(self, numero_track):
		"""Habilita al track durante la marca de tiempo
		en la cual esta parada el cursor."""
		CURSOR.activar_track(numero_track)

	def do_TRACKOFF(self, numero_track):
		"""Desabilita al track durante la marca de tiempo
		 en la cual esta parada el cursor."""
		CURSOR.desactivar_track(numero_track)

	def do_PLAY(self, parametro):
		"""Reproduce la marca en la que se encuentra el cursor actualmente."""
		CURSOR.reproducir_marca()

	def do_PLAYALL(self, parametro):
		"""Reproduce la canci´on completa desde el inicio."""
		CURSOR.reproducir_todo()

	def do_PLAYMARKS(self, marcas):
		"""Reproduce las proximas marcas dadas por parametro desde donde se
		encuentra el cursor actualmente."""
		CURSOR.reproducir_hasta(marcas)

	def do_PLAYSECONDS(self, segundos):
		"""Reproduce los proximos segundos dados desde donde esta el cursor."""
		CURSOR.reproducir_segundos(segundos)


Shell().cmdloop()




