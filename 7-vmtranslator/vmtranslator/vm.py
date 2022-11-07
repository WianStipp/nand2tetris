import enum


class ArithmeticCommands(enum.Enum):
    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"


class VMCommandTypes(enum.Enum):
    """
    Defines the VM command types.
    """

    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"

    @classmethod
    def is_push(cls, cmd: "VMCommandTypes") -> bool:
        return cmd == VMCommandTypes.C_PUSH

    @classmethod
    def is_pop(cls, cmd: "VMCommandTypes") -> bool:
        return cmd == VMCommandTypes.C_POP
