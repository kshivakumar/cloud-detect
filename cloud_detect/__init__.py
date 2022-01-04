import time
import logging
import asyncio

from cloud_detect.providers import AlibabaProvider
from cloud_detect.providers import AWSProvider
from cloud_detect.providers import AzureProvider
from cloud_detect.providers import DOProvider
from cloud_detect.providers import GCPProvider
from cloud_detect.providers import OCIProvider


PROVIDERS = [AlibabaProvider, AzureProvider, DOProvider,
             GCPProvider, OCIProvider, AWSProvider]

async def process():
    tasks = []
    for provider in PROVIDERS:
        task = asyncio.create_task(provider().identify(), name=provider.__name__)
        tasks.append(task)
    
    result = 'unknown'
    timeout = time.time() + 5
    while time.time() < timeout:
        for t in tasks:
            if t.done() and t.result():
                print(t.get_name(), 'done')
                result = t.get_name()
                break
        else:
            await asyncio.sleep(1)
            continue
        break

    for t in tasks:
        if not t.done():
            print('Cancelling', t.get_name())
            t.cancel()
    
    return result

def provider(excluded=[]):
    result = asyncio.run(process())
    print('Result', result)
    return
    if 'alibaba' not in excluded and AlibabaProvider().identify():
        logging.debug('Cloud_detect result is alibaba')
        return 'alibaba'
    elif 'aws' not in excluded and AWSProvider().identify():
        logging.debug('Cloud_detect result is aws')
        return 'aws'
    elif 'gcp' not in excluded and GCPProvider().identify():
        logging.debug('Cloud_detect result is gcp')
        return 'gcp'
    elif 'do' not in excluded and DOProvider().identify():
        logging.debug('Cloud_detect result is do')
        return 'do'
    elif 'azure' not in excluded and AzureProvider().identify():
        logging.debug('Cloud_detect result is azure')
        return 'azure'
    elif 'oci' not in excluded and OCIProvider().identify():
        logging.debug('Cloud_detect result is oci')
        return 'oci'
    else:
        logging.debug('Cloud_detect result is unknown')
        return 'unknown'
