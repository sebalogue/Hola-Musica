#-------------------------------------------------------------------------
import lista_enlazada
import marca_de_tiempo
#-------------------------------------------------------------------------
IteradorListaEnlazada = lista_enlazada.IteradorListaEnlazada
MarcaDeTiempo = marca_de_tiempo.MarcaDeTiempo
#-------------------------------------------------------------------------
class Cursor:
	"""
	Representa un cursor que recorre las marcas de tiempo de una cancion
	"""
	def __init__(self, cancion):
		"""
		Crea el cursor.
		"""
		self.cancion = cancion
		self.iterador = IteradorListaEnlazada(self.cancion)
		self.actual = self.iterador.elemento_actual()
		self.posicion = 0

	def avanzar(self, n = 1):
		"""
		Avanza n (entero) veces por la lista.
		"""
		n = int(n)
		if not len(self.cancion):
			raise ValueError("Cancion vacia.")
		if self.posicion == (len(self.cancion) - 1):
			raise StopIteration("Fin de la cancion.")
		for veces in range(n):
			self.actual = self.iterador.avanzar()
			self.posicion += 1

	def retroceder(self, n = 1):
		"""
		Retrocede n (entero) veces al anterior elemento de la lista.
		"""
		n = int(n)
		if not len(self.cancion):
			raise ValueError("Cancion vacia.")
		if self.posicion == 0:
			raise StopIteration("Principio de la cancion.")
		for veces in range(n):
			self.actual = self.iterador.retroceder()
			self.posicion -= 1
	
	def track_agregar(self):
		"""
		Recorre toda la cancion agregando un nuevo track deshabilitado
		a las marcas de tiempo.
		"""
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		actual = iterador_auxiliar.elemento_actual()
		i = 0
		if not actual:
			return
		while actual and (i < len(self.cancion)-1):
			actual.track_agregar()
			actual = iterador_auxiliar.avanzar()
			i += 1
		actual.track_agregar()

	def track_eliminar(self, posicion_de_track):
		"""
		Recorre todo la cancion eliminando de las marcas de tiempo, 
		el track en la posicion indicada.
		"""
		posicion = int(posicion_de_track)
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		actual = iterador_auxiliar.elemento_actual()		
		i = 0
		if not actual:
			return
		while actual and (i < len(self.cancion)-1):
			actual.track_eliminar(posicion)
			actual = iterador_auxiliar.avanzar() 
			i += 1
		actual.track_eliminar(posicion)

	def marca_agregar(self, duracion, canales):
		"""
		Pre: recibe una duracion (entero o decimal), y los canales de la cancion (entero).
		Post: agrega una marca de tiempo en la posicion actual del cursor
		con la duracion indicada.
		"""
		canales = int(canales)
		dato = MarcaDeTiempo(duracion, canales)
		self.iterador.insertar(dato)
		self.actual = dato

	def marca_agregar_siguiente(self, duracion, canales):
		"""
		Pre: recibe una duracion (entero o decimal), y los canales de la cancion (entero).
		Post: agrega una marca de tiempo en la posicion siguiente del cursor
		con la duracion indicada.
		"""
		if (not self.actual) or (self.posicion == (len(self.cancion) - 1)):
			dato = MarcaDeTiempo(float(duracion), canales)
			self.iterador.insertar_ultimo(dato)
			return
		self.actual = self.iterador.avanzar()
		self.marca_agregar(float(duracion), canales)
		self.actual = self.iterador.retroceder()

	def marca_agregar_previo(self, duracion, canales):
		"""
		Pre: recibe una duracion (entero o decimal), y los canales de la cancion (entero).
		Post: agrega una marca de tiempo en la posicion anterior del cursor
		con la duracion indicada.
		"""
		if self.posicion == 0:
			dato = MarcaDeTiempo(float(duracion), canales)
			self.iterador.insertar_principio(dato)
			self.posicion += 1
			return
		self.actual = self.retroceder()
		self.marca_agregar(float(duracion), canales)
		self.actual = self.avanzar()
		self.actual = self.avanzar()

	def activar_track(self, numero_track):
		"""
		Pre: recibe un numero de track existente.
		Post: activa el numero de track de la marca 
		de tiempo en la cual esta el cursor.
		"""
		numero_track = int(numero_track)
		if numero_track < 0:
			raise ValueError("Debe ingresar un numero de track.")
		self.actual.track_activar(numero_track)

	def desactivar_track(self, numero_track):
		"""
		Pre: recibe un numero de track existente.
		Post: desactiva el numero de track de la marca 
		de tiempo en la cual esta el cursor.
		"""
		numero_track = int(numero_track)
		if numero_track < 0:
			raise ValueError("Debe ingresar un numero de track.")
		self.actual.track_desactivar(numero_track)

	def obtener_marca(self):
		"""
		Devuelve una lista de listas de tiempo y track habilitado 
		en el que se encuentra el cursor.
		"""
		if not self.actual:
			raise ValueError("Cancion vacia.")
		return [self.actual.dar_tiempo_y_habilitados()]			   			   
	
	def obtener_cancion_completa(self):
		"""
		Reproduce toda la cancion representada por la lista.
		"""
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		marca_actual = iterador_auxiliar.elemento_actual()
		if not marca_actual:
			raise ValueError("Cancion vacia.")
		tiempos_y_tracks = []
		tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
		i = 0
		while marca_actual and (i < len(self.cancion)-1):
			marca_actual = iterador_auxiliar.avanzar()
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
			i += 1
		return tiempos_y_tracks

	def obtener_proximas_x_marcas(self, marca):
		"""
		Pre: recibe un entero correspondiente a las marcas a 
		obtener desde la posicion actual.
		Post: devuelve una lista de listas con el tiempo y los 
		tracks activados con las proximas marcas desde la 
		posicion.
		"""
		marca = int(marca)

		if marca < 1:
			raise ValueError("Marca deber ser mayor a 0.")
		
		marca_actual = self.actual
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		posicion_auxiliar = 0
		for _ in range(self.posicion):
			iterador_auxiliar.avanzar()
			posicion_auxiliar += 1
		
		if not marca_actual:
			raise ValueError("Cancion vacia.")

		tiempos_y_tracks = []
		tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
		
		i = 0
		while marca_actual and (i < marca - 1) and (posicion_auxiliar < len(self.cancion) - 1): 
			marca_actual = iterador_auxiliar.avanzar()
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
			posicion_auxiliar += 1
			i += 1

		return tiempos_y_tracks

	def obtener_segundos_hasta(self, segundos):
		"""
		Pre: recibe segundos (entero o decimal) mayor a cero.
		Post: devuelve una lista de listas con los tiempos y tracks 
		habilitados desde la posicion actual hasta que las suma de 
		sus tiempo acumulados alcancen a los segundos dados por parametro.
		"""
		segundos = float(segundos)
		
		if segundos <= 0:
			raise ValueError("Segundos debe ser mayor a cero.")
		if not self.actual:
			raise ValueError("Cancion vacia.")
		
		marca_actual = self.actual
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		posicion_auxiliar = 0
		for _ in range(self.posicion):
			iterador_auxiliar.avanzar()
			posicion_auxiliar += 1

		
		tiempo_marca = marca_actual.dar_tiempo()
		tiempos_y_tracks = []
		if tiempo_marca <= segundos:
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
		while marca_actual and (segundos >= tiempo_marca) and (posicion_auxiliar < len(self.cancion) - 1): 
			marca_actual = iterador_auxiliar.avanzar()
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
			tiempo_marca = marca_actual.dar_tiempo()
			segundos -= tiempo_marca
			posicion_auxiliar += 1
		return tiempos_y_tracks