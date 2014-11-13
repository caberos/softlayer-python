"""
    SoftLayer.tests.CLI.environment_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT, see LICENSE for more details.
"""

import click
import mock

from SoftLayer.CLI import environment
from SoftLayer.CLI import exceptions
from SoftLayer import testing


@click.command()
def fixture_command():
    pass


class EnvironmentTests(testing.TestCase):

    def set_up(self):
        self.env = environment.Environment()

    def test_list_commands(self):
        self.env.load()
        actions = self.env.list_commands()
        self.assertIn('vs', actions)
        self.assertIn('dns', actions)

    def test_get_command_invalid(self):
        self.assertRaises(exceptions.InvalidCommand,
                          self.env.get_command, 'invalid', 'command')

    def test_get_command(self):
        mod_path = 'SoftLayer.tests.CLI.environment_tests'
        fixture_loader = environment.ModuleLoader(mod_path, 'fixture_command')
        self.env.commands = {'fixture:run': fixture_loader}
        command = self.env.get_command('fixture', 'run')
        self.assertIsInstance(command, click.Command)

    def test_resolve_alias(self):
        self.env.aliases = {'aliasname': 'realname'}
        r = self.env.resolve_alias('aliasname')
        self.assertEqual(r, 'realname')

        r = self.env.resolve_alias('realname')
        self.assertEqual(r, 'realname')

    @mock.patch('SoftLayer.utils.console_input')
    def test_input(self, raw_input_mock):
        r = self.env.input('input')
        raw_input_mock.assert_called_with('input')
        self.assertEqual(raw_input_mock(), r)

    @mock.patch('getpass.getpass')
    def test_getpass(self, getpass):
        r = self.env.getpass('input')
        getpass.assert_called_with('input')
        self.assertEqual(getpass(), r)
