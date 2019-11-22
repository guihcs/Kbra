import string
from decimal import Decimal
from math import floor

# keywords and symbols to check in the tokenizer
keywords = (
    'if', 'else', 'while', 'repeat', 'for', 'to', 'continue', 'learn', 'break', 'return', 'None', 'wait', 'none')
symbols = ('!', '*', '(', ')', '-', '+', '=', '{', '}', '<', '>', '/', '^', ',', 'not', 'and', 'or')


# Token class to classify tokens
class Token(object):
    def __init__(self, token):
        self.value = token
        self.tok_type = self.get_type()
        pass

    # Avaliate and returns the token type
    def get_type(self):

        if self.value.lower() == 'true' or self.value.lower() == 'false':
            return "boolean"
        if self.value[0] == '\"':
            return "string"
        if is_number(self.value):
            return "number"
        if self.value in keywords:
            return "keyword"
        if self.value in symbols:
            return "symbol"
        if self.value[0] == '$' or self.value[0].isalpha():
            return "identifier"
        if self.value == '@':
            return 'special'
        return "Null"
        pass

    # Converts the token to its absolute value
    def get_value(self):
        if self.tok_type == "number":
            if '.' in self.value:
                return float(self.value)
            else:
                return int(self.value)
        if self.tok_type == "string":
            return self.value.strip('\"')
        if self.tok_type == "boolean":
            if self.value.lower() == "true" or self.value.lower() == "false":
                if self.value.lower() == 'true':
                    return True
                else:
                    return False
        if self.tok_type == "identifier":
            return self.value

        return None

    # Set the token representation in print method
    def __repr__(self):
        return "(\'%s\', %s)" % (self.value, self.tok_type)


# The tokenize function
def tokenize(text):
    # List declarations.
    raw_list = []
    id_token = []
    num_token = []

    # Gets permitted symbols in string
    valid_chars = string.punctuation.replace('\\', '')
    valid_chars = valid_chars.replace('%', '')
    invalid_symbols = ['@']
    # Iterate over all characters in text.
    for char in text:

        # check for invalid symbols
        if char in invalid_symbols: raise SyntaxError('Invalid symbol')
        # Check for comments
        if char == '#' and len(id_token) <= 0: break
        # Check for tabs
        if char == '\t': continue
        # if is alpha append to identifier.
        if char.isalpha() or char == '_':

            id_token.append(char)
            pass
        # check for starting strings or variable identifiers
        elif (char == '$' or char == '\"') and len(id_token) <= 0:
            id_token.append(char)
            pass
        # check for end of string with "
        elif char == '\"' and len(id_token) > 0 and id_token[0] == '\"':
            id_token.append(char)
            raw_list.append(''.join(id_token))
            id_token.clear()
            pass
        # check for chars that may appear inside the string
        elif (char.isspace() or char.isnumeric or char in valid_chars) and len(id_token) > 0 and id_token[0] == '\"':
            id_token.append(char)
        # Check for numeric constants.
        elif char.isnumeric() or len(num_token) > 0 and char == '.':
            if len(id_token) > 0:
                raw_list.append(''.join(id_token))
                id_token.clear()
            else:
                num_token.append(char)
        # Check the end of the identifier and add the character to the end.
        elif len(id_token) > 0:
            token = ''.join(id_token)
            raw_list.append(token.rstrip())
            id_token.clear()
            raw_list.append(char)
        # Check for number and append char to the end.
        elif len(num_token) > 0:
            raw_list.append(''.join(num_token))
            num_token.clear()
            raw_list.append(char)
        # Other chars must be symbols.
        else:
            raw_list.append(char)

    # Check if is a number or identifier that wasn't appended.
    if len(id_token) > 0:
        raw_list.append(''.join(id_token))
        pass
    elif len(num_token) > 0:
        raw_list.append(''.join(num_token))

    # Some spaces used to enclose tokens may remain. This line removes then.
    raw_list = [x for x in raw_list if x != ' ']
    token_list = [Token(x) for x in raw_list]
    return token_list


# gets the index of a token in a list
def index_of(key, tok_list):
    i = 0
    while i < len(tok_list):
        if tok_list[i].value == key:
            return i
        i += 1
    return -1


# check if number hav decimal value
def get_integer(value):
    try:
        if value is True or value is False:
            return value
        if Decimal(value) % 1 == 0:
            return floor(value)
        else:
            return value
    except Exception:
        return value


# function the check if a value is a number
def is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False
    pass


# check for tok occurrence in tok_list
def contains(tok, tok_list):
    for token in tok_list:
        if token.value == tok:
            return True
        pass
    pass
    return False


def contains_type(tok, tok_list):
    for token in tok_list:
        if token.tok_type == tok:
            return True
        pass
    pass
    return False

def replace_tok(old_tok, new_tok, tok_list, count):
    cur_count = 0
    for i in range(len(tok_list)):
        if cur_count >= count: return
        if old_tok.value == tok_list[i].value:
            tok_list[i] = new_tok
            cur_count += 1
