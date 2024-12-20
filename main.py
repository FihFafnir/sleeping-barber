import threading
import time
import random


class Barber:
    def __init__(self, max_queue_size):
        self.waiting_queue = [] # Clone da fila de espera
        self.lock = threading.Lock() # Mutex do sistema. Variavel de controle para colocar alguem na fila de espera
        self.barber_awake = threading.Event() # Lock do barbeiro, para saber se está acordado
        self.barber_is_not_attending = threading.Event() # Lock do babeiro, para saber se ele está atendendo um cliente
        self.waiting_chairs = threading.Semaphore(max_queue_size) # fila de cadeiras para espera dos clientes

    def attend_customer(self):
        """Método para o barbeiro atender um cliente."""

        self.barber_is_not_attending.set()

        while True:
            self.barber_awake.wait()  # Espera até um cliente estar na fila
            self.barber_is_not_attending.wait()  # Espera o terminar de atender o cliente atual
            self.lock.acquire()

            if self.waiting_queue:
                self.waiting_chairs.release()  # Libera uma "cadeira" no semáforo para um novo cliente
                self.barber_is_not_attending.clear()  # Começa a atender o cliente atual
                customer = self.waiting_queue.pop(0)

                print(f"Barbeiro atendendo o cliente {customer.id}.")
                self.lock.release()

                time.sleep(random.uniform(1, 3))  # Tempo aleatório de atendimento
                self.barber_is_not_attending.set()  # Termina de atender o cliente atual
                print(f"Barbeiro terminou de atender o cliente {customer.id}.")
            else:
                self.barber_awake.clear()  # Se a fila estiver vazia, o barbeiro volta a dormir
                self.lock.release()

    def add_customer(self, customer):
        """Método para adicionar um cliente à fila de espera, com controle de semáforo."""
        if self.waiting_chairs.acquire(blocking=False):  # Tenta adquirir o semáforo
            with self.lock:
                self.waiting_queue.append(customer)
                print(f"Cliente {customer.id} entrou na fila.")
                self.barber_awake.set()  # Acorda o barbeiro se ele estiver dormindo
        else:
            with self.lock:
                print(
                    f"Cliente {customer.id} foi embora, fila cheia."
                )  # Sem espaço na fila


class Customer(threading.Thread):
    def __init__(self, customer_id, barber):
        super().__init__()
        self.id = customer_id
        self.barber = barber

    def run(self):
        """Simula a chegada do cliente e sua tentativa de ser atendido."""
        time.sleep(random.uniform(1, 10))  # Tempo de chegada aleatório
        self.barber.add_customer(self)


def main():
    barber = Barber(max_queue_size=10)  # Limite de 10 clientes na fila

    # Criando e iniciando o barbeiro em uma thread
    barber_thread = threading.Thread(target=barber.attend_customer, daemon=True)
    barber_thread.start()

    # Criando e iniciando os clientes
    customers = [Customer(i, barber) for i in range(1, 20)]
    for customer in customers:
        customer.start()

    # Aguardando todas as threads de clientes terminarem
    for customer in customers:
        customer.join()  # Aguarda a finalização de cada cliente

    # Aguardando o barbeiro terminar de atender todos os clientes
    barber_thread.join()


if __name__ == "__main__":
    main()
