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
    tasks = []
    for provider in providers:
        task = asyncio.create_task(
            provider().identify(),
            name=provider.identifier,
        )
        tasks.append(task)

    result = 'unknown'
    timeout = time.time() + timeout
    while time.time() < timeout:
        for t in tasks:
            if t.done() and t.result():
                result = t.get_name()
                logging.debug(f'Cloud_detect result is {result}')
                break
        else:
            await asyncio.sleep(0.1)
            continue
        break
    else:
        result = 'timeout'

    for t in tasks:
        if not t.done():
            t.cancel()

    return result


def provider(excluded=[], timeout=TIMEOUT):
    providers = [p for p in ALL_PROVIDERS if p.identifier not in excluded]
    result = asyncio.run(_process(providers, timeout))
    print('Result', result)
    return result


SUPPORTED_PROVIDERS = tuple(p.identifier for p in ALL_PROVIDERS)


__all__ = (
    'provider',
    'SUPPORTED_PROVIDERS'
)
