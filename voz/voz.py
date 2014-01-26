from subprocess import call

def hablar(texto):
    print texto
    url = "http://translate.google.com/translate_tts?tl=es&q=" + texto
    call(["mpg123", "-q", url])
     
hablar("hola")
