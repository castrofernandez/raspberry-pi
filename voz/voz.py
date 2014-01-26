from subprocess import call

piglow = PiGlow()

def hablar(texto):
    call(["mpg123", '-q "http://translate.google.com/translate_tts?tl=es&q=' + texto + '"'])
     
hablar(hola)
