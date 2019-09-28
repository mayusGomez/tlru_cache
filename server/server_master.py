
from trlu_cache_server.app import CacheApp
import logging


settings = {
    'NODES_LIMIT_CUANTITY' : 5,
    'LOGGING': logging.DEBUG,
    'SERVER': {
        'type': 'master',
        'address': 'localhost',
        'port_to_slaves': 8765,
        'port_to_clients': 8766
    }
}


def main():
    app = CacheApp(settings)
    app.run()


if __name__ == "__main__":
    main()
