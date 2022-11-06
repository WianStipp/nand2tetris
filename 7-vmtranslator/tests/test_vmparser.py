"""Unit test for testing VMParser"""

from vmtranslator import vmparser


class TestVMParser:
    def test_advance(self):
        parser = vmparser.VMParser("tests/pushpop_test.vm")
        assert parser.has_more_lines()
        parser.advance()
        assert parser._current_line == "push local 1"

    def test_push(self):
        parser = vmparser.VMParser("tests/pushpop_test.vm")
        parser.advance()
        assert parser.command_type() == vmparser.VMCommandTypes.C_PUSH

    def test_pop(self):
        parser = vmparser.VMParser("tests/pushpop_test.vm")
        parser.advance()
        parser.advance()
        assert parser.command_type() == vmparser.VMCommandTypes.C_POP

    def test_arithmetic(self):
        parser = vmparser.VMParser("tests/pushpop_test.vm")
        parser.advance()
        parser.advance()
        parser.advance()
        assert parser.command_type() == vmparser.VMCommandTypes.C_ARITHMETIC

    def test_arg1(self):
        parser = vmparser.VMParser("tests/pushpop_test.vm")
        parser.advance()
        assert parser.arg1() == "local"
        parser.advance()
        assert parser.arg1() == "pointer"

    def test_arg2(self):
        parser = vmparser.VMParser("tests/pushpop_test.vm")
        parser.advance()
        assert parser.arg2() == "1"
        parser.advance()
        assert parser.arg2() == "0"
