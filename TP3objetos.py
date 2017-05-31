import soundPlayer
import csv
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


class MarcaDeTiempo: #doc
	"""Representa una marca de tiempo que contiene canales en los cuales se habilitan
	o desabilitan los tracks."""
	def __init__(self, tiempo, canales):
		"""Crea una marca de tiempo con el tiempo de duracion, la cantidad 
		de canales indicado, y con una lista de tracks habilitados."""
		self.tiempo = float(tiempo)
		self.canales = int(canales) 
		self.tracks = []
		for track in range(canales):
			self.tracks.append(False)

	def track_on(self, track):
		"""Habilita el numero de track de la marca de tiempo."""
		self.tracks[track] = True

	def track_off(self, track):
		"""Desabilita el numero de track de la marca de tiempo."""
		self.tracks[track] = False
	
	def track_add(self):
		"""
		Agrega un nuevo track deshabiltado al final de la lista.
		"""
		self.tracks.append(False)
		self.canales += 1

	def track_del(self, posicion_de_track):
		"""
		Elimina el track en la posicion indicada.
		Posicion de track deber ser un numero entero, y con un track asociodo.
		"""
		posicion = int(posicion_de_track)
		self.tracks.pop(posicion)
		self.canales -= 1

	def tracks_habilitados(self):
		"""Devuelve los numeros de los tracks habilitados en la marca de tiempo.""" 
		return [num for num, track in enumerate(self.tracks) if track]

	def dar_tiempo(self):
		"""Devuelve el tiempo de duracion de la marca de tiempo."""
		return self.tiempo

	def dar_tiempo_y_habilitados(self):
		"""Devuelve una tupla con el tiempo y los tracks habilitados de la marca de tiempo."""
		tiempo_y_habilitados = (self.dar_tiempo(), self.tracks_habilitados())
		return tiempo_y_habilitados

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
		frecuencia = float(frecuencia)
		volumen = float(volumen)	
		if not funcion_sonido in FUNCIONES_SONIDO:
			raise ValueError("Funcion invalida")
		if funcion_sonido == "square":
			duty_cycle = int(duty_cycle)
			self.sonido = FUNCIONES_SONIDO[funcion_sonido](frecuencia, volumen, duty_cycle)
			return
		self.sonido = FUNCIONES_SONIDO[funcion_sonido](frecuencia, volumen)
	
	def dar_sonido(self):
		"""Devuelve el sonido almacenado en el track"""
		return self.sonido
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

	def esta_vacia(self):
		"""
		Devuelve True si la lista esta vacia. 
		False en caso contrario.
		"""
		return self.lista.len == 0

	def elemento_actual(self):
		"""Devuelve el elemento actual"""
		if not self.actual:
			return None
		return self.actual.dato

	def avanzar(self):
		"""Pasa al siguiente elemento de la lista."""
		if self.esta_vacia() or not self.actual.prox:
			return
		self.pila_anteriores.apilar(self.anterior)
		self.anterior = self.actual
		self.actual = self.actual.prox
		return self.actual.dato

	def retroceder(self):
		"""Vuelve al elemento anterior de la lista."""
		if self.esta_vacia() or self.pila_anteriores.esta_vacia(): #raise o return solo?
			return
		self.actual = self.anterior
		self.anterior = self.pila_anteriores.desapilar()
		return self.actual.dato

	def insertar(self, dato):
		"""Inserta un elemento en la posicion actual del iterador."""
		if self.lista.len <= 1:
			self.lista._insertar_prim(dato)
			self.actual = self.lista.prim
			self.lista.len += 1
			return
		nodo = _Nodo(dato)
		self.anterior.prox = nodo
		nodo.prox = self.actual
		self.actual = nodo
		self.lista.len += 1
	
	def _insertar_ultimo(self, dato):
		"""
		Pre: Debe encontrarse el la ultima posicion de la lista enlazada.
		Post: Inserta un elemento al final de las lista (despues del ultimo elemento).
		"""
		if not self.actual:
			raise ValueError("Lista Vacia")
		if self.actual.prox:
			raise IndexError("Aun hay elementos adelante")
		nodo = _Nodo(dato)
		self.actual.prox = nodo
		self.lista.len += 1

#-----------------------------------------------------------------------------------


class Cursor:
	"""Representa un cursor que recorre las marcas de tiempo de una cancion"""
	def __init__(self, reproductor):
		"""Crea el cursor."""
		self.cancion = self.reproductor.dar_cancion()
		self.iterador = IteradorListaEnlazada(self.cancion)
		self.posicion = 0
		self.actual = self.iterador.elemento_actual()

	def step(self, n = 1):
		"""Avanza n veces por la lista."""
		n = int(n)
		if not len(self.cancion):
			raise ValueError("Cancion vacia.")
		if self.posicion == (len(self.cancion) - 1):
			raise StopIteration("Fin de la cancion.")
		for veces in range(n):
			self.actual = self.iterador.avanzar()
			if self.posicion < self.cancion.len:
				self.posicion += 1

	def back(self, n = 1):
		"""Retrocede al anterior elemento de la lista."""
		n = int(n)
		if not len(self.cancion):
			raise ValueError("Cancion vacia.")
		if self.posicion == 0:
			raise StopIteration("Principio de la cancion.")
		for veces in range(n):
			self.actual = self.iterador.retroceder()
			if self.posicion > 0:
				self.posicion -= 1
	
	def track_add(self):
		"""
		Recorre toda la cancion agregando un nuevo track deshabilitado
		a las marcas de tiempo.
		"""
		while self.actual:
			self.actual.track_add()
			self.actual = self.iterador.avanzar()

	def track_del(self, posicion_de_track):
		"""
		Recorre todo la cancion eliminando de las marcas de tiempo, 
		el track en la posicion indicada.
		"""
		posicion = int(posicion_de_track)
		while self.actual:
			self.actual.track_del(posicion)
			self.actual = self.iterador.avanzar()

	def track_obtener(self):
		"""Devuelve una lista de listas, de tiempo y tracks habilitados(lista)
		de toda la cancion desde la posicion actual."""
		marca_tiempo = self.actual
		tiempos_y_tracks = []
		while marca_tiempo:
			tiempos_y_tracks.append(marca_tiempo.dar_tiempo_y_habilitados())
			marca_tiempo = self.iterador.avanzar()
		return tiempos_y_tracks

	def mark_add(self, duracion, canales):
		"""
		Agrega una marca de tiempo en la posicion actual del cursor
		con la duracion indicada.
		"""
		canales = int(canales)
		dato = MarcaDeTiempo(duracion, canales)
		self.iterador.insertar(dato)
		self.actual = dato

	def mark_add_next(self, duracion, canales):
		"""
		Agrega una marca de tiempo en la posicion siguiente del cursor
		con la duracion indicada.
		"""
		if  not self.actual or self.posicion == (len(self.cancion) - 1):
			dato = MarcaDeTiempo(float(duracion), self.canales)
			self.iterador._insertar_ultimo(dato)
			return
		self.actual = self.iterador.avanzar()	
		self.mark_add(float(duracion))
		self.actual = self.iterador.retroceder()

	def mark_add_prev(self, duracion, canales):
		"""
		Agrega una marca de tiempo en la posicion anterior del cursor
		con la duracion indicada.
		"""
		if self.posicion == 0:
			mark_add(float(duracion))
			self.avanzar()
			return
		self.actual = self.iterador.retroceder()
		mark_add(float(duracion))
		self.actual = self.iterador.avanzar()

	def activar_track(self, numero_track):
		"""
		Activa el numero de track de la marca 
		de tiempo en la cual esta el cursor.
		"""
		self.actual.track_on(int(numero_track))

	def desactivar_track(self, numero_track):
		"""
		Desactiva el numero de track de la marca 
		de tiempo en la cual esta el cursor.
		"""
		self.actual.track_off(int(numero_track))

	def obtener_marca(self):
		"""Devuelve la marca de tiempo en el que se encuentra el cursor."""
		if not self.actual:
			raise ValueError("Cancion vacia.")
		return [self.actual.dar_tiempo_y_habilitados()]			   
				   

	def reproducir_todo(self):
		"""Reproduce toda la cancion representada por la lista."""
		iterador_auxiliar
		marca_actual =  self.cancion.prim
		cancion = []
		while marca_de_tiempo:
			cancion.append(marca_de_tiempo.dato.dar_tiempo_y_habilitados())
			marca_de_tiempo = marca_de_tiempo.prox
		self.reproductor.reproducir(cancion)

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
			raise ValueError("Marca deber ser mayor a 1.")
		if posicion + marca > len(self.cancion):
			raise ValueError("No hay tantas marcas desde esta posicion") 
		
		marca_actual = self.actual
		iterador_auxiliar = IteradorListaEnlazada(self.cancion)
		for _ in range(self.posicion):
			iterador_auxiliar.avanzar()
		
		if not marca_actual:
			raise ValueError("Cancion vacia.")

		i = 0
		tiempos_y_tracks = []
		while marca_actual and (i < marca): 
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
			marca_actual = iterador_auxiliar.avanzar()
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
		for _ in range(self.posicion):
			iterador_auxiliar.avanzar()
		
		tiempo_marca = marca_actual.dar_tiempo()
		tiempos_y_tracks = []
		while marca_actual and segundos >= tiempo_marca: 
			tiempos_y_tracks.append(marca_actual.dar_tiempo_y_habilitados())
			marca_actual = iterador_auxiliar.avanzar()
			tiempo_marca = marca_actual.dar_tiempo()
			segundos -= tiempo_marca
		return tiempos_y_tracks
#-----------------------------------------------------------------------------------

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
		self.cursor = Cursor(self) 

	def dar_cancion(self):
		"""Devuevlve la cancion cargada"""
		return self.cancion

	def step(self, pasos = 1):
		"""
		Pre: Recibe una cantidad de pasos a avanzar en la linea de tiempo 
		de la cancion. Pasos es una entero mayor a cero. (por defecto es 1).
		Post: avanza tantos pasos en la cancion.
		"""
		pasos = int(pasos)
		if pasos < 1:
			raise ValueError("No puede avanzar menos de un paso.")
		self.cursor.step(pasos)
	
	def back(self, pasos = 1):
		"""
		Pre: Recibe una cantidad de pasos a retrroceder en la linea de 
		tiempo de la cancion. Pasos es un entero mayor a cero (por defecto 
		es 1).
		Post retrocede tantos pasos en la cancion.
		"""
		pasos = int(pasos)
		if pasos < 1:
			raise ValueError("No puede retroceder menos de un paso")
		self.cursor.back(pasos)

	def mark_add(self, tiempo):
		"""
		Pre: recibe un tiempo (numero) mayor a cero.
		Post: Agrega una nueva marca de tiempo en las posicion actual del 
		cursor.
		"""
		tiempo = float(tiempo)
		if tiempo <= 0:
			raise ValueError("Tiempo debe ser un numero mayor a cero.")
		self.cursor.mark_add(tiempo, self.canales)

	def mark_add_next(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal) mayor a cero.
		Post: Agrega una nueva marca de tiempo un paso adelante de la 
		posicion actual del cursor.
		"""
		tiempo = float(tiempo)
		if tiempo <= 0:
			raise ValueError("Tiempo debe ser un numero mayor a cero.")
		self.cursor.mark_add_next(tiempo, self.canales)

	def mark_add_prev(self, tiempo):
		"""
		Pre: recibe un tiempo (entero o decimal) mayor a cero.
		Post Agrega una nueva marca de tiempo un paso atras de la posicion 
		actual del cursor 
		"""
		tiempo = int(tiempo)
		if tiempo <= 0:
			raise ValueError("Tiempo deber ser un numero mayor a cero.")
		self.cursor.mark_add_prev(tiempo, self.canales)

	def track_add(self, funcion_sonido, frecuencia, volumen): #porque cursor_auxiliar? no lo tendria que agregar al self.cursor?
		"""Crea y agrega un nuevo track."""
		duty_cycle = 0.15
		track = Track(funcion_sonido, frecuencia, volumen, duty_cycle)
		self.tracks.append(track.dar_sonido())
		self.info.append([funcion_sonido.upper(), frecuencia, volumen])
		self.canales += 1
		cursor_auxiliar = Cursor(self)
		cursor_auxiliar.track_add()

	def track_del(self, posicion): #aca tambien por que otro cursor? 
		"""
		Elimina el track de la posicion indicada.
		Posicion es un entero.
		"""
		posicion = int(posicion)
		self.tracks.pop(posicion-1)
		self.info.pop(posicion-1)
		self.canales -= 1
		cursor_auxiliar = Cursor(cancion)
		cursor_auxiliar.track_del(posicion-1)

	def track_on(self, indice_de_track):
		"""
		Pre: recibe el indice (entero) del track a activar. 
		Indice es mayor cero, y menor o igual a la cantidad de canales.  
		Post: activa el track en la posicion actual del cursor.
		"""
		indice = int(indice_de_track)
		if (indice < 0) or (indice > self.canales - 1):
			raise IndexError("No existe track en este indice.")
		self.cursor.activar_track(indice)

	def track_off(self, indice_de_track):
		"""
		Pre: recibe el indice (entero) del track a activar. 
		Indice es mayor cero, y menor o igual a la cantidad de canales.  
		Post: activa el track en la posicion actual del cursor.
		"""
		indice = int(indice_de_track)
		if (indice < 0) or (indice < self.canales - 1):
			raise IndexError("No existe track en este indice.")
		self.cursor.desactivar_track(indice)

	def sonar(self, tiempo, lista_de_tracks):
		"""
		Pre: recibe un tiempo en segundos, y la cantidad de canales (ambos enteros).
		Post: reproduce los tracks en el tiempo dado.
		"""
		tiempo = float(tiempo) 
		canales = self.canales # NUEVA ACTUALIZACION
		sp = soundPlayer.SoundPlayer(canales)
		sp.play_sounds(lista_de_tracks, tiempo)

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
		tiempos_y_sonidos = [] 
		
		for tiempo_y_habilitado in tiempos_y_habilitados:
			tiempo_A = tiempo_y_habilitado[0]
			sonidos_A = self.obtener_sonidos(tiempo_y_habilitado[1])
			tiempos_y_sonidos.append((tiempo_A, sonidos_A))
		
		for tiempo_y_sonido in tiempos_y_sonidos:
			tiempo_B = tiempo_y_sonido[0]
			sonidos_B = tiempo_y_sonido[1] 
			self.sonar(tiempo_B, sonidos_B)

	def store(self, nombre_de_archivo):
		"""
		Convierte la cancion (lista enlazada) en un archivo.plp.
		"""
		nombre = str(nombre_de_archivo)
		cursor_auxiliar = Cursor(self.cancion)
		tiempos_y_tracks = cursor_auxiliar.track_obtener()
		tiempo_anterior = None
		
		with open(nombre + ".plp", 'w') as _archivo:
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

	def load(self, cancion):
		"""
		Carga una cancion al reproductor.
		Cancion es un archivo.plp con formato de cancion.
		"""
		steps = 0
		with open(cancion) as _cancion:
			lector = csv.reader(_cancion, delimiter = ",")
			linea = next(lector, None)
			tiempo_anterior = None
			while linea:
				indice = linea[0]
				datos = linea[1]
				
				if indice == "C":
					self.canales = int(datos)
					self.cursor.canales = int(datos) #No dejar asi, buscar alternativa mas correcta 
				
				if indice == "S":
					info = datos.split("|")
					funcion, frecuencia, volumen = info
					self.track_add(funcion.lower(), int(frecuencia), float(volumen))

				if indice == "T":
					tiempo = float(datos)
					if tiempo != tiempo_anterior:
						tiempo_anterior = tiempo
				
				if indice == "N":
					try:
						self.cursor.mark_add_next(tiempo_anterior)
						self.cursor.step()
						steps += 1
					except ValueError:
						self.cursor.mark_add(tiempo_anterior)
					lista_de_tracks = list(datos)
					contador = 0
					for track in lista_de_tracks:
						if track == "#":
							self.cursor.activar_track(contador)
						contador += 1
				linea = next(lector, None)
					
		self.cursor.back(steps)



			

