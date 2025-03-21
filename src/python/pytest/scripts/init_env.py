#!/usr/bin/env python

from os import path
import shutil
import sys

def main():
    target_file = '.env'
    if path.exists(target_file):
        print('Not modifying existing file: {}'.format(target_file))
        return 1

    template_file = 'dotenv-template'
    shutil.copyfile(template_file, target_file)
    print('Initialied environment settings in {}'.format(target_file))
    print('Please edit to fill in your own values.')
    return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
