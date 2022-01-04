import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class AlibabaProvider(AbstractProvider):
    """
        Concrete implementation of the AWS cloud provider.
    """
    identifier = 'alibaba'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = 'http://100.100.100.200/latest/meta-data/latest/meta-data/instance/virtualization-solution'  # noqa
        self.vendor_file = '/sys/class/dmi/id/product_name'

    async def identify(self):
        """
            Tries to identify Alibaba using all the implemented options
        """
        self.logger.info('Try to identify Alibaba')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify Alibaba via metadata server
        """
        self.logger.debug('Checking Alibaba metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url) as response:
                    response = await response.json()
                    if response['imageId'].startswith('ami-',) and response[
                        'instanceId'
                    ].startswith('i-'):
                        return True
            return False
        except BaseException:
            return False

    def check_vendor_file(self):
        """
            Tries to identify Alibaba provider by reading the /sys/class/dmi/id/product_name
        """
        self.logger.debug('Checking Aliobaba vendor file')
        alibaba_path = Path(self.vendor_file)
        if alibaba_path.is_file():
            if 'Alibaba Cloud ECS' in open(self.vendor_file).read():
                return True
        return False
