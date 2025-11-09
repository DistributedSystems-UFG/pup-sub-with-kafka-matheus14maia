[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/eycvIrW-)

# 💬 Chat em Grupo com Kafka - Publish-Subscribe

Aplicação de chat em grupo implementando o padrão **Publish-Subscribe** utilizando **Apache Kafka** como middleware de mensageria.

## 📋 Descrição

Este projeto demonstra o uso do modelo publish-subscribe com Kafka, onde:
- **Producers** (remetentes) publicam mensagens em tópicos específicos
- **Consumers** (receptores) se inscrevem em um ou mais tópicos de interesse
- Múltiplos usuários podem participar de diferentes grupos de chat simultaneamente
- Mensagens são distribuídas automaticamente para todos os inscritos do tópico

## 🚀 Funcionalidades

### Sistema de Chat Completo
- ✅ **Múltiplos grupos/tópicos**: 7 grupos diferentes (geral, tecnologia, esportes, música, jogos, notícias, privado)
- ✅ **Mensagens estruturadas**: Formato JSON com timestamp, usuário e conteúdo
- ✅ **Mensagens do sistema**: Notificações de entrada/saída de usuários
- ✅ **Interface colorida**: Mensagens formatadas com cores ANSI no terminal
- ✅ **Comandos interativos**: Sistema de comandos para controlar o chat

### Producer (Produtor de Mensagens)
- Escolher nome de usuário
- Selecionar grupo para participar
- Enviar mensagens em tempo real
- Trocar de grupo dinamicamente
- Comandos especiais:
  - `/help` - Exibe ajuda
  - `/grupos` - Lista grupos disponíveis
  - `/trocar` - Muda de grupo
  - `/usuario` - Altera nome de usuário
  - `/sair` - Sai do chat

### Consumer (Receptor de Mensagens)
- Monitorar um ou múltiplos grupos simultaneamente
- Visualizar mensagens em tempo real com formatação colorida
- Distinguir mensagens normais de notificações do sistema
- Timestamps formatados (HH:MM:SS)
- Indicação clara do grupo de origem de cada mensagem

## 📁 Estrutura do Projeto

```
pup-sub-with-kafka/
├── const.py          # Configurações e constantes (broker, tópicos, cores)
├── producer.py       # Aplicação do produtor (envio de mensagens)
├── consumer.py       # Aplicação do consumidor (recebimento de mensagens)
└── README.md         # Este arquivo
```

## 🔧 Requisitos

### Software Necessário
- Python 3.7+
- Apache Kafka (servidor rodando)
- Biblioteca kafka-python

### Instalação das Dependências

```bash
pip install kafka-python
```

## ⚙️ Configuração

No arquivo `const.py`, configure o endereço do broker Kafka:

```python
BROKER_ADDR = '172.31.91.151'  # Altere para o IP do seu broker
BROKER_PORT = '9092'
```

## 🎮 Como Usar

### 1. Iniciar o Consumer (Receptor)

Primeiro, inicie um ou mais consumers para monitorar os grupos:

```bash
python consumer.py
```

O consumer irá:
1. Mostrar os grupos disponíveis
2. Solicitar quais grupos você deseja monitorar
3. Começar a exibir mensagens em tempo real

**Exemplos de uso:**
- Monitorar um grupo: `geral`
- Monitorar múltiplos grupos: `geral,tecnologia,esportes`
- Monitorar todos os grupos: `todos`

### 2. Iniciar o Producer (Remetente)

Em outro terminal, inicie o producer para enviar mensagens:

```bash
python producer.py
```

O producer irá:
1. Solicitar seu nome de usuário
2. Mostrar grupos disponíveis
3. Solicitar o grupo que deseja entrar
4. Permitir envio de mensagens

### 3. Testando com Múltiplos Usuários

Para simular um chat real, abra múltiplos terminais:

**Terminal 1 - Consumer monitorando tudo:**
```bash
python consumer.py
# Digite: todos
```

**Terminal 2 - Producer usuário "João":**
```bash
python producer.py
# Nome: João
# Grupo: tecnologia
```

**Terminal 3 - Producer usuário "Maria":**
```bash
python producer.py
# Nome: Maria
# Grupo: tecnologia
```

**Terminal 4 - Producer usuário "Pedro":**
```bash
python producer.py
# Nome: Pedro
# Grupo: esportes
```

## 🎯 Grupos Disponíveis

| Grupo | Descrição |
|-------|-----------|
| **geral** | Grupo Geral - Chat aberto para todos |
| **tecnologia** | Grupo Tecnologia - Discussões sobre tech |
| **esportes** | Grupo Esportes - Fale sobre seus times favoritos |
| **musica** | Grupo Música - Compartilhe e discuta músicas |
| **jogos** | Grupo Jogos - Para gamers |
| **noticias** | Grupo Notícias - Últimas notícias e eventos |
| **privado** | Grupo Privado - Conversas privadas |

## 📝 Formato das Mensagens

As mensagens são enviadas em formato JSON:

```json
{
  "username": "João",
  "content": "Olá pessoal!",
  "timestamp": "2025-11-09T14:30:45.123456",
  "type": "message"
}
```

**Tipos de mensagem:**
- `message` - Mensagem normal de chat
- `system` - Notificação do sistema (entrada/saída de usuários)

## 🎨 Interface

### Producer
```
============================================================
  CHAT EM GRUPO COM KAFKA - PRODUCER
============================================================

Digite seu nome de usuário: João

Grupos de Chat Disponíveis:
------------------------------------------------------------
  • geral          - Grupo Geral - Chat aberto para todos
  • tecnologia     - Grupo Tecnologia - Discussões sobre tech
  ...
------------------------------------------------------------

Escolha um grupo para entrar: tecnologia

✓ Conectado ao servidor Kafka!

Você entrou no grupo 'tecnologia'!
Digite suas mensagens (ou /help para ver comandos)

[João@tecnologia]: Olá pessoal!
```

### Consumer
```
============================================================
  CHAT EM GRUPO COM KAFKA - CONSUMER
============================================================

Grupos de Chat Disponíveis:
------------------------------------------------------------
  • geral          - Grupo Geral - Chat aberto para todos
  • tecnologia     - Grupo Tecnologia - Discussões sobre tech
  ...
------------------------------------------------------------

Digite os grupos que deseja monitorar (separados por vírgula)
Exemplo: geral,tecnologia,esportes
Ou digite 'todos' para monitorar todos os grupos

Grupos: tecnologia,esportes

Monitorando grupos: tecnologia, esportes
Aguardando mensagens... (Ctrl+C para sair)
============================================================

[14:30:45] [tecnologia] *** João entrou do grupo ***
[14:30:52] [tecnologia] João: Olá pessoal!
[14:31:05] [tecnologia] Maria: Oi João! Tudo bem?
[14:31:20] [esportes] *** Pedro entrou do grupo ***
```

## 🔄 Arquitetura Publish-Subscribe

```
┌─────────────┐                    ┌─────────────┐
│  Producer 1 │───┐                │  Consumer 1 │
│   (João)    │   │                │ (Monitor 1) │
└─────────────┘   │                └─────────────┘
                  │                       ▲
                  ▼                       │
┌─────────────┐  ┌────────────────────┐  │
│  Producer 2 │─▶│   KAFKA BROKER     │──┤
│   (Maria)   │  │                    │  │
└─────────────┘  │  Tópicos:          │  │
                 │  - geral           │  ▼
┌─────────────┐  │  - tecnologia      │  ┌─────────────┐
│  Producer 3 │─▶│  - esportes        │──│  Consumer 2 │
│   (Pedro)   │  │  - musica          │  │ (Monitor 2) │
└─────────────┘  │  - jogos           │  └─────────────┘
                 │  - noticias        │
                 │  - privado         │
                 └────────────────────┘
```

**Características:**
- **Desacoplamento**: Producers e consumers não se conhecem
- **Escalabilidade**: Múltiplos producers e consumers independentes
- **Flexibilidade**: Consumers escolhem quais tópicos monitorar
- **Persistência**: Kafka mantém histórico de mensagens
- **Distribuição**: Mensagens automaticamente distribuídas aos inscritos

## 🛠️ Tecnologias Utilizadas

- **Python 3** - Linguagem de programação
- **Apache Kafka** - Sistema de mensageria distribuído
- **kafka-python** - Biblioteca cliente Kafka para Python
- **JSON** - Formato de serialização de mensagens
- **ANSI Colors** - Formatação colorida do terminal

## 📚 Conceitos de Sistemas Distribuídos

Este projeto demonstra:
- ✅ **Publish-Subscribe Pattern** - Desacoplamento entre produtores e consumidores
- ✅ **Message Broker** - Kafka como intermediário de mensagens
- ✅ **Topics/Channels** - Organização lógica das mensagens
- ✅ **Assíncrono** - Comunicação não-bloqueante
- ✅ **Escalabilidade Horizontal** - Múltiplos producers/consumers
- ✅ **Persistência de Mensagens** - Kafka armazena o histórico
- ✅ **Consumer Groups** - Possibilidade de múltiplos consumidores

## 🔍 Possíveis Extensões

Ideias para expandir o projeto:
- [ ] Adicionar autenticação de usuários
- [ ] Implementar mensagens privadas (DM)
- [ ] Criar sala de moderadores
- [ ] Adicionar histórico de mensagens
- [ ] Implementar reações às mensagens
- [ ] Adicionar status online/offline
- [ ] Criar interface web (WebSocket + Kafka)
- [ ] Implementar criptografia de mensagens
- [ ] Adicionar suporte a arquivos/imagens
- [ ] Criar sistema de notificações

## 👥 Autor

Desenvolvido como trabalho acadêmico para a disciplina de Sistemas Distribuídos.

## 📄 Licença

Este projeto é de código aberto para fins educacionais.
