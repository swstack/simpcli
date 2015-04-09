#!/usr/bin/env python

from lib.simpcli import simpcli, command, optional_argument, positional_argument


@optional_argument("opt", description="Optional argument")
@positional_argument(description="Positional argument one")
@command(description="Command description")
def cmd1(named_positional, named_optional='bar'):
    import sys
    print(sys.argv)
    print("Positional argument: %s" % named_positional)
    print("Optional argument: %s" % named_optional)


@command(description="Command description")
def cmd2():
    print('cmd2 exe')


if __name__ == "__main__":
    simpcli.load()
    simpcli.execute()
