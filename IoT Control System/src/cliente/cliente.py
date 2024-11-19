import socket
import json
import logging
from typing import Dict, Any

class ClienteIoT:
    def __init__(self, host: str = "127.0.0.1", port: int = 10418):
        self.host = host
        self.port = port
        self.sock = None
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def conectar(self):
        """Estabelece conexão com o servidor"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.logger.info(f"Conectado ao servidor {self.host}:{self.port}")
        except Exception as e:
            self.logger.error(f"Erro ao conectar: {e}")
            raise

    def enviar_comando(self, comando: Dict[str, Any]) -> Dict[str, Any]:
        """Envia um comando para o servidor e recebe a resposta"""
        try:
            self.sock.send(json.dumps(comando).encode('utf-8'))
            resposta = self.sock.recv(1024).decode('utf-8')
            return json.loads(resposta)
        except Exception as e:
            self.logger.error(f"Erro ao enviar comando: {e}")
            return {"status": "erro", "mensagem": str(e)}

    def menu_principal(self):
        """Interface do usuário"""
        dispositivos = ["luz_sala", "luz_quarto", "luz_cozinha", "todos"]
        
        while True:
            print("\n=== Sistema de Controle IoT ===")
            print("1. Ligar dispositivo")
            print("2. Desligar dispositivo")
            print("3. Verificar status")
            print("4. Ligar TODOS dispositivos")
            print("5. Desligar TODOS dispositivos")
            print("6. Status TODOS dispositivos")
            print("7. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "7":
                break
                
            if opcao in ["4", "5", "6"]:
                comando = {
                    "dispositivo": "todos",
                    "acao": {
                        "4": "LIGAR",
                        "5": "DESLIGAR",
                        "6": "STATUS"
                    }[opcao]
                }
                resposta = self.enviar_comando(comando)
                if isinstance(resposta.get('estado'), dict):
                    print("\nStatus dos dispositivos:")
                    for disp, estado in resposta['estado'].items():
                        print(f"{disp}: {'Ligado' if estado else 'Desligado'}")
                else:
                    print(f"\nResposta: {resposta['mensagem']}")
                
            elif opcao in ["1", "2", "3"]:
                print("\nDispositivos disponíveis:")
                for i, disp in enumerate(dispositivos, 1):
                    print(f"{i}. {disp}")
                    
                try:
                    idx = int(input("Escolha o dispositivo: ")) - 1
                    dispositivo = dispositivos[idx]
                    
                    comando = {
                        "dispositivo": dispositivo,
                        "acao": {
                            "1": "LIGAR",
                            "2": "DESLIGAR",
                            "3": "STATUS"
                        }[opcao]
                    }
                    
                    resposta = self.enviar_comando(comando)
                    print(f"\nResposta: {resposta['mensagem'] if 'mensagem' in resposta else resposta}")
                    
                except (ValueError, IndexError):
                    print("Opção inválida!")
            else:
                print("Opção inválida!")

    def desconectar(self):
        """Encerra a conexão com o servidor"""
        if self.sock:
            self.sock.close()
            self.logger.info("Desconectado do servidor")

def main():
    cliente = ClienteIoT()
    try:
        cliente.conectar()
        cliente.menu_principal()
    finally:
        cliente.desconectar()

if __name__ == "__main__":
    main() 