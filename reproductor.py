import soundPlayer
import csv
from lista_enlazada import ListaEnlazada
from cursor import Cursor
from track import Track
from track import FUNCIONES_SONIDO

class Reproductor: 
	"""Representa un reproductor de sonidos."""
	def __init__(self):
		"""
		Crea el reproductor de canciones, el cual inicia sin ninguna 
		cancion.
		"""
		self.cancion = ListaEnlazada() 
		self.canales = 0 
		self.tracks = []
		self.info = []
		self.cursor = Cursor(self.cancion) 

	def dar_cancion(self):
		"""
		Devuevlve la cancion cargada.
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
		de la cancion. Pasos es una entero mayor a cero. (por defecto es 1).
		Post: avanza tantos pasos en la cancion.
		"""
		pasos = int(pasos)
		if pasos < 0:
			raise ValueError("Debe ser un numero entero mayor a cero")
		self.cursor.avanzar(pasos)
	
	def retroceder(self, pasos = 1):
		"""
		Pre: Recibe una cantidad de pasos a retrroceder en la linea de 
		tiempo de la cancion. Pasos es un entero mayor a cero (por defecto 
		es 1).
		Post retrocede tantos pasos en la cancion.
		"""
		pasos = int(pasos)
		if pasos < 0:
			raise ValueError("Debe ser un numero entero mayor a cero")
		self.cursor.retroceder(pasos)

	def marca_agregar(self, tiempo):
		"""
		Pre: recibe un tiempo (numero) mayor a cero.
		Post: Agrega una nueva marca de tiempo en las posicion actual del 
		cursor.
		"""
		tiempo = float(tiempo)
		if tiempo <= 0.0:
			raise ValueError("Tiempo debe ser un numero mayor a cero.")
		self.cursor.marca_agregar(tiempo, self.canales)

	def marca_agregar_siguiente(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal) mayor a cero.
		Post: Agrega una nueva marca de tiempo un paso adelante de la 
		posicion actual del cursor.
		"""
		tiempo = float(tiempo)
		if tiempo <= 0:
			raise ValueError("Tiempo debe ser un numero mayor a cero.")
		self.cursor.marca_agregar_siguiente(tiempo, self.canales)

	def marca_agregar_previo(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal) mayor a cero.
		Post Agrega una nueva marca de tiempo un paso atras de la posicion 
		actual del cursor 
		"""
		tiempo = float(tiempo)
		if tiempo <= 0:
			raise ValueError("Tiempo deber ser un numero mayor a cero.")
		self.cursor.marca_agregar_previo(tiempo, self.canales)

	def track_agregar(self, funcion_sonido, frecuencia, volumen): 
		"""
		Pre: recibe una funcion de la lista de funciones (cadena), una 
		frecuencia, volumen (enteros o decimales). 
		Post: crea y agrega un nuevo track.
		"""
		duty_cycle = 0.15
		track = Track(funcion_sonido, frecuencia, volumen, duty_cycle)
		self.tracks.append(track.dar_sonido())
		self.info.append([funcion_sonido.upper(), str(frecuencia), str(volumen)])
		self.canales += 1
		self.cursor.track_agregar()

	def track_eliminar(self, posicion):
		"""
		Pre: recibe una posicion. Posicion es un entero.
		Post: elimina el track de la posicion indicada.
		"""
		if posicion < 0 :
			raise ValueError("Posicion no valida.")
		self.tracks.pop(posicion)
		self.info.pop(posicion)
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
			lista_de_sonidos.append(self.tracks[indice])
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
			tiempo_A = tiempo_y_habilitado[0]
			sonidos_A = self.obtener_sonidos(tiempo_y_habilitado[1])
			tiempos_y_sonidos.append((tiempo_A, sonidos_A))
		
		for tiempo_y_sonido in tiempos_y_sonidos:
			tiempo_B = tiempo_y_sonido[0]
			sonidos_B = tiempo_y_sonido[1] 
			reproductor_interno.play_sounds(sonidos_B, tiempo_B)

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
		
		with open(nombre + ".plp", 'w', newline = '') as _archivo:
			escritor_A = csv.writer(_archivo, delimiter = ",")		
			escritor_A.writerow(["C", self.canales])
			
			for sonido in self.info:
				escritor_A.writerow(["S", "|".join(sonido)])
						
			for tiempo, tracks in tiempos_y_tracks:
				lista_de_tracks = []

				if tiempo != tiempo_anterior:
					escritor_A.writerow(["T", tiempo])
					tiempo_anterior = tiempo

				for canal in range(self.canales):
					if canal in tracks:
						lista_de_tracks.append("#")
						continue
					lista_de_tracks.append(".")
				escritor_A.writerow(["N","".join(lista_de_tracks)])

	def reiniciar(self):
		"""
		Reinicia la clase reproductor.
		Coloca todos sus atributos en su estado inicial. 
		"""
		self.cancion = ListaEnlazada() 
		self.canales = 0
		self.tracks = []
		self.info = []
		self.cursor = Cursor(self.cancion) 

	def cargar(self, cancion):
		"""
		Carga una cancion al reproductor.
		Cancion es un archivo.plp con formato de cancion.
		"""	
		pasos = 0
		with open(cancion) as _cancion:
			self.reiniciar()
			
			lector = csv.reader(_cancion, delimiter = ",")
			linea = next(lector, None)
			tiempo_anterior = None
			while linea:
				indice = linea[0]
				datos = linea[1]
				
				if indice == "C":
					if not datos.isdigit():
						self.reiniciar()
						raise ValueError("Error en lectura del archivo.plp 1")
					self.canales = int(datos)

				if indice == "S":
					barras = 0
					for caracter in datos:
						if caracter == "|":
							barras += 1
					if barras != 2:
						self.reiniciar()
						raise ValueError("Error en lectura del archivo.plp 2")
					info = datos.split("|")
					funcion, frecuencia, volumen = info
					if not se_puede_convertir_a_flotante(frecuencia) or not (se_puede_convertir_a_flotante(volumen)) or (not funcion.lower() in FUNCIONES_SONIDO):
						self.reiniciar()
						raise ValueError("Error en lectura del archivo.plp 3")
					self.track_agregar(funcion.lower(), float(frecuencia), float(volumen))
					self.canales -= 1

				if indice == "T":
					tiempo = datos
					if not se_puede_convertir_a_flotante(tiempo):
						self.reiniciar()
						raise ValueError("Error en lectura del archivo.plp 4")
					tiempo = float(tiempo)
					if tiempo != tiempo_anterior:
						tiempo_anterior = tiempo
				
				if indice == "N":
					if tiempo_anterior is None:
						self.reiniciar()
						raise ValueError("Error en lectura del archivo.plp 5")
					if len(self.cancion) == 0: 
						self.marca_agregar(tiempo_anterior)
					else:
						self.marca_agregar_siguiente(tiempo_anterior)
						self.avanzar()
						pasos += 1
					lista_de_tracks = list(datos)
					contador = 0
					for track in lista_de_tracks:
						if not (track in "#."):
							self.reiniciar()
							raise ValueError("Error en lectura del archivo.plp 6")
						if track == "#":
							self.track_activar(contador)
						contador += 1
				linea = next(lector, None)
		self.retroceder(pasos)


def se_puede_convertir_a_flotante(cadena):
	"""
	Pre: recibe una cadena.
	Post: Devuelve True si es posible convertirla en flotante, 
	False en caso contrario.
	"""
	try:
		float(cadena)
		return True
	except ValueError:
		return False
			
