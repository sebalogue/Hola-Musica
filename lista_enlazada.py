from pila import Pila

#-----------------------------------------------------------------------------------

class _Nodo():
	"""Clase que representa un elemento de lista enlazada"""
	
	def __init__(self, dato=None, prox=None):
		"""
		Pre: recibe un dato a almacenar, y una referencia al proximo Nodo.
		Post: su estado inicial, son estos dos atributos recibidos.
		"""
		self.dato = dato
		self.prox = prox

	def __str__(self):
		"""
		Devuelve una reprentacion (cadena) informal del Nodo.
		"""
		return str(self.dato)

	def __repr__(self):
		"""
		Devuelve una reprentacion (cadena) formal del Nodo.
		"""
		return str(self)
#-----------------------------------------------------------------------------------

class ListaEnlazada():
	"""
	Representa una lista de elementos enlazados
	"""
	def __init__(self):
		"""
		Inicia una lista enlazada vacia.
		"""
		self.prim = None
		self.len = 0

	def __len__(self):
		"""
		Devuelve el largo de la lista (entero).
		"""
		return self.len 
	
	def __str__(self):
		"""
		Devuelve una representacion en cadena de texto de la lista.
		"""		
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
		"""
		Devuelve un representacion formal en cadena de texto de la lista.
		"""
		return str(self)

	def insertar_primero(self, dato):
		"""
		Pre: recibe un dato cualquiera.
		Post: inserta un dato en la primera posicion.
		"""		
		nodo = _Nodo(dato)		
		if self.len == 0:
			self.prim = nodo
			self.len += 1
			return nodo
		nodo.prox = self.prim
		self.prim = nodo
		self.len += 1
		return nodo

	def insert(self, posicion, dato):
		"""
		Pre: recibe un dato cualquiera, y una posicion existente de la lista.
		Post: inserta un elemento en la posicion indicada
		"""	
		if posicion < 0 or posicion > self.len:
			raise IndexError("Indice fuera de rango")
		if posicion == 0:
			self.insertar_primero(dato)
			return
		actual = self.prim
		i = 0
		while actual and (i < posicion):
			actual = actual.prox
			i += 1
		nodo = _Nodo(dato)
		nodo.prox = actual.prox
		actual.prox = nodo
		self.len += 1

	def append(self, dato):
		"""
		Inserta un dato al final de la lista.
		"""
		self.insert(self.len, dato)

	def borrar_primero(self):
		"""
		Elimina el primer elemento de la lista.
		"""		
		if self.len == 0:
			raise ValueError("Lista vacia")
		dato = self.prim.dato
		self.prim = self.prim.prox
		self.len -= 1
		return dato
	
	def pop(self, posicion = None):
		"""
		Elimina el elemento de la posicion indicada (entero), si no 
		se especifica una posicion, borra el ultimo elemento
		"""
		if posicion is None:
			posicion = self.len - 1
		if (posicion < 0) or (posicion >= self.len):
			raise IndexError("Indice fuera de rango")
		if (posicion == 0) or (self.len == 0):
			dato = self.borrar_primero()
			return dato
		anterior = self.prim
		actual = self.prim.prox
		i = 0
		while actual.prox and (i < posicion):
			anterior = actual
			actual = actual.prox 
			i += 1
		anterior.prox = actual.prox
		self.len -= 1
		return dato

	def remove(self, item):
		"""
		Remueve la primera aparacion del item recibido en la lista
		"""
		if self.len == 0:
			raise ValueError("Lista vacia")
		if self.prim.dato == item:
			self.borrar_primero()
			return
		anterior = self.prim
		actual = anterior.prox
		while actual and actual.dato != item:
			anterior = anterior.prox
			actual = actual.prox
		if not actual:
			raise ValueError("Elemento no encontrado")
		anterior.prox = actual.prox
		self.len -= 1 

	def index(self, item):
		"""
		Devuelve el indice (entero) del elemento recibido.
		"""
		i = 0		
		if not self.len:
			raise ValueError("Lista vacia")
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

class IteradorListaEnlazada: 
	"""
	Representa un iterador que puede recorrer una lista enlazada
	tanto avanzando como retrocediendo.
	"""
	def __init__(self, lista_enlazada):
		"""
		Crea un iterador para una lista enlazada.
		Pre: recibe una lista enlazada.
		""" 
		self.lista = lista_enlazada
		self.anterior = None 
		self.actual = lista_enlazada.prim
		self.pila_anteriores = Pila()
		self.posicion = 0

	def elemento_actual(self):
		"""
		Devuelve el elemento actual.
		"""
		if not self.actual:
			return None
		return self.actual.dato

	def avanzar(self):
		"""
		Pasa al siguiente elemento de la lista.
		"""
		if (not len(self.lista)) or (not self.actual.prox): 
			raise StopIteration("No hay elementos en la lista.")
		self.pila_anteriores.apilar(self.anterior)
		self.anterior = self.actual
		self.actual = self.actual.prox
		self.posicion += 1
		return self.actual.dato

	def retroceder(self):
		"""
		Vuelve al elemento anterior de la lista.
		"""
		if self.pila_anteriores.esta_vacia(): 
			raise StopIteration("No hay mas elementos en la lista.")
		self.actual = self.anterior
		self.anterior = self.pila_anteriores.desapilar()
		self.posicion -= 1
		return self.actual.dato

	def insertar(self, dato):
		"""
		Inserta un elemento en la posicion actual del iterador.
		"""
		if self.posicion == 0:
			self.lista.insertar_primero(dato) 
			self.actual = self.lista.prim 
			return self.actual.dato
		nodo = _Nodo(dato)
		self.anterior.prox = nodo
		nodo.prox = self.actual
		self.actual = nodo
		self.lista.len += 1
	
	def insertar_ultimo(self, dato):
		"""
		Pre: Debe encontrarse el la ultima posicion de la lista enlazada.
		Post: Inserta un elemento al final de las lista (despues del ultimo elemento).
		"""
		if not self.actual:
			raise ValueError("Lista Vacia.")
		if self.actual.prox:
			raise IndexError("Aun hay elementos adelante.")
		nodo = _Nodo(dato)
		self.actual.prox = nodo
		self.lista.len += 1

	def insertar_principio(self, dato):
		"""
		Pre: la lista no esta vacia. y nos encontramos al principio de la misma.
		Post: Inserta un elemento al principio de la lista
		"""
		if not self.actual:
			raise ValueError("Lista vacia")
		if not (self.posicion == 0):
			raise IndexError("Este no es el principio de la lista")
		self.anterior = self.lista.insertar_primero(dato)
		self.pila_anteriores.apilar(None)
		self.posicion += 1