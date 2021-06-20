import argparse

from server.tcpserver import TCPServer


class Launcher(object):
    def __init__(self):
        args = self.__get_argument_parser().parse_args()
        self.server = TCPServer("", args.port)

    @staticmethod
    def __get_argument_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        # Required arguments
        parser.add_argument(
            "port",
            type=int,
            action="store",
            choices=range(0, 65535),
            help="Server port number",
        )

        return parser

    def run(self):
        self.server.run()


if __name__ == "__main__":
    launch = Launcher()
    launch.run()
