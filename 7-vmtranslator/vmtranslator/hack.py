import enum


class MemorySegments(enum.Enum):
    ARGUMENT = "argument"
    LOCAL = "local"
    STATIC = "static"
    CONSTANT = "constant"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"


ARG_POINTER = "ARG"
LCL_POINTER = "LCL"
THIS_POINTER = "THIS"
THAT_POINTER = "THAT"

SEGMENT_POINTER_MAP = {
    MemorySegments.ARGUMENT: ARG_POINTER,
    MemorySegments.LOCAL: LCL_POINTER,
    MemorySegments.THIS: THIS_POINTER,
    MemorySegments.THAT: THAT_POINTER,
}
