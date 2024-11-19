import socket
import logging
from typing import Tuple
import json

class ServidorIoT:
    def __init__(self, host: str = "127.0.0.1", port: int = 10418):
        self.host = host
        self.port = port
        self.sock = None
        self.dispositivos = {
            "luz_sala": False,
            "luz_quarto": False,
            "luz_cozinha": False
        }
        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def iniciar(self):
        """Inicia o servidor e aguarda conexões"""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5)
            self.logger.info(f"Servidor rodando em {self.host}:{self.port}")
            self._aceitar_conexoes()
        except Exception as e:
            self.logger.error(f"Erro ao iniciar servidor: {e}")
            raise

    def _aceitar_conexoes(self):
        """Loop principal para aceitar conexões"""
        while True:
            try:
                conn, addr = self.sock.accept()
                self.logger.info(f"Nova conexão de {addr}")
                self._gerenciar_cliente(conn, addr)
            except Exception as e:
                self.logger.error(f"Erro na conexão: {e}")

    def _gerenciar_cliente(self, conn: socket.socket, addr: Tuple[str, int]):
        """Gerencia a comunicação com um cliente específico"""
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break

                comando = json.loads(data)
                resposta = self._processar_comando(comando)
                conn.sendall(json.dumps(resposta).encode('utf-8'))

            except Exception as e:
                self.logger.error(f"Erro ao processar mensagem: {e}")
                break

        conn.close()
        self.logger.info(f"Conexão com {addr} encerrada")

    def _processar_comando(self, comando: dict) -> dict:
        """Processa os comandos recebidos do cliente"""
        acao = comando.get("acao")
        dispositivo = comando.get("dispositivo")

        if dispositivo == "todos":
            if acao == "LIGAR":
                for disp in self.dispositivos:
                    self.dispositivos[disp] = True
                return {"status": "sucesso", "mensagem": "Todos os dispositivos foram ligados"}
            
            elif acao == "DESLIGAR":
                for disp in self.dispositivos:
                    self.dispositivos[disp] = False
                return {"status": "sucesso", "mensagem": "Todos os dispositivos foram desligados"}
            
            elif acao == "STATUS":
                return {
                    "status": "sucesso",
                    "estado": self.dispositivos
                }
        else:
            if acao == "LIGAR":
                self.dispositivos[dispositivo] = True
                return {"status": "sucesso", "mensagem": f"{dispositivo} ligado"}
            elif acao == "DESLIGAR":
                self.dispositivos[dispositivo] = False
                return {"status": "sucesso", "mensagem": f"{dispositivo} desligado"}
            elif acao == "STATUS":
                return {
                    "status": "sucesso", 
                    "estado": self.dispositivos[dispositivo]
                }
        
        return {"status": "erro", "mensagem": "Comando inválido"}

if __name__ == "__main__":
    servidor = ServidorIoT()
    servidor.iniciar() 