# Creating class without inherting from provided library
#   Should create exact result as described, with slightly vary implementation
class SM:
    def __init__(self):
        pass
    def start(self):
        self.result = []
        self.currToken = ""
    def stop(self):
        pass
    def step(self, action):
        print("STEP IN PARENT", action)
        pass

    def transduce(self, procedures):
        self.start()
        for procedure in procedures:
            self.step(procedure)
        self.stop()
        print(self.result)
        return self.result

class Tokenizer(SM):
    def step(self, action):
        if action == ' ':
            if len(self.currToken) != 0:
                self.result.append(self.currToken)
                self.currToken = ""
            return
        if action in seps:
            if len(self.currToken) != 0:
                self.result.append(self.currToken)
                self.currToken = ""
            self.result.append(action)
        else:
            self.currToken += action
            self.result.append('')


class BinaryOp:
    # opStr = '%' # ???  Validation required
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

class Sum(BinaryOp):
    opStr = 'Sum'
    def eval(self, env):
        leftEval = self.left.eval(env)
        rightEval = self.right.eval(env)
        if isNum(leftEval) and isNum(rightEval):
            return leftEval + rightEval
        return Sum(leftEval, rightEval)


class Prod(BinaryOp):
    opStr = 'Prod'
    def eval(self, env):
        leftEval = self.left.eval(env)
        rightEval = self.right.eval(env)
        if isNum(leftEval) and isNum(rightEval):
            return leftEval * rightEval
        return Prod(leftEval, rightEval)

class Quot(BinaryOp):
    opStr = 'Quot'
    def eval(self, env):
        leftEval = self.left.eval(env)
        rightEval = self.right.eval(env)
        if isNum(leftEval) and isNum(rightEval):
            return leftEval / rightEval
        return Quot(leftEval, rightEval)

class Diff(BinaryOp):
    opStr = 'Diff'
    def eval(self, env):
        leftEval = self.left.eval(env)
        rightEval = self.right.eval(env)
        if isNum(leftEval) and isNum(rightEval):
            return leftEval - rightEval
        return Diff(leftEval, rightEval)

class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self, env):
        varName = self.left.name
        varValue = self.right
        env[varName] = varValue
        # Prefer return varValue 
        #   returning None to match the homework document
        return None

class UnknownOp(BinaryOp):
    opStr = 'UnknownOp'
    def eval(self, _):
        return -1
        
class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    def eval(self, _):
        return self.value
    __repr__ = __str__

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    def eval(self, env):
        if self.name not in env:
            return self
        value = env[self.name]
        if isNum(value):
            return value
        return value.eval(env)
    __repr__ = __str__

# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize(string):
    # <your code here>
    tokenList = []
    currToken = ""
    for char in string:
        if char == ' ':
            if len(currToken) != 0:
                tokenList.append(currToken)
                currToken = ""
            continue

        if char in seps:
            if len(currToken) != 0:
                tokenList.append(currToken)
                currToken = ""
            tokenList.append(char)
        else:
            currToken += char
    if len(currToken) != 0:
        tokenList.append(currToken)

    return tokenList

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
# TODO
def parse(tokens):
    def parseExp(index):
        # Number:
        if numberTok(tokens[index]):
            return (Number(float(tokens[index])), index+1)
        elif variableTok(tokens[index]):
            return (Variable(tokens[index]), index+1)
        (parsedExp1, nextIndex) = parseExp(index+1)
        opt = tokens[nextIndex]
        (parsedExp2, nextIndex) = parseExp(nextIndex+1) 
        if opt == '+':
            resultExp = Sum(parsedExp1, parsedExp2)
            pass
        elif opt == '-':
            resultExp = Diff(parsedExp1, parsedExp2)
            pass
        elif opt == '*':
            resultExp = Prod(parsedExp1, parsedExp2)
            pass
        elif opt == '/':
            resultExp = Quot(parsedExp1, parsedExp2)
            pass
        elif opt == '=':
            resultExp = Assign(parsedExp1, parsedExp2)
            pass
        else:
            resultExp = UnknownOp(parsedExp1, parsedExp2)
            pass
        return (resultExp, nextIndex+1) # index + 1 to skip the last ')' char
        
    (parsedExp, _) = parseExp(0)
    return parsedExp

# token is a string
# returns True if contains only digits
def numberTok(token):
    return token.isdigit()

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char.isalpha(): return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = input('%')            # prints %, returns user input
        print('%', e) # your expression here)
        print('   env =', env)

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print('%', e)                    # e is the experession 
        print(parse(tokenize(e)).eval(env))# your expression here
        print('   env =', env)

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print(tokenize('fred '))
    print(tokenize('777 '))
    print(tokenize('777 hi 33 '))
    print(tokenize('**-)('))
    print(tokenize('( hi * ho )'))
    print(tokenize('(fred + george)'))
    print(tokenize('(hi*ho)'))
    print(tokenize('( fred+george )'))

# Tokenizer().transduce("fred ")
# Tokenizer().transduce("777 ")
# Tokenizer().transduce("777 hi 33 ")
# Tokenizer().transduce("**-)( ")
# Tokenizer().transduce("(hi*ho) ")
# Tokenizer().transduce("(fred + george) ")



# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print(parse(['a']))
    print(parse(['888']))
    print(parse(['(', 'fred', '+', 'george', ')']))
    print(parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')']))
    print(parse(tokenize('((a * b) / (cee - doh))')))
    print(parse(tokenize('(a = (3 * 5))')))


####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable('a'), Number(5.0)).eval(env)
    print(Variable('a').eval(env))
    env['b'] = 2.0
    print(Variable('b').eval(env))
    env['c'] = 4.0
    print(Variable('c').eval(env))
    print(Sum(Variable('a'), Variable('b')).eval(env))
    print(Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env))
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print(Variable('a').eval(env))
    print(env)

 
# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
# TODO
# def testLazyEval():
#     env = {}
#     Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
#     print Variable('a').eval(env)
#     env['b'] = Number(2.0)
#     print Variable('a').eval(env)
#     env['c'] = Number(4.0)
#     print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
