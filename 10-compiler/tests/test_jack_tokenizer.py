from lxml import etree as et

from jack_compiler.jack_tokenizer import JackTokenizer
from jack_compiler.lexicon import KeywordTypes, Symbols, TokenType

PATH_TO_SQUARE_JACK = '../../official_nand2tetris/nand2tetris/projects/10/Square/Main.jack'
PATH_TO_SQUARE_XML = '../../official_nand2tetris/nand2tetris/projects/10/Square/MainT.xml'

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
    
def test_jack_tokenizer():
    tokenizer = JackTokenizer(PATH_TO_SQUARE_JACK)
    tester = TokenizerXmlTester(tokenizer)
    with open(PATH_TO_SQUARE_XML, 'r') as f:
        answer = et.fromstring(f.read())
        answer = et.tostring(answer).decode()
    answer_lines = answer.split("\n")[1:-1]
    tokenized = et.tostring(tester.emit_xml(), pretty_print=True).decode()
    tokenized_lines = [e.strip() for e in tokenized.split('\n')[1:-2]]
    assert tokenized_lines == answer_lines

if __name__ == "__main__":
    test_jack_tokenizer()
