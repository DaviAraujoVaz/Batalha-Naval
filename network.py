import socket
import threading

class NetworkManager:
    def __init__(self, message_callback):
        self.sock = None
        self.target_ip = None
        self.target_port = None
        self.callback = message_callback
        self.listening = False

    def start_listening(self, local_port):
        if self.listening:
            self.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.sock.bind(('0.0.0.0', local_port))
        except OSError as e:
            self.sock.close()
            self.sock = None
            raise e

        self.listening = True
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()

    def set_target(self, ip, port):
        self.target_ip = ip
        self.target_port = port

    def send_message(self, msg):
        if self.target_ip and self.target_port and self.sock:
            try:
                self.sock.sendto(msg.encode('utf-8'), (self.target_ip, self.target_port))
            except Exception as e:
                print(f"Error sending message: {e}")

    def _listen(self):
        while self.listening:
            try:
                data, addr = self.sock.recvfrom(4096)
                if data:
                    msg = data.decode('utf-8')
                    # Aprende o endereço alvo se for o Host (não configurou target antes)
                    if self.target_ip is None:
                        self.target_ip = addr[0]
                        self.target_port = addr[1]
                        
                    # Somente processa se veio do target configurado
                    if addr[0] == self.target_ip and addr[1] == self.target_port:
                        # Repassa para o callback processar a mensagem
                        self.callback(msg)
            except Exception as e:
                if self.listening:
                    print(f"UDP Listen Error: {e}")
                
    def close(self):
        self.listening = False
        if self.sock:
            self.sock.close()
            self.sock = None
