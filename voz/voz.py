from subprocess import call

def hablar(texto):
    print texto
    call(["mpg123", '-q "http://translate.google.com/translate_tts?tl=es&q=' + texto + '"'])
     
hablar(hola)
