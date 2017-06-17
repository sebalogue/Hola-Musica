from lista_enlazada import IteradorListaEnlazada
from marca_de_tiempo import MarcaDeTiempo

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
		if not actual:
			return
		while actual and not iterador_auxiliar.esta_al_final():
			actual.track_agregar()
			actual = iterador_auxiliar.avanzar()
		actual.track_agregar()

	def track_eliminar(self, posicion_de_track):
		"""
		Recorre todo la cancion eliminando de las marcas de tiempo, 
		el track en la posicion indicada.
		"""
		posicion = int(posicion_de_track)
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		actual = iterador_auxiliar.elemento_actual()		
		if not actual:
			return
		while actual and not iterador_auxiliar.esta_al_final():
			actual.track_eliminar(posicion)
			actual = iterador_auxiliar.avanzar() 
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
		con la duracion indicada. Si esta parado en la ultima posicion, 
		la marca se agrega despues de esta.
		"""
		dato = MarcaDeTiempo(float(duracion), canales)
		self.iterador.insertar_siguiente(dato)

	def marca_agregar_previo(self, duracion, canales):
		"""
		Pre: recibe una duracion (entero o decimal), y los canales de la cancion (entero).
		Post: agrega una marca de tiempo en la posicion anterior del cursor
		con la duracion indicada. Si esta parada en la primera posicion, la marca se agrega
		antes de esta, y se actualizan las posiciones.
		"""
		dato = MarcaDeTiempo(float(duracion), canales)
		self.iterador.insertar_anterior(dato)
		self.posicion += 1

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
	
	def _obtener_tiempos_y_tracks_hasta(self, mensaje, limite, factor=None):
		"""
		Pre: recibe un limite (entero o decimal) de hasta donde obtendra datos desde la posicion actual 
		inclusive, un mensaje (cadena) de error en caso de que la limite recibida sea menor a 1,
		un factor (entero o decimal) que junto al limite estableceran una condicion (limite >= factor)
		durante el ciclo.
		Si no se recibe limite, recorrera desde el principio de la cancion.
		Si no se recibe un factor, la funcion, toma comportamiento exclusivo para obtener segundos. 
		Post: devuelve una lista de lista con los tiempos y tracks desde la posicion actual hasta 
		la limite recibida.
		"""
		if not self.actual:
			raise ValueError("Cancion Vacia.")
		if limite and limite <= 0:
			raise ValueError(mensaje)

		marca_actual = self.actual
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		posicion_auxiliar = 0
		tiempos_y_tracks = []

		if limite:
			for _ in range(self.posicion):
				iterador_auxiliar.avanzar()
				posicion_auxiliar += 1
		else:
			limite = len(self.cancion) - 2

		if factor is None:
			comodin = marca_actual.dar_tiempo()
			if comodin <= limite:
				tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
		else:
			comodin = factor
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
	
		while marca_actual and (limite >= comodin) and (posicion_auxiliar < len(self.cancion) - 1):
			marca_actual = iterador_auxiliar.avanzar()
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
			if factor is None:
				comodin = marca_actual.dar_tiempo()
				limite -= comodin
			else:
				comodin += 1
			posicion_auxiliar += 1
	
		return tiempos_y_tracks	

	def obtener_cancion_completa(self):
		"""
		Devuelve una lista de listas con el tiempo y los 
		tracks activados de toda la cancion representada por la lista.
		"""
		return self._obtener_tiempos_y_tracks_hasta(None, None, 0)

	def obtener_proximas_x_marcas(self, marca):
		"""
		Pre: recibe un entero correspondiente a las marcas a 
		obtener desde la posicion actual.
		Post: devuelve una lista de listas con el tiempo y los 
		tracks activados con las proximas marcas desde la 
		posicion.
		"""
		marca = int(marca) - 2
		mensaje = "Marca debe ser mayor a 0"
		return self._obtener_tiempos_y_tracks_hasta(mensaje,marca,0)

	def obtener_segundos_hasta(self, segundos):
		"""
		Pre: recibe segundos (entero o decimal) mayor a cero.
		Post: devuelve una lista de listas con los tiempos y tracks 
		habilitados desde la posicion actual hasta que las suma de 
		sus tiempo acumulados alcancen a los segundos dados por parametro.
		"""
		segundos = float(segundos)
		mensaje = "Segundos debe ser mayor a cero"
		return self._obtener_tiempos_y_tracks_hasta(mensaje,segundos,None)