from typing import Tuple, List
import os
import glob
from lxml import etree as et

from jack_compiler.jack_tokenizer import JackTokenizer
from jack_compiler.lexicon import TokenType

ARRAYTEST_DIR_PATH = '../../official_nand2tetris/nand2tetris/projects/10/ArrayTest'
SQUARE_DIR_PATH = '../../official_nand2tetris/nand2tetris/projects/10/Square'
EXPRESSIONLESS_SQUARE_PATH = '../../official_nand2tetris/nand2tetris/projects/10/ExpressionLessSqure'


class TokenizerXmlTester:
    def __init__(self, tokenizer: JackTokenizer) -> None:
        self.tokenizer = tokenizer
    
    def emit_xml(self) -> et.Element:
        root = et.Element("tokens")
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.token_type() == TokenType.IDENTIFIER:
                e = et.Element('identifier')
                e.text = f" {self.tokenizer.identifier()} "
            elif self.tokenizer.token_type() == TokenType.INT_CONST:
                e = et.Element('integerConstant')
                e.text = f" {self.tokenizer.int_val()} "
            elif self.tokenizer.token_type() == TokenType.KEYWORD:
                e = et.Element('keyword')
                e.text = f" {self.tokenizer.keyword().value} "
            elif self.tokenizer.token_type() == TokenType.STRING_CONST:
                e = et.Element('stringConstant')
                e.text = f" {self.tokenizer.string_val()} "
            elif self.tokenizer.token_type() == TokenType.SYMBOL:
                e = et.Element('symbol')
                e.text = f" {self.tokenizer.symbol().value} "
            else:
                raise ValueError(f"Didn't recognize token type {self.tokenizer.token_type=}")
            root.append(e)
        return root

def get_inputs_and_expected_paths(dir_path: str) -> List[Tuple[str, str]]:
    jack_files = glob.glob(f"{dir_path}/*.jack")
    token_xml_files = [path.replace('.jack', 'T.xml') for path in jack_files]
    return list(zip(jack_files, token_xml_files))
    
    
def check_tokenization(input_path: str, output_path: str):
    tokenizer = JackTokenizer(input_path)
    tester = TokenizerXmlTester(tokenizer)
    with open(output_path, 'r') as f:
        answer = et.fromstring(f.read())
        answer = et.tostring(answer).decode()
    answer_lines = answer.split("\n")[1:-1]
    tokenized = et.tostring(tester.emit_xml(), pretty_print=True).decode()
    tokenized_lines = [e.strip() for e in tokenized.split('\n')[1:-2]]
    assert tokenized_lines == answer_lines

def test_square_tokenization():
    paths = get_inputs_and_expected_paths(SQUARE_DIR_PATH)
    for input_, out in paths:
        check_tokenization(input_, out)

def test_arraytest_tokenization():
    paths = get_inputs_and_expected_paths(ARRAYTEST_DIR_PATH)
    for input_, out in paths:
        check_tokenization(input_, out)


def test_expressionless_square_tokenization():
    paths = get_inputs_and_expected_paths(EXPRESSIONLESS_SQUARE_PATH)
    for input_, out in paths:
        check_tokenization(input_, out)
