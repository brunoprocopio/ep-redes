"""
Funções do servidor
Cuida do upload de arquivos
"""

from constants import *

class Server:

    def __init__(self, msg):
        try:
            # mensagem em bytes
            self.msg = msg

            # socket
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.connections = []

            # cria lista de peers
            self.peers = []

            # abre o socket
            self.s.bind((HOST, PORT))

            # escuta o socket
            self.s.listen(1)

            print("-" * 10 + " servidor iniciado " + "-" * 10)

            self.run()
        except Exception as e:
            sys.exit()

    
    """
    Envia os dados para os clients
    Fecha a conexão quando o client sai da sessão
    """
    def handler(self, socket_connection, address):
        try:
            while True:
                # server recebe a mensagem
                data = socket_connection.recv(BYTE_SIZE)
                for peer_connection in self.connections:

                    # sinal de desconexão enviado pelo peer
                    if data and data.decode('utf-8')[0].lower() == 'q':

                        # desconecta o peer
                        self.disconnect(c, address)
                        return
                    elif data and data.decode('utf-8') == REQUEST_STRING:
                        print("-" * 20 + " ENVIANDO " + "-" * 21)
                        # upload de arquivo
                        peer_connection.send(self.msg)
        except Exception as e:
            sys.exit()


    """
    Método para desconectar o peer
    """
    def disconnect(self, connection, address):
        self.connections.remove(connection)
        self.peers.remove(address)
        connection.close()
        self.send_peers()
        print("{} desconectado".format(address))
        print("-" * 50)



    """
    Método para executar o servidor
    Cria uma thread para cada client
    """
    def run(self):
        # sempre escuta as conexões
        while True:
            connection, address = self.s.accept()

            # salva na lista de peers
            self.peers.append(address)
            print("peers: {}".format(self.peers))
            self.send_peers()
            # cria uma thread para a conexão
            peer_thread = threading.Thread(target=self.handler, args=(connection, address))
            peer_thread.daemon = True
            peer_thread.start()
            self.connections.append(connection)
            print("{} conectado".format(address))
            print("-" * 50)


    """
    Atualiza a lista de peers para todos os peers
    """
    def send_peers(self):
        peers = ""
        for peer in self.peers:
            peers = peers + str(peer[0]) + ","

        for connection in self.connections:
            # adicionamos um byte '\x11' no começo da mensagem
            # para diferenciar se é uma mensagem normal ou se é uma atualização na lista de peers
            data = PEER_BYTE_DIFFERENTIATOR + bytes(peers, 'utf-8')
            connection.send(PEER_BYTE_DIFFERENTIATOR + bytes(peers, 'utf-8'))
