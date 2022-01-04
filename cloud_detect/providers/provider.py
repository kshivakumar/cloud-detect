from abc import ABCMeta  # noqa: F401
from abc import abstractmethod  # noqa: F401


class AbstractProvider:
    """
        Abstract class representing a cloud provider.
        All concrete cloud providers should implement this.
    """
    identifier = 'unknown'

    @abstractmethod
    async def identify(self):
        pass  # pragma: no cover

    @abstractmethod
    async def check_metadata_server(self):
        pass  # pragma: no cover

    @abstractmethod
    def check_vendor_file(self):
        pass  # pragma: no cover
