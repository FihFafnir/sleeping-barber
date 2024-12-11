import threading
import time
import random


class Barber:
    def __init__(self, max_queue_size):
        self.waiting_queue = []
        self.lock = threading.Lock()
        self.barber_awake = threading.Event()
        self.semaphore = threading.Semaphore(max_queue_size)

    def attend_customer(self):
        """Método para o barbeiro atender um cliente."""
        while True:
            self.barber_awake.wait()  # Espera até um cliente estar na fila
            self.lock.acquire()

            if self.waiting_queue:
                self.semaphore.release()  # Libera uma "cadeira" no semáforo para um novo cliente
                customer = self.waiting_queue.pop(0)
                print(f"Barbeiro atendendo o cliente {customer.id}.")
                self.lock.release()

                time.sleep(random.uniform(1, 3))  # Tempo aleatório de atendimento
                print(f"Barbeiro terminou de atender o cliente {customer.id}.")
            else:
                self.barber_awake.clear()  # Se a fila estiver vazia, o barbeiro volta a dormir

    def add_customer(self, customer):
        """Método para adicionar um cliente à fila de espera, com controle de semáforo."""
        if self.semaphore.acquire(blocking=False):  # Tenta adquirir o semáforo
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
        time.sleep(random.uniform(0.5, 2))  # Tempo de chegada aleatório
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
