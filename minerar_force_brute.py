import multiprocessing
from bit import Key
import os
import logging
import random
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def worker(start: int, end: int, wallets: List[str], stop_event: multiprocessing.Event, file_path: str) -> None:
    while not stop_event.is_set():
        key_int = random.randint(start, end)
        key = Key.from_int(key_int)
        public_address = key.address
        if public_address in wallets:
            logging.info(f"Found matching address: {public_address} with private key: {key.to_hex()}")
            with open(file_path, 'a') as f:
                f.write(f"Address: {public_address}, Private Key: {key.to_hex()}\n")
            stop_event.set()
            return
    logging.info("Completed without finding a match")

def main() -> None:
    min_exp = 65  # Expoente mínimo (potência de 2)
    max_exp = 66  # Exponente máximo (potência de 2)

    target_wallets = ['13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so']  # Endereços Bitcoin alvo

    min_key = 2 ** min_exp  # Chave privada mínima (em decimal)
    max_key = 2 ** max_exp - 1  # Chave privada máxima (em decimal)

    logging.info(f"Procurando chave privada para o endereço alvo: {target_wallets}")
    logging.info(f"Intervalo de chaves privadas: [{min_key}, {max_key}]")

    num_processes = os.cpu_count() or 1  # Número de processos baseado no número de CPUs

    file_path = 'found_keys.txt'  # Caminho do arquivo onde as chaves encontradas serão salvas

    with multiprocessing.Manager() as manager:
        stop_event = manager.Event()
        pool = multiprocessing.Pool(processes=num_processes)
        processes = []

        for _ in range(num_processes):
            p = pool.apply_async(worker, args=(min_key, max_key, target_wallets, stop_event, file_path))
            processes.append(p)

        for p in processes:
            p.wait()

        pool.close()
        pool.join()

if __name__ == "__main__":
    main()
