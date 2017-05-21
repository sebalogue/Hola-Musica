class _Nodo():
	"""Clase que representa un elemento de lista enlazada"""
	def __init__(self, dato=None, prox=None):
		"""Pre: recibe un dato a almacenar, y una referencia al proximo Nodo.
		Post: su estado inicial, son estos dos atributos recibidos."""

		self.dato = dato
		self.prox = prox

	def __str__(self):
		"""Devuelve una reprentacion (cadena) informal del Nodo"""
		return str(self.dato)

	def __repr__(self):
		"""Devuelve una reprentacion (cadena) formal del Nodo"""
		return str(self)
#-----------------------------------------------------------------------------------

class ListaEnlazada():
	"""Representa una lista de elementos enlazados"""
	def __init__(self):
		self.prim = None
		self.ult = None
		self.len = 0

	def __len__(self):
		"""Devuelve el largo de la lista (Entero)"""
		return self.len 
	
	def __str__(self):
		"""Devuelve una representacion en cadena de texto de la lista"""
		cadena = []
		actual = self.prim
		while actual:
			if type(actual.dato) == str:
				cadena.append("'" + str(actual.dato) + "'")
			else:	
				cadena.append(str(actual.dato))
			actual = actual.prox

		return "[" + ", ".join(cadena) + "]"

	def __repr__(self):
		"""Devuelve un representacion formal en cadena de texto de la lista"""
		return str(self)

	def append(self, dato):
		nodo = _Nodo(dato)

		if self.len == 0:
			self.prim = nodo
		
		if self.ult :
			self.ult.prox = nodo
		
		self.ult = nodo

		self.len += 1

	def _insertar_prim(self, dato):
		"""Inserta un dato en la primera posicion"""
		nodo = _Nodo(dato)
		
		if self.len == 0:
			self.prim = nodo
			self.ult = nodo
			self.len += 1
			return

		nodo.prox = self.prim
		self.prim = nodo

		self.len += 1

	def insert(self,dato,posicion=0):
		"""Inserta un elemento en la posicion indicada"""
		if posicion <= 0 or self.len == 0:
			self._insertar_prim(dato)
			return

		if posicion >= self.len - 1:
			self.append(dato)
			return

		actual = self.prim
		i = 0
		while actual and (i < (posicion - 1)):
			actual = actual.prox
			i += 1

		nodo = _Nodo(dato)
		
		nodo.prox = actual.prox
		actual.prox = nodo

		self.len += 1

	def _borrar_prim(self):
		"""Elimina el primer elemento de la lista"""
		
		if self.len == 0:
			raise ValueError("La lista esta vacia")

		dato = self.prim.dato
		self.prim = self.prim.prox

		if not self.prim:
			self.ult = None

		self.len -= 1

		return dato
	
	def pop(self, posicion = None):
		"""Elimina el elemento de la posicion indicada, si no 
		se especifica una posicion, borra el ultimo elemento"""

		if (posicion == 0) or (self.len == 0):
			dato = self._borrar_prim()
			return dato

		if not posicion:
			posicion = self.len - 1

		actual = self.prim
		i = 0

		while actual and (i < posicion - 1):
			actual = actual.prox 
			i += 1

		dato = actual.prox.dato

		actual.prox = actual.prox.prox

		if posicion == self.len - 1:
			self.ult = actual

		self.len -= 1

		return dato

	def remove(self, item):
		"""Remueve la primera aparacion del item recibido en la lista"""

		if self.len == 0:
			raise ValueError("Lista vacia")

		if self.prim.dato == item:
			self._borrar_prim()
			return


		anterior = self.prim
		actual = anterior.prox

		while actual and actual.dato != item:
			anterior = anterior.prox
			actual = actual.prox

		if not actual:
			raise ValueError("El elemento no esta en la lista")

		if actual.prox == None:
			self.ult = anterior

		anterior.prox = actual.prox

		self.len -= 1 

	def index(self, item):
		"""Devuelve el indice (entero) del elemento recibido."""
		i = 0
		
		if self.prim.dato == item:
			return i

		actual = self.prim

		while actual and actual.dato != item:
			actual = actual.prox
			i += 1

		if not actual:
			raise ValueError("Elemento no encontrado")

		return i 
#-----------------------------------------------------------------------------------

class Pila():
	"""Clase que representa una pila."""
	def __init__(self):
		"""
		Crea una pila vacia.
		Atributos: items (lista de python vacia).
		"""
		self.items = []

	def esta_vacia(self):
		"""
		Evalua si no hay elementos en la pila. 
		Devuelve un booleano.
		"""
		return len(self.items) == 0

	def apilar(self, item):
		"""
		Pre: recibe un item.
		Post: apila este item en la lista.
		"""
		self.items.append(item)

	def desapilar(self):
		"""
		Desapila y devuelve el ultimo item ingresado en la pila.
		"""
		if self.esta_vacia():
			raise ValueError("La pila esta vacia.")
		return self.items.pop()

	def ver_tope(self):
		"""
		Imprime un representacion del ultimo iterm ingresado.
		"""
		
		if self.esta_vacia():
			raise ValueError("La pila esta vacia")
		
		return self.items[-1]
#-----------------------------------------------------------------------------------

class MarcaDeTiempo: #doc
	"""Representa una marca de tiempo que contiene canales en los cuales se habilitan
	o desabilitan los tracks."""
	def __init__(self, tiempo, canales):
		"""Crea una marca de tiempo con el tiempo de duracion y la cantidad 
		de canales indicado."""
		self.tiempo = tiempo
		self.tracks = []
		self.canales = int(canales) 
		for track in range(1, canales+1):
			self.tracks.append(False)

	def track_on(self, track):
		"""Habilita el numero de track de la marca de tiempo."""
		self.tracks[track] = True

	def track_off(self, track):
		"""Desabilita el numero de track de la marca de tiempo."""
		self.tracks[track] = False
#-----------------------------------------------------------------------------------

class Iterador: #doc. 
	"""Representa un iterador que va y vuelve."""
	def __init__(self, lista_enlazada):
		"""Crea un iterador para una lista enlazada que la puede recorrer 
		para atras y paar adelante.""" 
		self.lista = lista_enlazada
		self.anterior = None
		self.actual = lista_enlazada.prim
		self.pila_anteriores = Pila()

	def proximo(self):
		"""Pasa al siguiente elemento de la lista."""
		if not self.actual.prox:
			return self.actual#return self.actual??
		self.pila_anteriores.apilar(self.anterior)
		self.anterior = self.actual
		self.actual = self.actual.prox
		return self.actual

	def anterior(self):
		"""Vuelve al elemento anterior de la lista."""
		if self.pila_anteriores.esta_vacia():
			return self.actual#return self.actual??
		self.actual = self.anterior
		self.anterior = self.pila_anteriores.desapilar()
		return self.actual

	def insertar(self, dato):
		"""Inserta un elemento en la pocision actual del iterador."""
		if self.lista.len == 0 or self.anterior == None:
			 self.lista._insertar_prim(dato)
			 self.actual = self.lista.prim
			 return
		nodo = _Nodo(dato)
		self.anterior.prox = nodo
		nodo.prox = self.actual
		self.actual = nodo

#-----------------------------------------------------------------------------------

class Cursor: #doc
	"""Representa un cursor que recorre una lista enlazada..."""
	def __init__(self, lista):
		"""Crea el cursor."""
		self.lista = lista
		self.iterador = Iterador(lista)
		self.actual = lista.prim
		self.pocision = 0
		self.reproducor = Reproductor(lista)

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
		self.iterador.insertar(dato)
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

	def reproducir_actual(self):
		"""Reproduce la marca de tiempo en el que se encuentra el cursor."""
		marca_de_tiempo = self.actual
		self.reproducor.sonar(marca_de_tiempo)

	def reproducir_todo(self): #con un iterador "reciclable"
		"""Reproduce toda la cancion representada por la lista."""



#-----------------------------------------------------------------------------------


class Reproductor: #doc
	"""Representa un reproductor de sonidos."""
	def __init__(self, lista_de_tracks):
		"""Crea el reproductor de sonidos a partir de una lista de elementos de la 
		clase Track."""
		self.lista_tracks = lista_de_tracks

	def sonar(self, marca_tiempo):
		"""Reproduce los tracks habilitados en una marca de tiempo
		(la cual debe ser de la clase MarcaDeTiempo)."""
		tiempo = marca_tiempo.tiempo
		canales = marca_tiempo.canales
		for i in range(canales):
			estado_track = marca_tiempo.tracks[i]
			if estado_track:
				track = self.lista_tracks[i]
				sonido = track.sonido
				sp = pysounds.SoundPlayer(2)
				sp.play_sounds(sonido, tiempo)


