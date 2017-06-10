class Pila():
	"""
	Clase que representa una pila.
	"""
	def __init__(self):
		"""
		Crea una pila vacia.
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
			raise ValueError("Pila vacia.")
		return self.items.pop()

	def ver_tope(self):
		"""
		Devuelve el ultimo item ingresado.
		"""	
		if self.esta_vacia():
			raise ValueError("Pila vacia")	
		return self.items[len(self.items)-1]