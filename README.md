# simpcli (Simple CLI)

This library helps to build quick and dirty command line interfaces in Python
using Python's implementation of the decorator pattern (decorators).

## Examples

Expose a command to run unit tests

```py
@command(description='Run unit tests')
def test():
    import nose

    nose_cfg = os.path.join('etc', 'nose.cfg')
    sys.exit(nose.run_exit(argv=sys.argv + ['--config={}'.format(nose_cfg)]))

```

Expose a command which takes one positional and one optional argument:

```py
@optional_argument("opt", description="Optional argument")
@positional_argument(description="Positional argument one")
@command(description="Command description")
def cmd1(pos, opt='bar'):
    import sys
    print(sys.argv)
    print("Positional argument: %s" % pos)
    print("Optional argument: %s" % opt)
```
