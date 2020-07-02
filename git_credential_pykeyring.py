from __future__ import print_function

import sys

import keyring

COMMANDS = {"get", "store", "erase"}


def main(args = None):
    if args is None:
        args = sys.argv[1:]
    if not args or args[-1] not in COMMANDS:
        print("Invalid usage", file=sys.stderr)
        return 1

    command = args.pop()

    stdin_args = read_stdin_args()
    url = "%(protocol)s://%(host)s" % stdin_args
    if "path" in stdin_args:
        url = "/".join((url, stdin_args["path"]))

    service = "git-credential-pykeyring+" + url

    if command == "get":
        username = stdin_args.get("username")
        if hasattr(keyring, "get_credential"):
            credential = keyring.get_credential(service, username)
            if credential is None:
                return 0

            username = credential.username
            password = credential.password
        else:
            password = keyring.get_password(service, username)
            if password is None:
                return 0

        if "username" not in stdin_args and username is not None:
            print("username=" + username)
        print("password=" + password)

    elif command == "store":
        keyring.set_password(service, stdin_args["username"], stdin_args["password"])

    elif command == "erase":
        keyring.delete_password(service, stdin_args["username"])


def read_stdin_args():
    args = {}
    while True:
        line = sys.stdin.readline().rstrip("\r\n")
        if not line:
            break

        key, value = line.split("=", 1)
        args[key] = value

    return args


if __name__ == "__main__":
    sys.exit(main())
