from kafka import KafkaProducer
from const import *
import sys
import json
from datetime import datetime

def show_banner():
    """Exibe banner de boas-vindas"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}  CHAT EM GRUPO COM KAFKA - PRODUCER{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def show_available_topics():
    """Exibe os tópicos/grupos disponíveis"""
    print(f"{Colors.YELLOW}Grupos de Chat Disponíveis:{Colors.END}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.END}")
    for topic, description in CHAT_TOPICS.items():
        print(f"  {Colors.GREEN}• {topic:15}{Colors.END} - {description}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.END}\n")

def show_help():
    """Exibe comandos disponíveis"""
    print(f"\n{Colors.YELLOW}Comandos Disponíveis:{Colors.END}")
    print(f"  {Colors.GREEN}/help{Colors.END}        - Mostra esta ajuda")
    print(f"  {Colors.GREEN}/grupos{Colors.END}      - Lista todos os grupos disponíveis")
    print(f"  {Colors.GREEN}/trocar{Colors.END}      - Troca de grupo/tópico")
    print(f"  {Colors.GREEN}/usuario{Colors.END}     - Troca seu nome de usuário")
    print(f"  {Colors.GREEN}/sair{Colors.END}        - Sai do chat\n")

def get_username():
    """Solicita nome do usuário"""
    username = input(f"{Colors.BLUE}Digite seu nome de usuário: {Colors.END}").strip()
    while not username:
        print(f"{Colors.RED}Nome não pode ser vazio!{Colors.END}")
        username = input(f"{Colors.BLUE}Digite seu nome de usuário: {Colors.END}").strip()
    return username

def get_topic():
    """Solicita o tópico/grupo"""
    show_available_topics()
    topic = input(f"{Colors.BLUE}Escolha um grupo para entrar: {Colors.END}").strip().lower()
    
    while topic not in CHAT_TOPICS:
        print(f"{Colors.RED}Grupo '{topic}' não existe! Escolha um grupo válido.{Colors.END}")
        topic = input(f"{Colors.BLUE}Escolha um grupo para entrar: {Colors.END}").strip().lower()
    
    return topic

def create_message(username, content, msg_type='message'):
    """Cria uma mensagem estruturada em JSON"""
    message = {
        'username': username,
        'content': content,
        'timestamp': datetime.now().isoformat(),
        'type': msg_type
    }
    return json.dumps(message)

def send_system_message(producer, topic, username, action):
    """Envia mensagens do sistema (entrou/saiu)"""
    msg = create_message(username, f"{action} do grupo", msg_type='system')
    producer.send(topic, value=msg.encode())

def main():
    """Função principal do chat producer"""
    show_banner()
    
    # Configuração inicial
    username = get_username()
    current_topic = get_topic()
    
    # Conecta ao Kafka
    try:
        producer = KafkaProducer(bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT])
        print(f"\n{Colors.GREEN}✓ Conectado ao servidor Kafka!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}✗ Erro ao conectar ao Kafka: {e}{Colors.END}")
        exit(1)
    
    # Anuncia entrada no grupo
    send_system_message(producer, current_topic, username, "entrou")
    producer.flush()
    
    print(f"\n{Colors.GREEN}Você entrou no grupo '{current_topic}'!{Colors.END}")
    print(f"{Colors.YELLOW}Digite suas mensagens (ou /help para ver comandos){Colors.END}\n")
    
    try:
        while True:
            # Lê mensagem do usuário
            user_input = input(f"{Colors.BOLD}[{username}@{current_topic}]:{Colors.END} ").strip()
            
            if not user_input:
                continue
            
            # Processa comandos
            if user_input.startswith('/'):
                command = user_input.lower()
                
                if command == '/help':
                    show_help()
                
                elif command == '/grupos':
                    show_available_topics()
                
                elif command == '/trocar':
                    # Anuncia saída do grupo atual
                    send_system_message(producer, current_topic, username, "saiu")
                    producer.flush()
                    
                    # Escolhe novo grupo
                    current_topic = get_topic()
                    
                    # Anuncia entrada no novo grupo
                    send_system_message(producer, current_topic, username, "entrou")
                    producer.flush()
                    print(f"\n{Colors.GREEN}Você entrou no grupo '{current_topic}'!{Colors.END}\n")
                
                elif command == '/usuario':
                    old_username = username
                    username = get_username()
                    print(f"{Colors.GREEN}Nome alterado de '{old_username}' para '{username}'!{Colors.END}\n")
                
                elif command == '/sair':
                    print(f"\n{Colors.YELLOW}Saindo do chat...{Colors.END}")
                    send_system_message(producer, current_topic, username, "saiu")
                    producer.flush()
                    break
                
                else:
                    print(f"{Colors.RED}Comando desconhecido! Digite /help para ver os comandos disponíveis.{Colors.END}")
            
            else:
                # Envia mensagem normal
                msg = create_message(username, user_input)
                producer.send(current_topic, value=msg.encode())
                producer.flush()
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Chat interrompido pelo usuário.{Colors.END}")
        send_system_message(producer, current_topic, username, "saiu")
        producer.flush()
    
    except Exception as e:
        print(f"\n{Colors.RED}Erro: {e}{Colors.END}")
    
    finally:
        producer.close()
        print(f"{Colors.GREEN}Desconectado do chat. Até logo!{Colors.END}\n")

if __name__ == "__main__":
    main()
