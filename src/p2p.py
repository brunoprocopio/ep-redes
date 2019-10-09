from constants import *
from client import *
from server import *


"""
Programa principal
cuida de agir como cliente e servidor quando necessário
"""
class p2p:
    # inicial como o peer default
    peers = ['127.0.0.1']


def main():
    msg = fileIO.convert_to_bytes()
    while True:
        try:
            print("-" * 20 + " conectando " + "-" * 20)
            # aguarda um tempo entre 1 e 5 segundos
            time.sleep(randint(RAND_TIME_START, RAND_TIME_END))
            for peer in p2p.peers:
                try:
                    client = Client(peer)
                except KeyboardInterrupt:
                    sys.exit(0)
                except:
                    pass

                # se transforma no servidor
                try:
                    server = Server(msg)
                except KeyboardInterrupt:
                    sys.exit()
                except:
                    pass

        except KeyboardInterrupt as e:
            sys.exit(0)


if __name__ == "__main__":
    main()
