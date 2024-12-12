# Simulação do Barbeiro Dorminhoco 💈✂️

Este algoritmo simula um sistema simples de atendimento de clientes em uma barbearia, utilizando conceitos de **concorrência** e **sincronização de threads** em Python. O algoritmo implementa um **barbeiro dorminhoco** que atende os clientes conforme eles chegam, respeitando o número máximo de clientes que podem esperar na fila.

## Descrição do Sistema 🛋️💺

O sistema consiste em dois componentes principais:

- **Barbeiro** 🧔: Responsável por atender os clientes, mas só acorda quando há um cliente na fila. Ele atende um cliente por vez, e se não houver clientes, ele volta a dormir 😴.
  
- **Clientes** 👨‍🦱👩‍🦳: Chegam à barbearia em tempos aleatórios, tentam entrar na fila de espera e, se houver espaço disponível, aguardam sua vez de serem atendidos.

### Componentes

1. **Barbeiro** 🧔:
   - **Fila de espera** 🛋️: Uma lista que armazena os clientes que estão aguardando para serem atendidos.
   - **Semáforo** 🚦: Limita o número de clientes que podem esperar na fila. Quando a fila está cheia, os clientes são informados de que não há mais espaço e vão embora 😞.
   - **Eventos e Lock** 🔒: Utilizados para coordenar o processo de atendimento do barbeiro e garantir que apenas um cliente seja atendido por vez.

2. **Cliente** 👨‍🦱👩‍🦳:
   - Cada cliente tenta entrar na fila de espera e aguarda sua vez de ser atendido pelo barbeiro.
   - O tempo de chegada e o tempo de atendimento são aleatórios, simulando um ambiente dinâmico ⏳.

## Como Funciona 🔄

1. O **barbeiro** começa dormindo 😴. Ele acorda apenas quando há um cliente na fila.
2. Quando um **cliente** chega, ele tenta entrar na fila de espera. Se houver espaço, ele entra; caso contrário, ele vai embora 😞.
3. O **barbeiro** atende os clientes na ordem em que chegaram, e quando termina o atendimento de um cliente, ele acorda e atende o próximo da fila.
4. Se a fila estiver vazia 🛋️, o barbeiro volta a dormir até que um novo cliente chegue.

## Detalhes Técnicos 🖥️

- **Threads** 💻: Utilizadas para representar tanto o barbeiro quanto os clientes.
- **Semáforo** 🚦: Limita o número de clientes na fila (10, no caso deste exemplo).
- **Eventos** 🛑: São usados para coordenar o momento em que o barbeiro começa e termina de atender um cliente.
- **Lock** 🔐: Garante que o acesso à fila de espera seja feito de forma segura e sincronizada entre as threads.

## Como Executar 🚀

Para rodar o programa, basta executar o script Python:

```bash
python main.py
```````
