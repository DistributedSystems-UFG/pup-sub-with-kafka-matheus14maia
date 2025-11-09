BROKER_ADDR = '172.31.91.151'
BROKER_PORT = '9092'

# Tópicos/Grupos de chat disponíveis
CHAT_TOPICS = {
    'geral': 'Grupo Geral - Chat aberto para todos',
    'tecnologia': 'Grupo Tecnologia - Discussões sobre tech',
    'esportes': 'Grupo Esportes - Fale sobre seus times favoritos',
    'musica': 'Grupo Música - Compartilhe e discuta músicas',
    'jogos': 'Grupo Jogos - Para gamers',
    'noticias': 'Grupo Notícias - Últimas notícias e eventos',
    'privado': 'Grupo Privado - Conversas privadas'
}

# Cores para o terminal (ANSI)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'