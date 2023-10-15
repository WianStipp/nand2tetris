import enum


class TokenType(str, enum.Enum):
  KEYWORD = 'keyword'
  SYMBOL = 'symbol'
  IDENTIFIER = 'identifier'
  INT_CONST = 'int_constant'
  STRING_CONST = 'string_const'
  
class KeywordTypes(str, enum.Enum):
  CLASS = "class"
  CONSTRUCTOR = "constructor"
  FUNCTION = "function"
  METHOD = 'method'
  FIELD = 'field'
  STATIC = 'static'
  VAR = 'var'
  INT = 'int'
  CHAR = 'char'
  BOOLEAN = 'boolean'
  VOID = 'void'
  TRUE = 'true'
  FALSE = 'false'
  NULL = 'null'
  THIS = 'this'
  LET = 'let'
  DO = 'do'
  IF = 'if'
  ELSE = 'else'
  WHILE = 'while'
  RETURN = 'return'


class Symbols(str, enum.Enum):
  LEFT_CURLY = "{"
  RIGHT_CURLY = "}"
  LEFT_PAREN = "("
  RIGHT_PAREN = ")"
  LEFT_SQR_PAREN = "["
  RIGHT_SQR_PAREN = "]"
  PERIOD = "."
  COMMA = ','
  SEMICOLON = ';'
  PLUS = "+"
  MINUS = "-"
  ASTERISK = "*"
  FORWARD_SLASH = "/"
  AMPERSAND = '&'
  PIPE = '|'
  LT = "<"
  GT = ">"
  EQ = "="
  TILDA = "~"

  @classmethod
  def is_op(cls, v: 'Symbols'):
    return v in [cls.PLUS, cls.MINUS, cls.ASTERISK, cls.FORWARD_SLASH \
                 , cls.AMPERSAND, cls.PIPE, cls.LT, cls.GT, cls.EQ, cls.TILDA]
  @classmethod
  def is_unary_op(cls, v: 'Symbols'):
    return v in [cls.MINUS, cls.TILDA]

