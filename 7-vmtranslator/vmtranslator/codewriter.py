"""Generates Hack assembly code from the parsed VM command."""

from vmtranslator import vmparser


class ASMCodeWriter:
    """
    Class to translate a parsed VM command into ASM.
    """

    def __init__(self, output_file_path: str) -> None:
        self.output = open(output_file_path, "w", encoding="utf-8")

    def write_arithmetic(self, command: str) -> None:
        """
        Writes to the output file the assembly code that implements
        the given arithmetic-logical command.
        """

    def write_push_pop(
        self, command: vmparser.PUSHPOP_CMD, segment: str, index: int
    ) -> None:
        """
        Writes to the output file the assembly code that implements
        the given push or pop command.
        """

    def close(self) -> None:
        """
        Closes the output file.
        """
        self.output.close()
