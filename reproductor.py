import soundPlayer
import csv
from lista_enlazada import ListaEnlazada
from cursor import Cursor
from track import Track
from track import FUNCIONES_SONIDO

DUTY_CYCLE = 0.15

class Reproductor: 
	"""Representa un reproductor de sonidos."""
	def __init__(self, cancion=None):
		"""
		Pre: Recibe una cancion (ubicacion de un archivo.plp).
		Post: incia un reproductor con la cancion recibida cargada. 
		Si no se recibe cancion, el reproductor inicia con una 
		cancion vacia.
		"""
		self.canales = 0 
		self.tracks = []
		self.info_tracks = []
		self.cancion = ListaEnlazada() 
		self.cursor = Cursor(self.cancion)
		if cancion:
			self.cargar(cancion)		 

	def dar_cancion(self):
		"""
		Devuelve la cancion cargada.
		"""
		return self.cancion

	def dar_canales(self):
		"""
		Devuelve los canales de la cancion.
		"""
		return self.canales

	def avanzar(self, pasos = 1):
		"""
		Pre: Recibe una cantidad de pasos a avanzar en la linea de tiempo 
		de la cancion. Pasos es un entero mayor a cero. (por defecto es 1).
		Post: avanza tantos pasos en la cancion.
		"""
		pasos = int(pasos)
		if pasos <= 0:
			raise ValueError("Debe ser un numero entero mayor a cero")
		self.cursor.avanzar(pasos)
	
	def retroceder(self, pasos = 1):
		"""
		Pre: Recibe una cantidad de pasos a retroceder en la linea de 
		tiempo de la cancion. Pasos es un entero mayor a cero (por defecto 
		es 1).
		Post retrocede tantos pasos en la cancion.
		"""
		pasos = int(pasos)
		if pasos <= 0:
			raise ValueError("Debe ser un numero entero mayor a cero")
		self.cursor.retroceder(pasos)

	def validar_tiempo(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal).
		Post: valida que el valor recibido es correcto, y devuelve el 
		tiempo convertido a float.
		"""
		tiempo = float(tiempo)
		if tiempo <= 0:
			raise ValueError("Tiempo debe ser un numero mayor a cero.")
		return tiempo

	def marca_agregar(self, tiempo):
		"""
		Pre: recibe un tiempo (numero) mayor a cero.
		Post: Agrega una nueva marca de tiempo en las posicion actual del 
		cursor.
		"""
		tiempo = self.validar_tiempo(tiempo)
		self.cursor.marca_agregar(tiempo, self.canales)

	def marca_agregar_siguiente(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal) mayor a cero.
		Post: Agrega una nueva marca de tiempo un paso adelante de la 
		posicion actual del cursor.
		"""
		tiempo = self.validar_tiempo(tiempo)
		self.cursor.marca_agregar_siguiente(tiempo, self.canales)

	def marca_agregar_previo(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal) mayor a cero.
		Post Agrega una nueva marca de tiempo un paso atras de la posicion 
		actual del cursor 
		"""
		tiempo = self.validar_tiempo(tiempo)
		self.cursor.marca_agregar_previo(tiempo, self.canales)

	def track_agregar(self, funcion_sonido, frecuencia, volumen): 
		"""
		Pre: recibe una funcion de la lista de funciones (cadena), una 
		frecuencia, volumen (enteros o decimales). 
		Post: crea y agrega un nuevo track.
		"""
		track = Track(funcion_sonido, frecuencia, volumen, DUTY_CYCLE)
		self.tracks.append(track.dar_sonido())
		self.info_tracks.append([funcion_sonido.upper(), str(frecuencia), str(volumen)])
		self.canales += 1
		self.cursor.track_agregar()

	def track_eliminar(self, posicion):
		"""
		Pre: recibe una posicion. Posicion es un entero.
		Post: elimina el track de la posicion indicada.
		"""
		if int(posicion) < 0 :
			raise ValueError("Posicion no valida.")
		self.tracks.pop(posicion)
		self.info_tracks.pop(posicion)
		self.canales -= 1
		self.cursor.track_eliminar(posicion)

	def track_activar(self, indice_de_track):
		"""
		Pre: recibe el indice (entero) del track a activar. 
		Indice es mayor cero, y menor o igual a la cantidad de canales.  
		Post: activa el track en la posicion actual del cursor.
		"""
		indice = int(indice_de_track)
		if (indice < 0) or (indice > self.canales - 1):
			raise IndexError("No existe track en este indice.")
		self.cursor.activar_track(indice)

	def track_desactivar(self, indice_de_track):
		"""
		Pre: recibe el indice (entero) del track a activar. 
		Indice es mayor cero, y menor o igual a la cantidad de canales.  
		Post: activa el track en la posicion actual del cursor.
		"""
		indice = int(indice_de_track)
		if not (indice >= 0) or not (indice <= self.canales - 1):
			raise IndexError("No existe track en este indice.")
		self.cursor.desactivar_track(indice)

	def obtener_sonidos(self, tracks_habilitados):
		"""
		Pre: Recibe una lista de indices a los tracks habilitados.
		Post: Devuelve una lista de sonidos habilitados.
		"""
		lista_de_sonidos = []
		for indice in  tracks_habilitados:
			lista_de_sonidos.append(self.tracks[indice]) #Podriamos validar esto de alguna manera?.
		return lista_de_sonidos

	def reproducir(self, tiempos_y_habilitados):
		"""
		Pre: recibe un lista de tuplas, donde cada una tiene un tiempo (numero), 
		y una lista de tracks habilitados.
		Post: reproduce la cantidad recibida de marcas de tiempo (tuplas).   
		"""
		reproductor_interno = soundPlayer.SoundPlayer(self.canales)
		tiempos_y_sonidos = [] 
		
		for tiempo_y_habilitado in tiempos_y_habilitados:
			tiempo = tiempo_y_habilitado[0]
			sonidos = self.obtener_sonidos(tiempo_y_habilitado[1])
			tiempos_y_sonidos.append((tiempo, sonidos))
		
		for tiempo_y_sonido in tiempos_y_sonidos:
			tiempo, sonidos = tiempo_y_sonido
			reproductor_interno.play_sounds(sonidos, tiempo)

	def reproducir_marca(self):
		"""
		Reproduce la marca actual.
		"""
		tiempos_y_tracks_habilitados = self.cursor.obtener_marca()
		self.reproducir(tiempos_y_tracks_habilitados)

	def reproducir_completa(self):
		"""
		Reproduce la cancion completa.
		"""
		tiempos_y_tracks_habilitados = self.cursor.obtener_cancion_completa()
		self.reproducir(tiempos_y_tracks_habilitados)

	def reproducir_marcas(self, marcas):
		"""
		Pre: recibe un entero.
		Post: reproduce la siguientes marcas, contando desde la posicion actual.
		"""
		marcas = int(marcas)
		tiempos_y_tracks_habilitados = self.cursor.obtener_proximas_x_marcas(marcas)
		self.reproducir(tiempos_y_tracks_habilitados)

	def reproducir_segundos(self, segundos):
		"""
		Pre: recibe un entero o decimal.
		Post: reproduce los siguientes segundos desde la posicion actual.
		"""
		segundos = float(segundos)
		tiempos_y_tracks_habilitados = self.cursor.obtener_segundos_hasta(segundos)
		self.reproducir(tiempos_y_tracks_habilitados)

	def guardar(self, nombre_de_archivo):
		"""
		Convierte la cancion (lista enlazada) en un archivo.plp.
		"""
		nombre = str(nombre_de_archivo)
		cursor_auxiliar = Cursor(self.cancion)
		tiempos_y_tracks = cursor_auxiliar.obtener_cancion_completa()
		tiempo_anterior = None
		
		with open(nombre + ".plp", 'w', newline = '') as _ :
			escritor = csv.writer( _ , delimiter = ",")		
			escritor.writerow(["C", self.canales])
			
			for sonido in self.info_tracks:
				escritor.writerow(["S", "|".join(sonido)])
						
			for tiempo, tracks in tiempos_y_tracks:
				tiempo_anterior = self._guardar_tracks(tiempo, tracks, tiempo_anterior, escritor)			

	def _guardar_tracks(self, tiempo, tracks, tiempo_anterior, escritor):
		"""Escribe en el archivo las marcas de tiempo. Devuelve el tiempo de la marca
		anterior escrita para actualizarlo."""
		cadena_de_tracks = ""
		if tiempo != tiempo_anterior:
			escritor.writerow(["T", tiempo])
			tiempo_anterior = tiempo
		for canal in range(self.canales):
			if canal in tracks:
				cadena_de_tracks += "#"
				continue
			cadena_de_tracks += "."
		escritor.writerow(["N",cadena_de_tracks])
		return tiempo_anterior

	def _cargar_canales(self, canales):
		"""
		Pre: recibe la cantidad (entero) de canales a cargar.
		Post: carga la cantidad de canales.
		"""
		if not canales.isdigit() or not (int(canales)):
			raise ValueError("Error en lectura del archivo.plp 1")
		self.canales = int(canales)

	def _cargar_sonidos(self, info_sonido):
		"""
		Pre: recibe la informacion (cadena) correspondiente a un sondido, de 
		la forma: funcion_de_sonido|frecuencia|volumen. Donde funcion_de_sonido 
		es una de las dadas por el programa, frecuencia y volumen son numeros 
		(enteros o decimales).
		Post: carga el sonido.
		"""
		if self.canales == len(self.tracks):
			raise ValueError("Error en lectura del archivo.plp 2: hay menos canales que sonidos")
		info = info_sonido.split("|")
		if not len(info) == 3:
			raise ValueError("Error en lectura del archivo.plp 2.5")
		funcion, frecuencia, volumen = info
		try:
			frecuencia = float(frecuencia)
			volumen = float(volumen)
		except ValueError:
			raise ValueError("Error en lectura del archivo.plp 3")
		funcion = funcion.lower()
		if not funcion in FUNCIONES_SONIDO:
			raise ValueError("Error en lectura del archivo.plp 3.5")
		self.track_agregar(funcion, frecuencia, volumen)
		self.canales -= 1

	def _actualizar_tiempo(self, tiempo_anterior, tiempo):
		"""
		Pre: recibe un tiempo y el tiempo anterior al mismo (ambos enteros).
		Post: actualiza el tiempo anterior.
		"""
		try:
			tiempo = float(tiempo)
		except ValueError:
			raise ValueError("Error en lectura del archivo.plp 4")
		if tiempo != tiempo_anterior:
			tiempo_anterior = tiempo
		return tiempo_anterior
	
	def _cargar_marcas(self, tiempo, info_tracks, pasos): # Habria que controlar que el tiempo no sea cero?
		"""
		Pre: recibe un tiempo (entero o decimal), informacion de los tracks (cadena de #.) 
		activados y una cantidad de pasos realizados (entero).
		Post: Agrega una marca de tiempo con el tiempo dado, activa los tracks correspondiente 
		a la informacion recibida, y devuelve los pasos actualizados, con los realizados durante
		la carga.
		""" 
		if tiempo is None:
			raise ValueError("Error en lectura del archivo.plp 5")
		if len(self.cancion) == 0: 
			self.marca_agregar(tiempo)
		else:
			self.marca_agregar_siguiente(tiempo)
			self.avanzar()
			pasos += 1
		lista_de_tracks = list(info_tracks)
		contador = 0
		for track in lista_de_tracks:
			if not (track in "#."):
				raise ValueError("Error en lectura del archivo.plp 6")
			if track == "#":
				self.track_activar(contador)
			contador += 1
		return pasos

	def cargar(self, cancion):
		"""
		Carga una cancion al reproductor.
		Cancion es un archivo.plp con formato de cancion.
		"""	
		pasos = 0
		with open(cancion) as _cancion:
			lector = csv.reader(_cancion, delimiter = ",")
			linea = next(lector, None)
			tiempo_anterior = None
			while linea:
				indice = linea[0]
				datos = linea[1]
				if indice == "C":
					self._cargar_canales(datos)
				if indice == "S":
					self._cargar_sonidos(datos)
				if indice == "T":
					tiempo_anterior = self._actualizar_tiempo(tiempo_anterior, datos)
				if indice == "N":
					pasos = self._cargar_marcas(tiempo_anterior, datos, pasos)
				linea = next(lector, None)
		self.retroceder(pasos)
