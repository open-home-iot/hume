import argparse


def parse_args():
    arg_parser = argparse.ArgumentParser(
        description='HUME, the HOME network hub'
    )

    arg_parser.add_argument('--clear-logs',
                            help="Clear out all logs produced by the logging "
                                 "application.",
                            action='store_true')

    args = arg_parser.parse_args()

    return args
