# Project Phase 2.2
# By Jordan Somers and Sage Lee

#Imports
import re
import sys

#Global vars
iterator = 0
allTokens = []


  
#Tree class
class Tree():
  def __init__(self, data = None, left = None, right = None, middle = None):
    self.data = data
    self.left = left
    self.right = right
    self.middle = middle


def printTree(node, depth):
  output = ""
  if node.data[1] == "NONE":
    output += (node.data[0] + "\n")
  else:
    output += (node.data[0] + " : " + node.data[1] + "\n")
  output += ("\t\t")
  if(node.left != None):
    for i in range(depth):
      output += ("\t\t")
    output += printTree(node.left, depth+1)
  
  if(node.right != None):
    for i in range(depth):
      output += ("\t\t")
    output += printTree(node.right, depth+1)
  if(node.middle != None):
    for i in range(depth):
      output += ("\t\t")
    output += printTree(node.middle, depth+1)
  return output

def nextToken():
  return allTokens[iterator][1]

def nextTokenType():
  return allTokens[iterator][0]

def consumeToken():
  global iterator
  iterator += 1 

def parseStatement():
  t = parseBaseStatement()
  
  if(iterator == len(allTokens)):
    return t
  while nextToken() == ';':
    consumeToken()
    doubleSymbolCheck()
    t = Tree([';', "SYMBOL"], t, parseBaseStatement())
    if(iterator == len(allTokens)):
      break
  return t

def parseBaseStatement():
  if nextToken() == "skip":
    t = Tree(["SKIP", "NONE"])
    consumeToken()
    return t
  elif nextToken() == "while":
    t = parseWhileStatement()
  elif nextToken() == "if":
    t = parseIfStatement()
  elif nextTokenType() == "IDENTIFIER":
    t = parseAssignment()
  else:
    fileout.write("ERROR: Invalid Syntax")
    sys.exit(0)
  return t

def parseAssignment():
  identifier = Tree([nextToken(), "IDENTIFIER"])
  consumeToken()
  
  if(nextToken() != ":="):
    fileout.write("ERROR: Expected Token :=.")
    sys.exit(0)
  else:
    consumeToken()
    t = Tree([":=", "SYMBOL"], identifier, parseExpression())
    return t

def parseIfStatement():
  consumeToken() # Gets rid of "if"
  condition = parseExpression()
  if nextToken() != "then":
    fileout.write("ERROR: Expected Token \"then\".")
    sys.exit(0)
  consumeToken() # Gets rid of "then"
  ifState = parseStatement()
  if nextToken() != "else":
    fileout.write("ERROR: Expected Token \"else\".")
    sys.exit(0)
  consumeToken()
  elseState = parseStatement() # Gets rid of "else"
  if nextToken() != "endif":
    fileout.write("ERROR: Expected Token \"endif\".")
    sys.exit(0)
  consumeToken() # Gets rid of "endif"
  return(Tree(["IF-STATEMENT", "NONE"], condition, ifState, elseState))
  

def parseWhileStatement():
  consumeToken() # Gets rid of "while"
  condition = parseExpression()
  if nextToken() != "do":
    fileout.write("ERROR: Expected Token \"do\".")
    print(nextToken())
    sys.exit(0)
  consumeToken() # Gets rid of "do"

  whileState = parseStatement()
  if nextToken() != "endwhile":
    fileout.write("ERROR: Expected Token \"endwhile\".")
    sys.exit(0)
  consumeToken() # Gets rid of "endwhile"
  return(Tree(["WHILE-STATEMENT", "NONE"], condition, whileState))

def doubleSymbolCheck():
  if(iterator == len(allTokens)):
    return
  if(nextTokenType() == "SYMBOL"):
      fileout.write("ERROR: Cannot have two concurrent symbols.")
      sys.exit(0)

def parseExpression():
  t = parseTerm()
  if(iterator == len(allTokens)):
    return t
  while nextToken() == '+':
    consumeToken()
    doubleSymbolCheck()
    t = Tree(['+', "SYMBOL"], t, parseTerm())
    if(iterator == len(allTokens)):
      break
  return t

def parseTerm():
  t = parseFactor()
  if(iterator == len(allTokens)):
    return t
  while nextToken() == '-':
    consumeToken()
    doubleSymbolCheck()
    t = Tree(['-', "SYMBOL"], t, parseFactor())
    if(iterator == len(allTokens)):
      break
  return t
  
def parseFactor():
  t = parsePiece()
  if(iterator == len(allTokens)):
    return t
  while nextToken() == '/':
    consumeToken()
    doubleSymbolCheck()
    t = Tree(['/', "SYMBOL"], t, parsePiece())
    if(iterator == len(allTokens)):
      break
  return t
  
def parsePiece():
  t = parseElement()
  
  if(iterator == len(allTokens)):
    return t
  while nextToken() == '*':
    consumeToken()
    doubleSymbolCheck()
    t = Tree(['*', "SYMBOL"], t, parseElement())
    if(iterator == len(allTokens)):
      break
  return t
  
def parseElement():
  if(iterator == len(allTokens)):
    fileout.write("ERROR: Attempted to parse element when no tokens remain.")
    sys.exit(0)
  if nextToken() == ')':
    fileout.write("ERROR: Unexpected token ).")
    sys.exit(0)
  if nextToken() == '(':
    consumeToken()
    t = parseExpression()
    if(iterator == len(allTokens)):
      fileout.write("ERROR: Expected token \')\'.")
      sys.exit(0)
    if nextToken() == ')':
      consumeToken()
      return t
    else:
      fileout.write("ERROR: Expected token \')\'.")
      sys.exit(0)
  elif nextTokenType() == "NUMBER":
    t = Tree([nextToken(), "NUMBER"])
    consumeToken()
    if(iterator != len(allTokens)):
      if nextToken() == ')':
        fileout.write("ERROR: Unexpected token ).")
        sys.exit(0)
    return t
  elif nextTokenType() == "IDENTIFIER":
    t = Tree([nextToken(), "IDENTIFIER"])
    consumeToken()
    if(iterator != len(allTokens)):
      if nextToken() == ')':
        fileout.write("ERROR: Unexpected token ).")
        sys.exit(0)
    return t
  else:
    fileout.write("ERROR: Unexpected token " + str(nextToken()) + ".")
    sys.exit(0)
    

def scanLine(line):
    tokens = []
    words = line.split(" ")
    for word in words:
        word = re.sub("\n", "", word)
        word = re.sub("\t", "", word)
        while word != "":
            
            if re.search("^(if|then|else|endif|while|do|endwhile|skip)$", word):
                token = re.search("if|then|else|endif|while|do|endwhile|skip", word)
                tokens.append(["KEYWORD", token[0]])
                word = re.sub(token[0], "", word, 1)
            elif re.search("^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*", word):
                token = re.search("([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*", word)
                tokens.append(["IDENTIFIER", token[0]])
                word = re.sub(token[0], "", word, 1)
            elif re.match("^[0-9]+", word):
                token = re.search("[0-9]+", word)
                tokens.append(["NUMBER", token[0]])
                word = re.sub(token[0], "", word, 1)
            elif re.match("^\+|\-|\*|/|\(|\)|:=|;", word):
                token = re.search("\+|\-|\*|/|\(|\)|:=|;", word)
                tokens.append(["SYMBOL", token[0]])
                word = re.sub("\\" + token[0], "", word, 1) 
            else:
                tokens.append(["ERROR", word[0]])
                word = ""
                return tokens
    return tokens

#Input validation
if (len(sys.argv) != 3):
  print("ERROR: INVALID INPUT")
  sys.exit()
try:
  filein = open(sys.argv[1], "r+")
except OSError:
  print("ERROR: INVALID INPUT")
  sys.exit()
fileout = open(sys.argv[2], 'w')
lines = filein.readlines()
filein.close()
for line in lines:
    fileout.write("Line: " + line + "\n")
    for token in scanLine(line):
        allTokens.append(token)
        fileout.write("\t" + token[0] + ": " + token[1] + "\n")


AST = parseStatement()

fileout.write("\n\n" + printTree(AST, 0))
fileout.close()
