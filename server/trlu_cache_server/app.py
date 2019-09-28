import logging
from trlu_cache_server.repository import file_repo

from  trlu_cache_server.web_socket import server_master, server_slave


class CacheApp:
    def __init__(self, settings=None):
        self.settings = settings

    def run(self):
        logging.basicConfig(
            level=self.settings['LOGGING'],
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        if self.settings['SERVER']['type'] == 'master':
            file_repo.init_master()
            server_master.execute(self.settings)
        else:
            file_repo.init_slave()
            server_slave.execute(self.settings)
