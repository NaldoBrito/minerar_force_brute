import multiprocessing
from bit import Key
import os

def worker(start, end, wallets):
    for key_int in range(start, end + 1):
        key = Key.from_int(key_int)
        public_address = key.address
        if public_address in wallets:
            print(f"Found matching address: {public_address} with private key: {key.to_hex()}")
            return
    print("Completed without finding a match")

def main():
    min_exp = 9  # Expoente mínimo (potência de 2)
    max_exp = 10  # Exponente máximo (potência de 2)

    target_wallets = ['1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe']  # Endereços Bitcoin alvo

    min_key = 2 ** min_exp  # Chave privada mínima (em decimal)
    max_key = 2 ** max_exp - 1  # Chave privada máxima (em decimal)

    print(f"Procurando chave privada para o endereço alvo: {target_wallets}")
    print(f"Intervalo de chaves privadas: [{min_key}, {max_key}]")

    # Cria processos para cada intervalo de chaves privadas
    processes = []
    num_processes = os.cpu_count()  # Número de processos baseado no número de CPUs
    range_per_process = (max_key - min_key) // num_processes

    for i in range(num_processes):
        start = min_key + i * range_per_process
        if i == num_processes - 1:  # Se for o último processo, vai até o final do intervalo
            end = max_key
        else:
            end = start + range_per_process - 1
        p = multiprocessing.Process(target=worker, args=(start, end, target_wallets))
        processes.append(p)
        p.start()

    # Aguarda todos os processos terminarem
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
