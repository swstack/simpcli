# TODO: Add flag-type argument decorator (e.g. action=store_true)
# TODO: Implement argument types

import argparse
import sys
import inspect


def _print_command_list(commands):
    """Print formatted list of available commands"""

    indented_commands = ""
    for cmd, info  in commands.items():
        indented_commands += "    {} - {}\n".format(cmd, info['args'])
    message = "Choose from commands: \n{}".format(indented_commands)
    print(message)


class _SimpleCli(object):
    """Core component of simpcli

    The ``SimpleCli`` implements a subparser to offer a name-based command
    executor from the command line.  If you'd like to alter the "root" lever parser
    there are utilities to do so.  See usage for more details.

    """

    def __init__(self, name=''):
        self._root_parser = argparse.ArgumentParser(prog=name)
        self._command_parsers = self._root_parser.add_subparsers(help="Commands")
        self._commands = {}

    def add_command(self, name, args, description, handler):
        """Extend ``SimpleCli`` with a command"""

        if self._commands.get(name, None) is not None:
            raise Exception("Command {} already registered".format(name))

        self._commands[name] = {
            "args": args,
            "description": description,
            "handler": handler,
            "positionals": [],
            "optionals": [],
        }

    def add_positional_argument(self, command_name, description):
        """Add an argument to an existing command"""

        cmd = self._commands.get(command_name, None)
        if cmd:
            cmd['positionals'].append({
                'description': description,
            })

    def add_optional_argument(self, command_name, name, description):
        """Add an argument to an existing command"""

        cmd = self._commands.get(command_name, None)
        if cmd:
            cmd['optionals'].append({
                'name': name,
                'description': description,
            })

    def load(self):
        """Load the ``SimpleCli`` from decorated functions"""

        for name, cmd in self._commands.items():

            # Setup command parser
            cmd_parser = self._command_parsers.add_parser(name, help=cmd['description'])
            cmd_parser.set_defaults(sub_handler=cmd['handler'])

            # Setup positional arguments for this command
            for position, positional in enumerate(cmd['positionals']):
                cmd_parser.add_argument("<pos{}>".format(position + 1),
                                        help=positional['description'])

            # Setup optional arguments for this command
            for optional in cmd['optionals']:
                cmd_parser.add_argument("--%s" % optional['name'],
                                        help=optional['description'])

    def execute(self):
        """Execute one command from command line

        This calls the command specified in sys args (first positional arg).  The
        command specified should match a ``command`` user-decorated function.
        """

        if len(sys.argv) == 1:
            _print_command_list(self._commands)
            return 1

        cli_args = self._root_parser.parse_args()
        cmd = self._commands.get(cli_args.sub_handler.__name__, None)
        if cmd:
            # Build positional arguments
            pos_args = []
            for position, positional in enumerate(cmd['positionals']):
                arg_val = getattr(cli_args, "<pos{}>".format(position + 1))
                pos_args.append(arg_val)

            # Build optional arguments
            opt_args = {}
            for optional in cmd['optionals']:
                value = getattr(cli_args, optional['name'])
                if value is not None:
                    opt_args[optional['name']] = value

        cli_args.sub_handler(*pos_args, **opt_args)

    def add_root_argument(self, *args, **kwargs):
        """Add an argument to the root argument parser, typically not needed"""

        self._root_parser.add_argument(*args, **kwargs)


class command(object):
    """Decorator for adding a command to ``SimpleCli``"""

    def __init__(self, description=''):
        self._description = description

    def __call__(self, handler):
        simpcli.add_command(handler.__name__,
                            inspect.getargspec(handler)[0],
                            self._description,
                            handler)
        return handler


class positional_argument(object):
    """Decorator for adding a positional argument to a ``SimpleCli`` command"""

    def __init__(self, description='', type=None):
        self._description = description
        self._type = type

    def __call__(self, handler):
        simpcli.add_positional_argument(handler.__name__,
                                        self._description)
        return handler


class optional_argument(object):
    """Decorator for adding an optional argument to a ``SimpleCli`` command"""

    def __init__(self, name, description='', type=None):
        self._name = name
        self._description = description
        self._type = type

    def __call__(self, handler):
        simpcli.add_optional_argument(handler.__name__,
                                      self._name,
                                      self._description)
        return handler


simpcli = _SimpleCli()
