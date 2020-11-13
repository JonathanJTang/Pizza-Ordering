class InvalidOptionError(Exception):
    """ Exception that is raised when an invalid option is given."""

    def __init__(self, containing_class_name: str, option: str,
                 option_type: str) -> None:
        self.containing_class_name = containing_class_name
        self.option = option
        self.option_type = option_type

    def __str__(self) -> str:
        return "'{}' is not a valid {} option for {}".format(
            self.option, self.option_type, self.containing_class_name)
