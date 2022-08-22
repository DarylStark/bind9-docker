#!/usr/bin/python3

import sys
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
        args=[
            '/app/bind9/sbin/named',
            '-v'],
        stdout=subprocess.PIPE)
    version = version_output.stdout.decode('utf-8').split(' ')[1]
    logger.info(f'BIND9 version: {version}')

    # Check if there is a `named.conf` file. If there is, the
    # script doesn't do antyhing. If there isn't, the script will
    # create a `rndc.key` file and will copy the predefined
    # `named.conf` files from the image
    logger.info('Checking if a `named.conf` file exists')
    if not os.path.isfile('/app/config/named.conf'):
        logger.info(
            'The `named.conf` file doesn\'t exist. Copying examples to config directory')
        copy_tree(
            src='/app/config-examples/',
            dst='/app/config/')
        logger.info('Generating key for `rndc`')
        #os.system('/app/bind9/sbin/rndc-confgen -a')
        rv = subprocess.run(
            args=[
                '/app/bind9/sbin/rndc-confgen',
                '-a',                   # Genere the clause and write to file
                '-b', '512',            # 512 bits for the key
                '-A', 'hmac-sha512'     # hmac-sha512 as algorithm
            ],
            capture_output=True)
        if rv.returncode != 0:
            logger.error('Error generating key for `rndc`')
            logger.error(f'STDOUT: {rv.stdout}')
            logger.error(f'STDERR: {rv.stderr}')
            exit(1)
    else:
        logger.info('The `named.conf` file does exist!')

    # Start the BIND9 server
    arguments = ['-f']
    if len(sys.argv) > 1:
        arguments = sys.argv[1:]
    logger.info(f'Starting BIND {version} with arguments: {arguments}')
    try:
        subprocess.run(
            args=[
                '/app/bind9/sbin/named',
                *arguments
            ],
            capture_output=False)
    except KeyboardInterrupt:
        logger.info(f'Killed by KeyboardInterrupt')
