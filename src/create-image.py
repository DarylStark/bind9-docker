""" Module that contains the script to create Dockerfile with
    the specified version. """

import os
import jinja2
import argparse
from tkinter import W

if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('version',
                        type=str,
                        help='The version number for BIND9')
    parser.add_argument('--is-stable',
                        action='store_true',
                        default=False,
                        help='The version number for BIND9')
    parser.add_argument('--is-esv',
                        action='store_true',
                        default=False,
                        help='The version number for BIND9')

    # Parse the arguments
    args = parser.parse_args()

    # Load the Dockerfile template
    loader = jinja2.FileSystemLoader(searchpath='./')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('Dockerfile.template.j2')
    dockerfile = template.render(
        {
            'version': args.version
        }
    )

    # Create the build directory
    directory_name = f'../build/{args.version}'
    try:
        os.makedirs(directory_name)
    except FileExistsError:
        pass

    # Create the Dockerfile
    with open(f'{directory_name}/Dockerfile', 'w') as outfile:
        outfile.write(dockerfile)

    # TODO: Create image
    # TODO: Publish image
