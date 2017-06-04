import soundPlayer

FUNCIONES_SONIDO = {
	"noise": soundPlayer.SoundFactory.get_noise_sound ,
	"silence": soundPlayer.SoundFactory.get_silence_sound ,
	"sine": soundPlayer.SoundFactory.get_sine_sound ,
	"square": soundPlayer.SoundFactory.get_square_sound ,
	"triangular": soundPlayer.SoundFactory.get_triangular_sound ,
}

class Track():
	"""
	Clase que representa un track/pista de sonido
	"""

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
		"""
		Devuelve el sonido almacenado en el track.
		"""
		return self.sonido