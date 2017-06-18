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
		if len(self.cancion) == 0:
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
		if len(self.cancion) == 0:
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

	def _obtener_tiempos_y_tracks(self, limite, marca_inicial, posicion, iterador, factor=None):
		"""
		Pre: recibe un limite (entero o decimal) mayor a cero, correspodiente a la marca hasta donde debe recorrer, 
		recibe la marca inicial (objeto de la clase MarcadeTiempo) y su posicion (entero) correspondientes al punto 
		de partida, un iterador (objeto de la clase IteradorListaEnlazada) que este apuntando a la posicion 
		actual y un factor (entero o decimal) que se utlizara para distinguir entre que tipo de recorrido hara:
		Post:
		Si factor es None o no se recibe factor, obtendra los tiempos y tracks habilitados en base a unidades de 
		tiempo(segundos)
		Si factor es 0, lo hara en base a las marcas de tiempo.
		"""
		if limite <= 0 or posicion < 0:
			raise ValueError("Parametros invalidos")

		if not isinstance(marca_inicial, MarcaDeTiempo) or not isinstance(iterador, IteradorListaEnlazada):
			raise TypeError("Parametros invalidos")

		tiempos_y_tracks = []
		
		limite, comodin = self._determinar_e_inicializar_caso_de_obtencion(factor, limite, marca_inicial, tiempos_y_tracks)
	
		while marca_inicial and (limite >= comodin) and (posicion < len(self.cancion) - 1):
			marca_inicial = iterador.avanzar()
			tiempos_y_tracks.append(marca_inicial.dar_tiempo_y_habilitados())
			if factor is None:
				comodin = marca_inicial.dar_tiempo()
				limite -= comodin
			else:
				comodin += 1
			posicion += 1
	
		return tiempos_y_tracks	

	def _determinar_e_inicializar_caso_de_obtencion(self, factor, limite, marca_inicial, tiempos_y_tracks):
		"""
		Subfuncion de _obtener_tiempos_y_tracks.
		Pre: recibe el factor, el limite (entero), la marca inicial (objeto de la clase MarcaDeTiempo), 
		y la lista de tiempos y tracks. La funcion supone que los elementos recibidos son correctos.
		Post: realize el primer append a la lista y devuelve un tupla (limite, comodin) con los valores que 
		se van a usar en el ciclo posterior. 
		"""
		if factor is None:
			comodin = marca_inicial.dar_tiempo()
			if comodin <= limite:
				tiempos_y_tracks.append(marca_inicial.dar_tiempo_y_habilitados())
				limite -= comodin
		else:
			limite -= 2
			comodin = factor
			tiempos_y_tracks.append(marca_inicial.dar_tiempo_y_habilitados())

		return (limite, comodin)

	def obtener_cancion_completa(self):
		"""
		Devuelve una lista de listas con el tiempo y los 
		tracks activados de toda la cancion representada por la lista.
		"""
		if not self.actual:
			raise ValueError("Cancion Vacia.")
		largo_cancion = len(self.cancion)
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		marca_inicial = iterador_auxiliar.elemento_actual()
		return self._obtener_tiempos_y_tracks(largo_cancion, marca_inicial, 0, iterador_auxiliar, 0)

	def obtener_proximas_x_marcas(self, marca):
		"""
		Pre: recibe un entero correspondiente a las marcas a 
		obtener desde la posicion actual.
		Post: devuelve una lista de listas con el tiempo y los 
		tracks activados con las proximas marcas desde la 
		posicion.
		"""
		marca = int(marca)
		if not self.actual:
			raise ValueError("Cancion Vacia.")
		if marca <= 0:
			raise ValueError("Marca debe ser mayor a cero.")
		marca_inicial = self.actual
		posicion = self.posicion
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		for _ in range(self.posicion):
			iterador_auxiliar.avanzar() 
		return self._obtener_tiempos_y_tracks(marca, marca_inicial, posicion, iterador_auxiliar, 0)

	def obtener_segundos_hasta(self, segundos):
		"""
		Pre: recibe segundos (entero o decimal) mayor a cero.
		Post: devuelve una lista de listas con los tiempos y tracks 
		habilitados desde la posicion actual hasta que las suma de 
		sus tiempo acumulados alcancen a los segundos dados por parametro.
		"""
		segundos = float(segundos)
		if not self.actual:
			raise ValueError("Cancion Vacia.")
		if segundos <= 0:
			raise ValueError("Segundos debe ser mayor a cero.")
		marca_inicial = self.actual
		posicion = self.posicion
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		for _ in range(self.posicion):
			iterador_auxiliar.avanzar()
		return  self._obtener_tiempos_y_tracks(segundos, marca_inicial, posicion, iterador_auxiliar, None)
