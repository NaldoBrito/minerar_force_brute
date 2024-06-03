import unittest
from unittest.mock import patch, mock_open, MagicMock
import multiprocessing
import time
from minerar_force_brute import worker  # Certifique-se de que minerar_force_brute.py tem a função worker


class TestBitcoinKeySearch(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open)
    @patch('minerar_force_brute.Key.from_int')
    def test_worker_finds_key(self, mock_key_from_int, mock_file):
        key_mock = MagicMock()
        key_mock.address = '1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum'
        key_mock.to_hex.return_value = '00000000000000000000000000000000000000000000000000000000000d2c55'
        mock_key_from_int.return_value = key_mock

        wallets = ['1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum']
        stop_event = multiprocessing.Event()
        file_path = 'found_keys.txt'

        worker(2 ** 19, 2 ** 20 - 1, wallets, stop_event, file_path)

        mock_file().write.assert_called_once_with(
            "Address: 1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum, Private Key: 00000000000000000000000000000000000000000000000000000000000d2c55\n")

    @patch('minerar_force_brute.random.randint', side_effect=lambda start, end: end)
    def test_worker_does_not_find_key(self, mock_randint):
        wallets = ['NonMatchingAddress']
        stop_event = multiprocessing.Event()
        file_path = 'found_keys.txt'

        with patch('minerar_force_brute.logging.info') as mock_logging:
            worker(2 ** 19, 2 ** 20 - 1, wallets, stop_event, file_path)
            mock_logging.assert_any_call("Completed without finding a match")


if __name__ == '__main__':
    unittest.main()
