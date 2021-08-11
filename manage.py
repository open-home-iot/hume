#!/usr/bin/env python3

import os
import sys
import argparse

import peewee


def parse_args():
    """
    Parse arguments provided at running the python program.
    """
    parser = argparse.ArgumentParser(
        description="HUME device controller"
    )

    parser.add_argument("-cdb",
                        "--clean-db",
                        action="store_true",
                        help="Clean all tables in local Postgres DB 'hume'")

    subparsers = parser.add_subparsers(help="supported commands")

    clean_db_parser = subparsers.add_parser("clean-db",
                                            help="Clean the local DB.")
    clean_db_parser.set_defaults(func=clean_db)

    clear_device_data_parser = subparsers.add_parser(
        "clear-device-data", help="Clear the local DB of all device data."
    )
    clear_device_data_parser.set_defaults(func=clear_device_data)

    return parser.parse_args()


"""
Subparsers below
"""


def clean_db(_):
    """
    Clean the local Postgres DB 'hume' of all table content. If new tables are
    added to HUME, they must be added here as well, I don't have the energy for
    fixing automatic discovery.

    :param _: CLI args
    """
    # Fix path to solve import errors
    root_path = os.getcwd()
    project_root = "hume"

    sys.path.append(f"{root_path}/{project_root}")

    from hume.device.models import Device, DeviceAddress
    from hume.hint.models import BrokerCredentials, HumeUser

    print("clearing the local Postgres DB 'hume' of all tables...\n")

    psql_db = peewee.PostgresqlDatabase("hume",
                                        user="hume",
                                        password="password")
    psql_db.connect()
    psql_db.drop_tables([Device, DeviceAddress, BrokerCredentials, HumeUser])

    # Remove the two added paths
    sys.path = sys.path[:-1]


def clear_device_data(_):
    """
    Clear the local DB of all device data, deleting the tables for
    re-definition at a later start.

    :param _: CLI args
    """
    # Fix path to solve import errors
    root_path = os.getcwd()
    project_root = "hume"

    sys.path.append(f"{root_path}/{project_root}")

    from hume.device.models import Device, DeviceAddress

    print("clearing the local Postgres DB 'hume' of all device tables...\n")

    psql_db = peewee.PostgresqlDatabase("hume",
                                        user="hume",
                                        password="password")
    psql_db.connect()
    psql_db.drop_tables([Device, DeviceAddress])

    # Remove the two added paths
    sys.path = sys.path[:-1]


if __name__ == "__main__":
    cli_args = parse_args()
    if cli_args.clean_db:
        clean_db(None)

    try:
        cli_args.func(cli_args)
    except AttributeError:
        print("no command specified...")
