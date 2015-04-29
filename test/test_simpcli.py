from simpcli.simpcli import simpcli, command, optional_argument, positional_argument
import unittest
import mock
import sys


class TestCommandLineInterface(unittest.TestCase):

    def _go(self, cmd, *positionals, **optionals):
        mocked_argv = [sys.argv[0], cmd]

        for value in positionals:
            mocked_argv.append(value)

        for name, value in optionals.items():
            mocked_argv.append("--%s" % name)
            mocked_argv.append(value)

        with mock.patch('sys.argv', mocked_argv):
            simpcli.load()
            simpcli.execute()

    def test_command_no_args(self):
        @command(description="Command help")
        def cmd(*args, **kwargs):
            self.assertEqual(args, ())
            self.assertEqual(kwargs, {})
        self._go('cmd')

    def test_positional_args(self):
        @positional_argument(description="Positional argument")
        @command(description="Command help")
        def cmd(pos):
            self.assertEqual(pos, 'foo')
        self._go('cmd', 'foo')

    def test_optional_args(self):
        @optional_argument("opt", description="Optional argument")
        @command(description="Command help")
        def cmd(opt=None):
            self.assertEqual(opt, 'bar')
        self._go('cmd', opt='bar')

    def test_optional_args_default(self):
        @optional_argument("opt", description="Optional argument")
        @command(description="Command help")
        def cmd(opt='baz'):
            self.assertEqual(opt, 'baz')
        self._go('cmd')

    def test_combined(self):
        @optional_argument("opt", description="Optional argument")
        @positional_argument(description="Positional argument")
        @command(description="Command help")
        def cmd(pos, opt='baz'):
            self.assertEqual(pos, 'foo')
            self.assertEqual(opt, 'bar')
        self._go('cmd', 'foo', opt='bar')
