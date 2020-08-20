import sys
import wget
import logging
import argparse
import os
from os import environ

def main(args):
    fullpath=args.destination + '/' + args.source.split('/')[-1]
    logging.info('downloading ' + args.source + ' to ' + fullpath)
    wget.download(args.source, fullpath)

def get_arg(env, default):
    return os.getenv(env) if os.getenv(env, "") != "" else default

def parse_args(parser):
    args = parser.parse_args()
    args.source = get_arg('SOURCE_URL', args.source)
    args.destination = get_arg('DESTINATION_PATH', args.destination)
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('parsing args')
    parser = argparse.ArgumentParser(description='wget a file')
    parser.add_argument(
            '--source',
            help='Source URL, env variable SOURCE_URL',
            default='https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-07-16/metadata.csv')
    parser.add_argument(
            '--destination',
            help='Path for destination, env variable DESTINATION_PATH',
            default='/mnt/data')
    cmdline_args = parse_args(parser)
    main(cmdline_args)
    logging.info('exiting')
