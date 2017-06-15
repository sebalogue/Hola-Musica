class MarcaDeTiempo: 
	"""
	Representa una marca de tiempo que contiene canales en los cuales se habilitan
	o deshabilitan los tracks.
	"""
	def __init__(self, tiempo, canales):
		"""
		Pre: recibe un tiempo (entero o decimal), y los canales de una cancion.
		Post: crea una marca de tiempo con el tiempo recibido, la cantidad 
		de canales indicado, y con una lista de tracks habilitados.
		"""
		self.tiempo = float(tiempo)
		self.canales = int(canales) 
		self.tracks = []
		for track in range(canales):
			self.tracks.append(False)

	def track_activar(self, track):
		"""
		Habilita el numero de track de la marca de tiempo.
		"""
		self.tracks[track] = True

	def track_desactivar(self, track):
		"""
		Desabilita el numero de track de la marca de tiempo.
		"""
		self.tracks[track] = False
	
	def track_agregar(self):
		"""
		Agrega un nuevo track deshabiltado a la marca de tiempo.
		"""
		self.tracks.append(False)
		self.canales += 1

	def track_eliminar(self, posicion_de_track):
		"""
		Pre: recibe una osicion de track. La misma debe ser un numero entero,
		y con un track asociado.
		Post: elimina el track en la posicion indicada.
		"""
		posicion = int(posicion_de_track)
		self.tracks.pop(posicion)
		self.canales -= 1

	def tracks_habilitados(self):
		"""
		Devuelve los numeros de los tracks habilitados en la marca de tiempo.
		""" 
		return [num for num, track in enumerate(self.tracks) if track]

	def dar_tiempo(self):
		"""
		Devuelve el tiempo de duracion de la marca de tiempo.
		"""
		return self.tiempo

	def dar_tiempo_y_habilitados(self):
		"""
		Devuelve una tupla con el tiempo y los tracks habilitados de la marca de tiempo.
		"""
		tiempo_y_habilitados = (self.dar_tiempo(), self.tracks_habilitados())
		return tiempo_y_habilitados