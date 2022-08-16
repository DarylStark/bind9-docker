#!/usr/bin/python3

import logging
from rich.logging import RichHandler
import subprocess

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        datefmt="[%X]",
        handlers=[RichHandler()]
    )
    logger = logging.getLogger('Entrypoint')

    # Start the script
    logger.info('Starting Docker container for BIND9')

    # Get the BIND9 version
    version_output = subprocess.run(
        ['/app/bind9/sbin/named', '-v'], stdout=subprocess.PIPE)
    version = version_output.stdout.decode('utf-8').split(' ')[1]
    logger.info(f'BIND9 version: {version}')
