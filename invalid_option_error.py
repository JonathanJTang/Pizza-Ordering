class InvalidOptionError(Exception):
    """ Exception that is raised when an invalid product option was given."""
    def __init__(self, option: str, option_type: str) -> None:
        self.option = option
        self.option_type = option_type

    def __str__(self) -> str:
        return f"'{self.option}' is not a valid Pizza {self.option_type} option"