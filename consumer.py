from kafka import KafkaConsumer
from const import *
import sys
import json
from datetime import datetime

def show_banner():
    """Exibe banner de boas-vindas"""
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}  CHAT EM GRUPO COM KAFKA - CONSUMER{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def show_available_topics():
    """Exibe os tópicos/grupos disponíveis"""
    print(f"{Colors.YELLOW}Grupos de Chat Disponíveis:{Colors.END}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.END}")
    for topic, description in CHAT_TOPICS.items():
        print(f"  {Colors.GREEN}• {topic:15}{Colors.END} - {description}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.END}\n")

def get_topics():
    """Solicita os tópicos que o usuário deseja monitorar"""
    show_available_topics()
    print(f"{Colors.BLUE}Digite os grupos que deseja monitorar (separados por vírgula){Colors.END}")
    print(f"{Colors.YELLOW}Exemplo: geral,tecnologia,esportes{Colors.END}")
    print(f"{Colors.YELLOW}Ou digite 'todos' para monitorar todos os grupos{Colors.END}\n")
    
    topics_input = input(f"{Colors.BLUE}Grupos: {Colors.END}").strip().lower()
    
    if topics_input == 'todos':
        return list(CHAT_TOPICS.keys())
    
    topics = [t.strip() for t in topics_input.split(',')]
    
    # Valida os tópicos
    valid_topics = []
    for topic in topics:
        if topic in CHAT_TOPICS:
            valid_topics.append(topic)
        else:
            print(f"{Colors.RED}Aviso: Grupo '{topic}' não existe e será ignorado.{Colors.END}")
    
    if not valid_topics:
        print(f"{Colors.RED}Nenhum grupo válido foi selecionado!{Colors.END}")
        exit(1)
    
    return valid_topics

def format_timestamp(iso_timestamp):
    """Formata timestamp para exibição"""
    try:
        dt = datetime.fromisoformat(iso_timestamp)
        return dt.strftime("%H:%M:%S")
    except:
        return "??:??:??"

def display_message(msg, topic):
    """Exibe mensagem formatada"""
    try:
        # Tenta decodificar como JSON (mensagens novas)
        data = json.loads(msg.value.decode('utf-8'))
        username = data.get('username', 'Desconhecido')
        content = data.get('content', '')
        timestamp = format_timestamp(data.get('timestamp', ''))
        msg_type = data.get('type', 'message')
        
        # Formata baseado no tipo de mensagem
        if msg_type == 'system':
            # Mensagens do sistema (entrou/saiu)
            print(f"{Colors.YELLOW}[{timestamp}] [{topic}] "
                  f"*** {username} {content} ***{Colors.END}")
        else:
            # Mensagens normais
            print(f"{Colors.CYAN}[{timestamp}] [{Colors.GREEN}{topic}{Colors.CYAN}] "
                  f"{Colors.BOLD}{username}:{Colors.END} {content}")
    
    except json.JSONDecodeError:
        # Mensagens antigas/simples (não JSON)
        try:
            content = msg.value.decode('utf-8')
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{Colors.CYAN}[{timestamp}] [{Colors.GREEN}{topic}{Colors.CYAN}] "
                  f"{Colors.END}{content}")
        except:
            print(f"{Colors.RED}[Erro ao decodificar mensagem]{Colors.END}")

def main():
    """Função principal do chat consumer"""
    show_banner()
    
    # Configuração inicial
    topics = get_topics()
    
    print(f"\n{Colors.GREEN}Monitorando grupos: {', '.join(topics)}{Colors.END}")
    print(f"{Colors.YELLOW}Aguardando mensagens... (Ctrl+C para sair){Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
    
    # Conecta ao Kafka
    try:
        consumer = KafkaConsumer(
            bootstrap_servers=[BROKER_ADDR + ':' + BROKER_PORT],
            auto_offset_reset='latest',  # Começa do mais recente
            enable_auto_commit=True,
            value_deserializer=lambda x: x  # Mantém como bytes, vamos decodificar depois
        )
        consumer.subscribe(topics)
    except Exception as e:
        print(f"\n{Colors.RED}✗ Erro ao conectar ao Kafka: {e}{Colors.END}")
        exit(1)
    
    # Loop principal - recebe e exibe mensagens
    try:
        for msg in consumer:
            display_message(msg, msg.topic)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Consumer interrompido pelo usuário.{Colors.END}")
    
    except Exception as e:
        print(f"\n{Colors.RED}Erro: {e}{Colors.END}")
    
    finally:
        consumer.close()
        print(f"{Colors.GREEN}Desconectado do chat. Até logo!{Colors.END}\n")

if __name__ == "__main__":
    main()
