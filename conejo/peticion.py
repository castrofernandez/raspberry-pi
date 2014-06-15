import sys, argparse
import rpyc

servidor = rpyc.connect("localhost", 12345)
c = servidor.root

ejemplo = "%s --serie 0019db9e9367 --boton 1 --rfid d0021a0353063b72" % sys.argv[0]

parser  = argparse.ArgumentParser( description=ejemplo )
parser.add_argument('--serie',   "-s", help = 'Numero de serie.', required = True )
parser.add_argument('--boton',   "-b", help = 'Boton pulsado. Si o no.', default = None )
parser.add_argument('--rfid',  "-r", help = 'RFID posicionado sobre nariz.', default = None )
args = parser.parse_args()

if not args.serie == None:
  print c.peticion(args.serie, args.boton, args.rfid)
else:
  print "Introduza numero de serie."
