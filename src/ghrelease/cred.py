
import os

from .log import logger

def get_credentials(args):
    """
    fetch the credentials from the given docopt args

    >>> get_credentials({"--user": "fred", "--password": "secret"})
    ("fred", "secret")

    >>> import os
    >>> os.environ["PASS"] = "secret-env"
    >>> get_credentials({"--user": "fred", "--password-env": "FOO"})
    ("fred", "secret-env")

    >>> import os
    >>> os.environ["USER"] = "fred-env"
    >>> get_credentials({"--user": "fred", "--password-env": "FOO"})
    ("fred-env", "secret")

    >>> import os
    >>> os.environ["PASS"] = "secret-env1"
    >>> os.environ["USER"] = "fred-env1"
    >>> get_credentials({"--user-env": "USER", "--password-env": "FOO"})
    ("fred-env1", "secret-env1")
    """
    username = args.get("--user")
    if not username:
        username = os.environ[args.get("--user-env")]

    password = args.get("--password")
    if not password:
        password = os.environ[args.get("--password-env")]
    return (username, password)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
