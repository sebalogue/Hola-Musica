#nesesitan pilas, listas enlazadas y nodos..

class MarcaDeTiempo: #doc
	"""Representa una marca de tiempo que contiene canales en los cuales se hebilitan
	o desabilitan los tracks."""
	def __init__(self, tiempo, canales):
		"""Crea una marca de tiempo con el tiempo de duracion y la cantidad 
		de canales indicado."""
		self.tiempo = tiempo
		self.tracks = {}
		self.canales = int(canales) # creo que no es nesesario
		for track in range(1, canales+1):
			self.tracks[track] = False

	def track_on(self, track):
		"""Habilita el numero de track de la marca de tiempo."""
		self.tracks[track] = True

	def track_off(self, track):
		"""Desabilita el numero de track de la marca de tiempo."""
		self.tracks[track] = False

class Iterador: #doc.  #creo que no es nesesario self.siguiente
	"""Representa un iterador que va y vuelve."""
	def __init__(self, lista_enlazada):
		"""Crea un iterador para una lista enlazada que la puede recorrer 
		para atras y paar adelante.""" 
		self.lista = lista_enlazada
		self.anterior = None
		self.actual = lista_enlazada.prim
		self.siguiente = lista_enlazada.prim.prox
		self.pila_anteriores = Pila()

	def proximo(self):
		"""Pasa al siguiente elemento de la lista."""
		if not self.siguiente:
			return #return self.actual??
		self.pila_anteriores.apilar(self.anterior)
		self.anterior = self.actual
		self.actual = self.siguiente
		self.siguiente = self.siguiente.prox
		return self.actual

	def anterior(self):
		"""Vuelve al elemento anterior de la lista."""
		if self.pila_anteriores.esta_vacia():
			return #return self.actual??
		self.siguiente = self.actual
		self.actual = self.anterior
		self.anterior = self.pila_anteriores.desapilar()
		return self.actual

class Cursor: #doc
	"""Representa un cursor que recorre una lista enlazada..."""
	def __init__(self, lista):
		"""Crea el cursor."""
		self.lista = lista
		self.iterador = Iterador(lista)
		self.actual = lista.prim
		self.pocision = 0

	def step(n = 1):
		"""Avanza n veces por la lista."""
		for veces in range(n):
			self.actual = self.iterador.proximo()
			if self.pocision < self.lista.len:
				self.pocision += 1

	def back(n = 1):
		"""Retrocede al anterior elemento de la lista."""
		for veces in range(n):
			self.actual = self.iterador.anterior()
			if self.pocision > 0:
				self.pocision -= 1

	def mark_add(self, duracion):
		"""Agrega una marca de tiempo en la pocision actual del cursor
		con la duracion indicada."""
		canales = self.actual.canales
		dato = MarcaDeTiempo(duracion, canales)
		pocision = self.pocision
		self.lista.insert(dato, pocision)
		self.actual = self.iterador.proximo()

	def mark_add_next(self, duracion):
		"""Agrega una marca de tiempo en la pocision siguiente del cursor
		con la duracion indicada."""
		self.actual = self.iterador.proximo()
		mark_add(duracion)
		self.actual = self.iterador.anterior()

	def mark_add_prev(self, duracion):
		"""Agrega una marca de tiempo en la pocision anterior del cursor
		con la duracion indicada."""
		self.actual = self.iterador.anterior()
		mark_add(duracion)
		self.actual = self.iterador.proximo()

class Reproductor:

