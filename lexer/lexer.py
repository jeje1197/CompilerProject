import string

class Position:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.idx = -1
        self.ln = 1
        self.col = 0
    
    def advance(self, cur_char):
        if cur_char == '\n':
            self.ln += 1
            self.col = 1
        else:
            self.col += 1
        self.idx += 1

    def copy(self):
        pos = Position(self.fn, self.text)
        pos.idx = self.idx
        pos.ln = self.ln
        pos.col = self.col
        return pos

    def __repr__(self):
        return f'ln: {self.ln}, col: {self.col} in {self.fn}'

class Token:
    def __init__(self, type, value, position):
        self.type = type
        self.value = value
        self.position = position

    def matches(self, tok_type=None, value=None):
        if tok_type and type(tok_type) is tuple:
            return self.type in tok_type

        if not value:
            return self.type == tok_type
        else:
            if type(value) is tuple:
                return self.value in value
            return self.value == value



    def __repr__(self) -> str:
        return f"({self.type}, {self.value})"


KEYWORDS = ['var', 'if', 'else if', 'else', 'while', 'fn', 'return',
        'continue', 'break', 'struct', 'cast']

escape_chars = {
    '\\': '\\',
    't': '\t',
    'n': '\n'
}

double_operators = {
    '<=', '>=', '==', '!=', '&&', '||' 
}

single_operators = {
    '+', '-', '*', '/', '%', '=', '<', '>', '!', '&'
}


class Lexer:
    def __init__(self, fn, text):
        self.text = text
        self.index = -1
        self.cur = None
        self.position = Position(fn, text)
        self.get_next()

    def has_next(self, steps_ahead=1) -> bool:
        """
        Returns true is there are more tokens to create
        """
        
        return self.index + steps_ahead < len(self.text)

    def get_next(self):
        """
        # Gets next character from text
        # If no characters are left, returns None
        """
        if self.has_next():
            self.index += 1
            self.position.advance(self.cur)
            self.cur = self.text[self.index]
        else: self.cur = None
        return self.cur

    def look_ahead(self, steps_ahead=1):
        """
        Gets next character from file text
        If no characters are left, returns None
        """
        if self.has_next(steps_ahead):
            return self.text[self.index + steps_ahead]
        else: 
            return '\\0'

    def get_tokens(self):
        """
        Returns a list of Token objects
        """
        tokens = []

        while self.cur:
            char = self.cur
            next2 = self.cur + self.look_ahead()

            if char in ' \n': # whitespace
                self.get_next()
                continue
            elif next2 == '//': # Comments
                self.get_next()
            elif char in string.ascii_letters + '_': # id or keyword
                start_pos = self.position.copy()
                id_str = ""
                
                while self.cur and self.cur in string.ascii_letters + string.digits + "_":
                    id_str += self.cur
                    self.get_next()
                

                if id_str in KEYWORDS:
                    tokens.append(Token('KEYWORD', id_str, start_pos))
                else:
                    tokens.append(Token('ID', id_str, start_pos))
                continue
            elif char in string.digits: # number
                start_pos = self.position.copy()
                num_str = ""

                has_dot = False
                while self.cur and self.cur in (string.digits + "."):
                    if self.cur == ".":
                        if has_dot:
                            break
                        else:
                            has_dot = True
                    num_str += self.cur
                    self.get_next()

                if has_dot:
                    tokens.append(Token('FLOAT', num_str, start_pos))
                else:
                    tokens.append(Token('INT', num_str, start_pos))
                continue
            elif char == '\'':
                start_pos = self.position.copy()
                self.get_next()

                new_char = ""
                if self.cur and not self.cur == '\'':
                    if self.cur == '\\':
                        self.get_next()
                        if self.cur in escape_chars:
                            new_char += escape_chars[self.cur]
                            self.get_next()
                        else:
                            raise Exception(f"Expected escape character after ;\\' {self.position}")
                    else:
                        new_char += self.cur
                        self.get_next()
                
                if not self.cur == '\'':
                    raise Exception(f"Expected closing quote {self.position}")
                self.get_next()

                tokens.append(Token('CHAR', new_char, start_pos))
                continue
            elif char == '"':
                start_pos = self.position.copy()
                self.get_next()
                
                new_str = ""
                while not self.cur == '"':
                    if self.cur == '\\':
                        self.get_next()
                        if self.cur in escape_chars:
                            new_str += escape_chars[self.cur]
                            self.get_next()
                        else:
                            raise Exception(f"Expected escape character after '\\' {self.position}")
                    else:
                        new_str += self.cur
                        self.get_next()
                self.get_next()
                tokens.append(Token('STRING', new_str, start_pos))
                continue
            elif char == '(':
                tokens.append(Token('LPAREN', char, self.position))
            elif char == ')':
                tokens.append(Token('RPAREN', char, self.position))
            elif char == '{':
                tokens.append(Token('LBRACE', char, self.position))
            elif char == '}':
                tokens.append(Token('RBRACE', char, self.position))
            elif char == '[':
                tokens.append(Token('LBRACKET', char, self.position))
            elif char == ']':
                tokens.append(Token('RBRACKET', char, self.position))
            elif char == ':':
                tokens.append(Token('COLON', char, self.position))
            elif char == ';':
                tokens.append(Token('SEMICOLON', char, self.position))
            elif char == ',':
                tokens.append(Token('COMMA', char, self.position))
            elif char == '.':
                tokens.append(Token('DOT', char, self.position))
            elif next2 in double_operators:
                tokens.append(Token('OP', next2, self.position))
                self.get_next()
            elif char in single_operators:
                tokens.append(Token('OP', char, self.position))
            else:
                raise Exception(f"Token not found {self.position}")

            self.get_next()

        tokens.append(Token('EOF', 'EOF', self.position))
        return tokens