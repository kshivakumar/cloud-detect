import asyncio
import logging
import time

from cloud_detect.providers import AlibabaProvider
from cloud_detect.providers import AWSProvider
from cloud_detect.providers import AzureProvider
from cloud_detect.providers import DOProvider
from cloud_detect.providers import GCPProvider
from cloud_detect.providers import OCIProvider

ALL_PROVIDERS = [
    AlibabaProvider, AWSProvider, AzureProvider,
    DOProvider, GCPProvider, OCIProvider,
]

TIMEOUT = 5  # seconds


async def _process(providers, timeout):
    tasks = {
        prov.identifier: asyncio.create_task(
            prov().identify(),
        ) for prov in providers
    }

    def cancel_unfinished_tasks():
        for t in tasks.values():
            if not t.done():
                t.cancel()

    stoptime = time.time() + timeout
    while tasks and time.time() < stoptime:
        for prov in list(tasks):
            t = tasks[prov]
            if t.done():
                del tasks[prov]
                if t.result():
                    logging.debug(f'Cloud_detect result is {prov}')
                    cancel_unfinished_tasks()
                    return prov
        else:
            await asyncio.sleep(0.1)
            continue

    if tasks:
        cancel_unfinished_tasks()
        return 'timeout'
    else:
        return 'unknown'


def provider(excluded=[], timeout=TIMEOUT):
    providers = [p for p in ALL_PROVIDERS if p.identifier not in excluded]
    return asyncio.run(_process(providers, timeout))


SUPPORTED_PROVIDERS = tuple(p.identifier for p in ALL_PROVIDERS)


__all__ = (
    'provider',
    'SUPPORTED_PROVIDERS'
)
