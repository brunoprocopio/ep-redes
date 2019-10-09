"""
Funções do cliente
Cuida do download dos arquivos
"""

from constants import *

class Client:


    def __init__(self, address):
        # configura o socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # permite o python reutilizar um socket recentemente fechado
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # realiza a conexão
        self.s.connect((address, PORT))

        self.previous_data = None

        # realiza o trabalho em uma outra thread
        client_thread = threading.Thread(target=self.send_message)
        client_thread.daemon = True
        client_thread.start()

        # envia a mensagem

        while True:

            request_thread = threading.Thread(target=self.receive_message)
            request_thread.start()
            request_thread.join()

            data = self.receive_message()

            if not data:
                # erro no servidor
                print("-" * 20 + " erro no servidor " + "-" * 20)
                break

            elif data [0:1] == PEER_BYTE_DIFFERENTIATOR:
                # checa se o primeiro byte é para atualizar a lista de peers
                print("atualizando peers")
                self.update_peers(data[1:])


    """
    Escreve mensagens recebidas
    """
    def receive_message(self):
        try: 
            print("recebendo ----------")
            data = self.s.recv(BYTE_SIZE)

            print(data.decode("utf-8"))

            print("mensagem recebida pelo cliente:")

            if self.previous_data != data:
                fileIO.create_file(data)
                self.previous_data = data

            return data
        except KeyboardInterrupt:
            self.send_disconnect_signal()


    """
    Atualiza lista de peers
    """
    def update_peers(self, peers):
        # nossa lista é algo como 127.0.0.1, 192.168.1.1,
        # removemos o ultimo elemento, que seria None
        p2p.peers = str(peers, "utf-8").split(',')[:-1]

    
    """
    Envia a mensagem
    """
    def send_message(self):
        try:
            self.s.send(REQUEST_STRING.encode('utf-8'))
        except KeyboardInterrupt as e:
            self.send_disconnect_signal()
            return


    def send_disconnect_signal(self):
        print("desconectado")
        self.s.send("q".encode('utf-8'))
        sys.exit()
