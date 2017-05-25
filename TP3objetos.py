import soundPlayer
#-----------------------------------------------------------------------------------


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
		"""
		Posee 2 atributos que hacen referencia al primer elemento de 
		la lista, y al largo de la misma.
		Inicia con estas referencia en None y 0, respectivamente.
		"""
		self.prim = None
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

	def _insertar_prim(self, dato):
		"""Inserta un dato en la primera posicion"""		
		nodo = _Nodo(dato)		
		if self.len == 0:
			self.prim = nodo
			self.len += 1
			return
		nodo.prox = self.prim
		self.prim = nodo
		self.len += 1

	def insert(self, posicion, dato):
		"""Inserta un elemento en la posicion indicada"""	
		if posicion < 0 or posicion > self.len:
			raise IndexError("Indice fuera de rango")
		if posicion == 0 or self.len == 0:
			self._insertar_prim(dato)
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

	def append(self, dato):
		self.insert(self.len, dato)

	def _borrar_prim(self):
		"""Elimina el primer elemento de la lista"""		
		if self.len == 0:
			raise ValueError("Lista vacia")
		dato = self.prim.dato
		self.prim = self.prim.prox
		self.len -= 1
		return dato
	
	def pop(self, posicion = None):
		"""Elimina el elemento de la posicion indicada, si no 
		se especifica una posicion, borra el ultimo elemento"""
		if posicion is None:
			posicion = self.len - 1
		if (posicion < 0) or (posicion >= self.len):
			raise IndexError("Indice fuera de rango")
		if (posicion == 0) or (self.len == 0):
			dato = self._borrar_prim()
			return dato
		actual = self.prim
		i = 0
		while actual and (i < posicion - 1):
			actual = actual.prox 
			i += 1
		dato = actual.prox.dato
		actual.prox = actual.prox.prox
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
			raise ValueError("Elemento no encontrado")
		anterior.prox = actual.prox
		self.len -= 1 

	def index(self, item):
		"""Devuelve el indice (entero) del elemento recibido."""
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
			raise ValueError("Pila vacia.")
		return self.items.pop()

	def ver_tope(self):
		"""
		Imprime un representacion del ultimo iterm ingresado.
		"""	
		if self.esta_vacia():
			raise ValueError("Pila vacia")
		
		return self.items[-1]
#-----------------------------------------------------------------------------------


class Cola():
	"""Clase que representa una cola representa una cola."""
	def __init__(self):
		"""Crea  una cola vacia"""
		self.primero = None
		self.ultimo = None

	def esta_vacia(self):
		"""
		Devuelve True si la cola esta vacia, 
		False en caso contrario.
		"""
		return (self.primero is None)

	def encolar(self, dato):
		"""Encola el dato recicido."""
		nodo = _Nodo(dato)
		if self.ultimo:
			self.ultimo.prox = nodo
			self.ultimo = nodo
			return
		self.primero = nodo
		self.ultimo = nodo

	def desencolar(self):
		"""
		Desencola el primer elemento de 
		la cola y devuelve su valor.
		"""		
		if self.esta_vacia():
			raise ValueError("Cola vacia")
		dato = self.primero.dato		
		self.primero = self.primero.prox
		if not self.primero:
			self.ultimo = None		
		return dato

	def ver_primero(self):
		"""Devuelve el primer elemento de la cola"""
		if self.esta_vacia():
			raise ValueError("Cola vacia")
		return self.primero.dato
#-----------------------------------------------------------------------------------


class MarcaDeTiempo: #doc
	"""Representa una marca de tiempo que contiene canales en los cuales se habilitan
	o desabilitan los tracks."""
	def __init__(self, tiempo, canales):
		"""Crea una marca de tiempo con el tiempo de duracion y la cantidad 
		de canales indicado."""
		self.tiempo = float(tiempo)
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

	def tracks_habilitados(self):
		"""Devuelve los numeros de los tracks habilitados en la marca de tiempo.""" 
		return [num for num, track in enumerate(lista) if track]

	def dar_tiempo(self):
		"""Devuelve el tiempo de duracion de la marca de tiempo."""
		return self.tiempo


#-----------------------------------------------------------------------------------


class IteradorListaEnlazada: #doc. 
	"""Representa un iterador que va y vuelve."""
	def __init__(self, lista_enlazada):
		"""Crea un iterador para una lista enlazada que la puede recorrer 
		para atras y para adelante.""" 
		self.lista = lista_enlazada
		self.anterior = None
		self.actual = lista_enlazada.prim
		self.pila_anteriores = Pila()

	def elemento_actual(self):
		"""Devuelve el elemento actual"""
		return self.actual.dato

	def avanzar(self):
		"""Pasa al siguiente elemento de la lista."""
		if not self.lista.len:
			raise ValueError("Lista Vacia")
		if not self.actual.prox:
			raise StopIteration("Fin de la lista")
		self.pila_anteriores.apilar(self.anterior)
		self.anterior = self.actual
		self.actual = self.actual.prox
		dato = self.actual.dato
		return dato

	def retroceder(self):
		"""Vuelve al elemento anterior de la lista."""
		if not self.lista.len:
			raise ValueError("Lista Vacia")
		if self.anterior is None:
			raise StopIteration("Principio de la lista")
		self.actual = self.anterior
		dato = self.anterior.dato
		self.anterior = self.pila_anteriores.desapilar()
		return dato

	def insertar(self, dato):
		"""Inserta un elemento en la posicion actual del iterador."""
		if (self.lista.len == 0) or (self.anterior == None):
			self.lista._insertar_prim(dato)
			self.actual = self.lista.prim
			return
		nodo = _Nodo(dato)
		self.anterior.prox = nodo
		nodo.prox = self.actual
		self.actual = nodo
		self.lista.len += 1

#-----------------------------------------------------------------------------------


class Cursor: #doc
	"""Representa un cursor que recorre las marcas de tiempo de una cancion"""
	def __init__(self, cancion):
		"""Crea el cursor."""
		self.lista = cancion #Solucionar
		self.iterador = IteradorListaEnlazada(cancion)
		self.actual = self.iterador.elemento_actual()
		self.posicion = 0
		self.reproductor = Reproductor(cancion) #Solucionar

	def step(n = 1):
		"""Avanza n veces por la lista."""
		n = int(n)
		for veces in range(n):
			self.actual = self.iterador.avanzar()
			if self.posicion < self.lista.len:
				self.posicion += 1

	def back(n = 1):
		"""Retrocede al anterior elemento de la lista."""
		n = int(n)
		for veces in range(n):
			self.actual = self.iterador.retroceder()
			if self.posicion > 0:
				self.posicion -= 1

	def mark_add(self, duracion):
		"""Agrega una marca de tiempo en la posicion actual del cursor
		con la duracion indicada."""
		canales = self.actual.canales
		dato = MarcaDeTiempo(duracion, canales)
		self.iterador.insertar(dato)
		self.actual = self.iterador.avanzar()

	def mark_add_next(self, duracion):
		"""Agrega una marca de tiempo en la posicion siguiente del cursor
		con la duracion indicada."""
		self.actual = self.iterador.avanzar()
		mark_add(duracion)
		self.actual = self.iterador.retroceder()

	def mark_add_prev(self, duracion):
		"""Agrega una marca de tiempo en la posicion anterior del cursor
		con la duracion indicada."""
		self.actual = self.iterador.retroceder()
		mark_add(duracion)
		self.actual = self.iterador.avanzar()

	def reproducir_marca(self, marca = None):
		"""Reproduce la marca de tiempo en el que se encuentra el cursor."""
		marca_de_tiempo = marca
		if marca is None:
			marca_de_tiempo = self.actual
		habilitados = marca_de_tiempo.tracks_habilitados() #solucionar 
		tiempo = marca_de_tiempo.dar_tiempo()			   #Los tracks hablitados no le dan al reproductor los sonidos 
		self.reproductor.sonar(tiempo, habilitados)		   #sacar de la clase principal(a crear)

	def reproducir_todo(self):
		"""Reproduce toda la cancion representada por la lista."""
		marca_de_tiempo = self.lista.prim
		while marca_de_tiempo:
			reproducir_marca(marca_de_tiempo)
			marca_de_tiempo = marca_de_tiempo.prox

	def reproducir_hasta(self, marca):
		"""Reproduce desde la marca de tiempo actual hasta la marca dada por parametro."""
		marca_actual = self.actual
		pos_actual = self.pocision
		if marca < pos_actual:
			return
		i = 0
		while i =< marca and marca_actual:
			reproducir_marca(marca_actual)
			marca_actual = marca_actual.prox
			i += 1
	def reproducir_segundos(self, segundos):
		"""Reproduce los proximos segundos dados por parametro 
		desde la posicion actual del cursor."""
		marca_actual = self.actual
		tiempo_marca = marca_actual.dar_tiempo()
		segundos = float(segundos)
		while segundos >= tiempo_marca and marca_actual:
			reproducir_marca(marca_actual)
			marca_actual = marca_actual.prox
			tiempo_marca = marca_actual.dar_tiempo()
			segundos -= tiempo_marca



#-----------------------------------------------------------------------------------

class Reproductor: #doc
	"""Representa un reproductor de sonidos."""
	def __init__(self, lista_de_tracks):
		"""Crea el reproductor de sonidos a partir de una lista de elementos de la 
		clase Track."""
		self.lista_tracks = lista_de_tracks

	def sonar(self, tiempo, canales):
		"""
		Pre: recibe un tiempo en segundos, y la cantidad de canales (ambos enteros).
		Post: reproduce los tracks en el tiempo dado.
		"""
		tiempo = float(tiempo) 
		canales = int(canales)
		sp = soundPlayer.SoundPlayer(canales)
		sp.play_sounds(self.lista_tracks, tiempo)
#-----------------------------------------------------------------------------------


FUNCIONES_SONIDO = {
	"noise": soundPlayer.SoundFactory.get_noise_sound ,
	"silence": soundPlayer.SoundFactory.get_silence_sound ,
	"sine": soundPlayer.SoundFactory.get_sine_sound ,
	"square": soundPlayer.SoundFactory.get_square_sound ,
	"triangular": soundPlayer.SoundFactory.get_triangular_sound ,
}

class Track():
	"""Clase que representa un track/pista de sonido"""

	def __init__(self, funcion_sonido, frecuencia, volumen, duty_cycle=0.5):
		"""
		Pre: recibe una funcion perteneciente al diccionario de funciones 
		de sonido, una frecuencia (entero), volumen (entero) y un ciclo de 
		trabajo(entero, parametro opcional).
		Post: la clase track inicia con atributo que corresponde aun sonido 
		creado por la funcion a traves de los parametros.
		"""
		frecuencia = int(frecuencia)
		volumen = float(volumen)	
		if not funcion_sonido in FUNCIONES_SONIDO:
			raise ValueError("Funcion invalida")
		if funcion_sonido == "square":
			duty_cycle = int(duty_cycle)
			self.sonido = FUNCIONES_SONIDO[funcion_sonido](frecuencia, volumen, duty_cycle)
			return
		self.sonido = FUNCIONES_SONIDO[funcion_sonido](frecuencia, volumen)
	
	def devolver_sonido(self):
		"""Devuelve el sonido almacenado en el track"""
		return self.sonido
#-----------------------------------------------------------------------------------
