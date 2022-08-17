#!/usr/bin/python3

import time
from rich.logging import RichHandler
import logging
import subprocess
import os
from distutils.dir_util import copy_tree

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

    # Check if there is a `named.conf` file. If there is, the
    # script doesn't do antyhing. If there isn't, the script will
    # create a `rndc.key` file and will copy the predefined
    # `named.conf` files from the image
    logger.info('Checking if a `named.conf` file exists')
    if not os.path.isfile('/app/config/named.conf'):
        logger.info(
            'The `named.conf` file doens\'t exist. Copying examples to config directory')
        copy_tree(
            src='/app/config-examples/',
            dst='/app/config/')
        logger.info('Generating key for `rndc`')
        # TODO: IMPLEMENT
    else:
        logger.info('The `named.conf` file does exist!')

    # Start the BIND9 server
    while True:
        time.sleep(1)
