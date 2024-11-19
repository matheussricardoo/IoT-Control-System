"""Configurações globais do projeto"""

# Configurações do servidor
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 10418

# Configurações de logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# Configurações dos dispositivos
DISPOSITIVOS_PADRAO = {
    "luz_sala": False,
    "luz_quarto": False,
    "luz_cozinha": False
} 