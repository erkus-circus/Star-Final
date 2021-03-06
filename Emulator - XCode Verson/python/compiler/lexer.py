class Type:
    def __init__(self, a: str, b: str, c=False):
        self.name = a
        self.values = b
        self.stackable = c

    def isOfType(self, type: str) -> bool:
        return self.values.find(type) >= 0

    name = ""
    values = ""
    stackable: bool

class LexList:

    def __init__(self) -> None:
        self.index: int = -1
        self.length: int = 0
        self.types: list[str] = []
        self.vals: list[str] = []


    def add(self, type: str, val: str):
        self.types.append(type)
        self.vals.append(val)
        self.length += 1
    
    # checks if the current token has a newline character in it
    def isCurrentNewLine(self) -> bool:
        # TODO: this
        pass
    
    def expect(self, *types: Type):
        typeFound = False
        for i in types:
            if self.getType() == i.name:
                typeFound = True
                break
        if not typeFound:
            #error
            print("An Error occured", i.name, self.index)


    def getType(self) -> str:
        return self.types[self.index] if self.canRetrieve() else "EOF"

    def getVal(self) -> str:
        return self.vals[self.index] if self.canRetrieve() else "EOF"

    def stepUp(self, steps: int = 1):
        self.index += steps

    def stepDown(self, steps: int = 1):
        self.stepUp(-steps)

    # skips whitespace, whitespace must be on top
    # down is false, unless true then skip downwards instead of upwards
    def skipSpace(self, down: bool = False):
        if not self.canRetrieve() or self.getType() == "EOF":
            return
        if self.getType() == "SPACE":
            self.stepUp(-1 if down else 1)
        # check for comment type here
        # then skip comment
        if self.getType() == "EXPONENT":
            while not '\n' in self.getVal():
                self.stepUp()
            # skip the last space
            self.stepUp()
    
    # print out all of the lexed list
    def printOut(self):
        for i in range(self.length):
            print("(" + str(i) + ")" + self.vals[i] + ": " + self.types[i])
    

    # checks if you are able to retrieve a token
    def canRetrieve(self) -> bool:
        return self.index < self.length
    
    # checks if the current value is EOF
    def eof(self) -> bool:
        return self.getType() == "EOF"


class Types:
    ID = Type("ID", "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", 1)
    STRSEP = Type("STRSEP", "\"`'")
    NUM = Type("NUM", "1234567890", 1)
    SPACE = Type("SPACE", " \n\t", 1)
    QMARK = Type("QMARK", "?")
    COMMA = Type("COMMA", ",")
    EXPOMARK = Type("EXPOMARK", "!")
    PARENTH = Type("PARENTH", "()")
    CURLY_PAREN = Type("CURLY_PAREN", "{}")
    BRACKET = Type("BRACKET", "[]")
    # adding the = sign here to make my life much easier.
    COMPOPERATOR = Type("COMPOPERATOR", "<>=", 1)
    OPERATOR = Type("OPERATOR", "/*+-")
    PERIOD = Type("PERIOD", ".")
    USCORE = Type("USCORE","_")
    BSLASH = Type("BSLASH","\\")
    SEMICOL = Type("SEMICOL",";")
    TYPEOPER = Type("TYPEOPER","@")
    TILDE = Type("TILDE","~")
    EXPONENT = Type("EXPONENT", "^")
    # this is a special case, not included in list types
    STATEMENT = Type("STATEMENT", "")
    # maybe should add EOF type?]

types = [
	Types.ID,
	Types.STRSEP,
	Types.NUM,
	Types.SPACE,
	Types.QMARK,
    Types.COMMA,
	Types.EXPOMARK,
	Types.PARENTH,
	Types.CURLY_PAREN,
	Types.BRACKET,
    Types.COMPOPERATOR,
	Types.OPERATOR,
	Types.PERIOD,
	Types.USCORE,
	Types.BSLASH,
	Types.SEMICOL,
	Types.TILDE,
	Types.EXPONENT, 
    Types.TYPEOPER
]

statements = [
    "func",
	"var",
	"if",
	"return",
    "include"
]

def lex(text: str, linenum=0) -> LexList:
    index = 0

    lexed = LexList()

    lastType = "NULL"
    lastVal = "NULL"
    first = False

    length = len(text)

    done = False

    for i in range(length):
        c = text[i]

        theType = getCharType(c)
        typ = theType.name

        if typ == lastType and theType.stackable:
            lastVal += c
        else:
            if first:
                for j in range(len(statements)):
                    if statements[j] == lastVal:
                        lastType = "STATEMENT"
                lexed.add(lastType, lastVal)
            else:
                first = True
            
            lastType = typ
            lastVal = c
    for i in range(len(statements)):
        if statements[i] == lastVal:
            lastType = "STATEMENT"
    
    lexed.add(lastType, lastVal)

    lexed.add("EOF", "EOF")

    return lexed

def getCharType(char: str) -> Type:
    for i in range(len(types)):
        if types[i].isOfType(char):
            return types[i]
    return Type("NULL", "^")


if __name__ == "__main__":
    # an example program that i should use for reference when making the syntax tree and parsing through the LexList
    l = lex("""
    func sayHi@string (name@string, age@int) {
        var message@string = "Hi " + name + ". You are " + string(age) + " years old";
        print(message);
        ^ print the string message
    }
    """)

    l.printOut()