""" Module that contains the script to create Dockerfile with
    the specified version. """

import os
import shutil
import jinja2
import argparse
import logging
import sys
from subprocess import Popen
from rich.logging import RichHandler

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    # Get the script directory
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Argument parser
    parser = argparse.ArgumentParser()

    # Positional arguments
    parser.add_argument('version',
                        type=str,
                        help='The version number for BIND9 (in the format `9.16.32`)')

    # Optional arguments
    parser.add_argument('--builddir',
                        type=str,
                        default='./bind9-docker-build/',
                        help='The build directory')
    parser.add_argument('--is-development',
                        action='store_true',
                        default=False,
                        help='Tag as `development` version')
    parser.add_argument('--is-esv',
                        action='store_true',
                        default=False,
                        help='Tag as `extended support version`')
    parser.add_argument('--is-stable',
                        action='store_true',
                        default=False,
                        help='Tag as `stable` and `latests` version')

    # Parse the arguments
    args = parser.parse_args()
    build_dir = args.builddir
    if build_dir[-1] == '/':
        build_dir = build_dir[0:-1]

    # Load the Dockerfile template
    loader = jinja2.FileSystemLoader(searchpath=script_dir)
    env = jinja2.Environment(loader=loader)
    logging.info('Loading Dockerfile template')
    template = env.get_template(f'Dockerfile.template.j2')
    dockerfile = template.render(
        {
            'version': args.version
        }
    )

    # Create the build directory
    directory_name = f'{build_dir}/{args.version}'
    try:
        os.makedirs(directory_name)
    except FileExistsError:
        logging.warning(
            f'The directory "{directory_name}" already exists. Overwriting')
    except:
        # All other error messages should stop the script
        logging.info(
            f'Couldn\'t create build directory "{directory_name}". Please check permissions.')
        sys.exit(1)

    # Create the Dockerfile
    logging.info('Creating Dockerfile')
    try:
        with open(f'{directory_name}/Dockerfile', 'w') as outfile:
            outfile.write(dockerfile)
    except Exception:
        logging.error('Couldn\'t write Dockerfile. Please check permissions.')
        sys.exit(1)

    # Copy 'container folder'
    logging.info('Copying container folder')
    try:
        containerfolder_src = f'{script_dir}/container-folders/'
        containerfolder_dst = f'{directory_name}/container-folders'
        shutil.copytree(
            src=containerfolder_src,
            dst=containerfolder_dst,
            dirs_exist_ok=True)
    except KeyboardInterrupt:
        logging.error('Couldn\'t copy container')

    # Build image
    tags = [f'dast1986/darylstark-bind9:{args.version}']

    if args.is_stable:
        tags.append(f'dast1986/darylstark-bind9:latest')
        tags.append(f'dast1986/darylstark-bind9:stable')

    if args.is_esv:
        tags.append(f'dast1986/darylstark-bind9:esv')

    # Add the `--tag` keyword
    tags_args = tags[::]
    for x in range(len(tags_args) - 1):
        tags_args.insert(2 * x + 1, '--tag')
    tags_args.insert(0, '--tag')

    logging.info('Creating Docker image with the following tags:')
    for tag in tags:
        logging.info(f'- {tag}')

    # Get the args
    args = ['docker', 'build', *tags_args, '.']

    build = Popen(
        args=args,
        cwd=directory_name)
    build.wait()

    if build.returncode != 0:
        logging.error(
            'Something went wrong while building Docker image. Aborting!')
        sys.exit(1)

    # Publish image
    for tag in tags:
        logging.info(f'Pushing tag "{tag}"')
        push = Popen(args=['docker', 'push', tag])
        push.wait()
