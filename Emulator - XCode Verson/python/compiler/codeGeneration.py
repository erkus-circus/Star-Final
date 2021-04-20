"""
Takes a Node tree, from actionTree.py
Then converts it into a string containing the bytecode and data to be transpiled into actual bytecode
Eric Diskin
Created: 4-19-21, in TLP class
"""

from syntaxTree import Node
from createData import bytesFromNumber, createData
from actionTree import Function, functionData, specialFunctionData
constantsData = ""
output = ""



# wraps a bunch of code into a function
# 
def wrapInFunction(code: str, functionIndex: int) -> str:
    ## TODO: bytes from number gives it a 4 long hex, when it should be 2 long hex number.
    argumentsLen =  ' '.join(bytesFromNumber(len(functionData[functionIndex].paramTypes)).split()[2:])
    return "\nFUN_HEAD\n" + argumentsLen + "\n" + code + "\n"


def createExpression(expression: list[Node]) -> str:
    # the dictionary for comparing operators to their bytecode values.
    operatorDict = {
        '+': "IADD",
        '-': "ISUB",
        '*': "IMUL",
        '/': "IDIV",
        '%': "IMOD"
    }
    currentOutput = ""
    # loop through the expression and create an currentOutput
    for i in expression:
        if i.nodeName == "call":
            # do something special here.
            currentOutput += createCall(i)
        elif i.nodeName == "variableReference":
            currentOutput += '\n' + getString(i.name, "L_")
        elif i.nodeName == "constantReference":
            currentOutput += '\n' + getString(i.value, "C_")
        elif i.nodeName == "operator":
            currentOutput += '\n' + operatorDict[i.value]
    return currentOutput


def createCall(node: Node) -> str:
    currentOutput = ""

    # parse its arguments
    for i in node.children[0].children:
        currentOutput += '\n' + createExpression(i.children)

    # this is a builtin function.
    if node.special:
        currentOutput += '\n' + specialFunctionData[node.name].assembly
    else:
        # get call index
        currentOutput += '\n' + getString(node.name, "C_")
        # call the function
        currentOutput += '\n' + "CALL"
    return currentOutput

# turn like get 5 to C_5 or C_3 or if it is greater than 5, C_B 0x06 or something.
# number is the index of the string, prefix is the prefix like C_ or P_ or S_ or L_
def getString(number: int, prefix: str) -> str:
    if number <= 5:
        return prefix + str(number)
    else:
        # not sure if hex is the correct function, should work for now tho.
        return prefix + "B" + "\n" + hex(number)

def createVariableAssignment(node: Node) -> str:
    # the output for the expression
    currentOutput = ""
    # get expression as children.
    # node.children is the expression array
    ## should this work?
    if len(node.children)  > 0:
        # child length is greater than zero.
        currentOutput += createExpression(node.children[0].children)
    else:
        currentOutput += "\nZERO"
    currentOutput += "\n" + getString(node.name, "S_")
    return currentOutput

# create a higher level constants string, then output it
def createConstants(constants: list) -> str:
    global constantsData
    for i in constants:
        if type(i) == int:
            # int
            constantsData += "\nN " + str(i)
        else:
            # string uses less bits to hold values
            constantsData += "\nS " + i
    return createData(constantsData.strip())

# number of functions
functionCount = 0
## TODO variables are accessed in the variables array when they should be accessed from the parameters array. I need a fix to this.
def createBody(node: Node) -> str:
    global functionCount
    # the current output, this will go into wrapFunction to turn it into a function before going into the output.
    currentOutput = ""
    for i in node.children:
        # parse a variable declaration
        if i.nodeName == "varDeclaration" or i.nodeName == "assignment":
            currentOutput += createVariableAssignment(i)
        elif i.nodeName == "function":
            currentOutput += wrapInFunction(createBody(i.children[0]), functionIndex=functionCount)
            # increment the number of functiions parsed.
            functionCount += 1
        elif i.nodeName == "call":
            currentOutput += createCall(i)
    return currentOutput


def createCode(node: Node, variables: list[str], functions: list[str], functionData: list[str], constants: list):
    constants = createConstants(constants)
    functionsOut = createBody(node)
    # - 1 i think for function count?
    output = constants + str(' '.join(bytesFromNumber(functionCount).split()[2:])) + functionsOut
    return output