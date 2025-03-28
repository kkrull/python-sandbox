class MainState:
    _argv: list[str]

    def __init__(self, argv: list[str]):
        self._argv = argv

    def arguments(self) -> list[str]:
        return self._argv[1:]

    def program_name(self) -> str:
        return self._argv[0]
