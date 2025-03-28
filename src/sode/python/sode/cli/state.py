class MainState:
    _argv: list[str]

    def __init__(self, argv: list[str]):
        self._argv = argv

    @property
    def arguments(self) -> list[str]:
        return self._argv[1:]

    @property
    def program_name(self) -> str:
        return self._argv[0]
