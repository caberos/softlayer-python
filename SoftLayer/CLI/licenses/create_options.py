"""Licenses order options for a given VMware licenses."""
# :license: MIT, see LICENSE for more details.

import click

from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.managers import licenses
from SoftLayer import utils


@click.command()
@environment.pass_env
def cli(env):
    """Server order options for a given chassis."""

    licenses_manager = licenses.LicensesManager(env.client)

    options = licenses_manager.get_create_options()

    table = formatting.Table(['Id', 'description', 'keyName', 'recurringFee'])
    for item in options:
        table.add_row([item.get('id'),
                       utils.trim_to(item.get('description'), 40),
                       item.get('keyName'),
                       item.get('prices')[0]['recurringFee']])

    env.fout(table)
