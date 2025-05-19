# Παπακυριακού Βασίλειος, 5324, cs215324
# Νικόλαος Μιχαήλ Βασιλείου, 5186, cs215186

import sys

# Token class - holds data about tokens (family, recognised_string, line_number)

class Token:

    # Constructor
    def __init__(self, recognised_string, family, line_number):
        self.family = family
        self.recognised_string = recognised_string
        self.line_number = line_number

    def __str__(self):
        return f"String: {self.recognised_string} | Family: {self.family} | Line: {self.line_number}"


# Symbol table helper methods

# Entity class - entity representation in the symbol table (variable, function, procedure entity)

class Entity:

    # Constructor
    def __init__(self, name, type, startingQuad):
        self.name = name    # Entity name
        self.type = type    # Entity type
        self.startingQuad = startingQuad    # Starting quad for functions or procedures

        self.argumentList = []  # List of arguments for functions or procedures
        self.offset = 0     # Offset for memory
        self.framelength = 0    # Total frame length
        self.parMode = ""   # Parameter mode (pass by value or pass by reference) if dealing with a parameter type

# Scope class - scope representation in the symbol table (global, function scope)

class Scope:

    # Constructor
    def __init__(self, nestingLevel):
        self.nestingLevel = nestingLevel    # Depth level for the scope
        self.listEntity = []            # List of entities for the scope
        self.framelength = 12           # Starting framelength


# Argument class - formal parameter representation of a function (or procedure)

class Argument:

    # Constructor
    def __init__(self, parMode, type):
        self.parMode = parMode  # parameter mode (value or reference)
        self.type = type


# FinalCodeGen class - Final RISC-V code generator

class FinalCodeGen:

    def __init__(self, quad_list, symbol_table):

        self.quad_list = quad_list
        self.symbol_table = symbol_table
        self.output_lines = []  # List of assembly lines (to write at the .asm file)
        self.output_lines.append(".data\n")
        self.output_lines.append("str_nl: .asciz \"\\n\"\n")
        self.output_lines.append(".text\n")

        self.current_scope = self.symbol_table.scopes[-1]  # Current scope is the last scope from the symbol table


    def gnlvcode(self, variable):
        # Get the entity and its scope from the symbol table
        tempScope, tempEntity = self.symbol_table.searchEntity(variable)
        x = ""
        x += "      lw t0,-4(sp) \n"

        levels = len(self.symbol_table.scopes) - tempScope.nestingLevel - 2
        for i in range(levels):
            x += "      lw t0,-4(t0) \n"
        x += f"      addi t0,t0,-{tempEntity.offset} \n"

        self.output_lines.append(x)


    def loadvr(self, value, register):
        if str(value).isdigit():  # If the value is a digit, load directly into the register
            self.output_lines.append(f"      li {register},{value} \n")  # "li register, integer"
        else:
            # Get the entity and its scope from the symbol table
            tempScope, tempEntity = self.symbol_table.searchEntity(value)
            level = tempScope.nestingLevel

            if level == self.symbol_table.depth and (
                    tempEntity.type == "temporary" or tempEntity.type == "είσοδος" or tempEntity.type == "parameter"):
                self.output_lines.append(f"      lw {register},-{tempEntity.offset}(sp) \n")
            elif level == self.symbol_table.depth and tempEntity.type == "έξοδος":
                self.output_lines.append(f"      lw t0,-{tempEntity.offset}(sp) \n")
                self.output_lines.append(f"      lw {register},(t0) \n")
            elif level == 0 and tempEntity.type == "parameter":
                self.output_lines.append(f"      lw {register},-{tempEntity.offset}(gp) \n")
            elif level < self.symbol_table.depth and (tempEntity.type == "είσοδος" or tempEntity.type == "parameter"):
                self.gnlvcode(value)  # Call your existing gnlvcode method
                self.output_lines.append(f"      lw {register},(t0) \n")
            elif level < self.symbol_table.depth and tempEntity.type == "έξοδος":
                self.gnlvcode(value)  # Call your existing gnlvcode method
                self.output_lines.append(f"      lw t0,(t0) \n")
                self.output_lines.append(f"      lw {register},(t0) \n")


    def storerv(self, register, value):
        # Store value from register into variable location
        tempScope, tempEntity = self.symbol_table.searchEntity(value)
        level = tempScope.nestingLevel

        if level == self.symbol_table.depth and (
                tempEntity.type == "temporary" or tempEntity.type == "είσοδος" or tempEntity.type == "parameter"):
            self.output_lines.append(f"      sw {register},-{tempEntity.offset}(sp) \n")
        elif level == self.symbol_table.depth and tempEntity.type == "έξοδος":
            self.output_lines.append(f"      lw t0,-{tempEntity.offset}(sp) \n")
            self.output_lines.append(f"      sw {register},(t0) \n")
        elif level == 0 and tempEntity.type == "parameter":
            self.output_lines.append(f"      sw {register},-{tempEntity.offset}(gp) \n")
        elif level < self.symbol_table.depth and (
                tempEntity.type == "είσοδος" or tempEntity.type == "parameter"):
            self.gnlvcode(value)
            self.output_lines.append(f"      sw {register},(t0) \n")
        elif level < self.symbol_table.depth and tempEntity.type == "έξοδος":
            self.gnlvcode(value)
            self.output_lines.append(f"      lw t0,(t0) \n")
            self.output_lines.append(f"      sw {register},(t0) \n")


    def assemblyBlock(self, block_name, start_quad):
        start_index = int(start_quad[0])

        for quad in self.quad_list[start_index - 1:]:
            self.output_lines.append(f"L{quad[0]}: \n")
            self.generateAssembly(quad, block_name)


    def generateAssembly(self, quad, blockName):

        global program_name
        global paramSetupDone
        global paramList

        op, x, y, z = quad[1], quad[2], quad[3], quad[4]

        if op == "jump":
            self.output_lines.append(f"      b L{z} \n")

        elif op == "+":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     add t1,t1,t2 \n")
            self.storerv("t1", z)


        elif op == "-":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     sub t1,t1,t2 \n")
            self.storerv("t1", z)

        elif op == "*":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     mul t1,t1,t2 \n")
            self.storerv("t1", z)

        elif op == "/":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     div t1,t1,t2 \n")
            self.storerv("t1", z)

        elif op == "=":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     beq t1,t2,L{z} \n")

        elif op == "<>":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     bne t1,t2,L{z} \n")

        elif op == "<":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     blt t1,t2,L{z} \n")

        elif op == ">":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     bgt t1,t2,L{z} \n")

        elif op == "<=":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     ble t1,t2,L{z} \n")

        elif op == ">=":
            self.loadvr(x, "t1")
            self.loadvr(y, "t2")
            self.output_lines.append(f"     bge t1,t2,L{z} \n")

        elif op == ":=":
            self.loadvr(x, "t1")
            self.storerv("t1", z)

        elif op == "in":
            self.output_lines.append(f"     li a7,5\n")
            self.output_lines.append(f"     ecall\n")
            self.storerv("a0", x)  # Store result from a0 into x

        elif op == "out":
            self.loadvr(x, "a0")  # Move value to be printed into a0
            self.output_lines.append(f"     li a7,1\n")
            self.output_lines.append(f"     ecall\n")
            # Print newline
            self.output_lines.append(f"     la a0,str_nl\n")
            self.output_lines.append(f"     li a7,4\n")
            self.output_lines.append(f"     ecall\n")

        elif op == "retv":
            self.loadvr(x, "t1")
            self.output_lines.append(f"     lw t0,-8(sp)\n")
            self.output_lines.append(f"     sw t1,(t0)\n")

        elif op == "halt":
            self.output_lines.append(f"     li a0,0\n")
            self.output_lines.append(f"     li a7,93\n")
            self.output_lines.append(f"     ecall\n")

        elif op == "begin_block":
            framelength = self.symbol_table.scopes[0].framelength
            if (program_name == blockName):
                self.output_lines.append(f"      addi sp,sp,{framelength} \n")
                self.output_lines.append(f"      mv gp,sp \n")
            else:
                self.output_lines.append(f"      sw ra,-0(sp) \n")

        elif op == "end_block":
            if program_name != blockName:
                self.output_lines.append(f"      lw ra,-0(sp) \n")
                self.output_lines.append(f"      jr ra \n")

        elif op == "par":
            if paramSetupDone == False:

                callQuadIndex = int(quad[0])
                paramNum = 0

                while callQuadIndex < len(self.quad_list) and self.quad_list[callQuadIndex - 2][1] != "call":
                    paramNum += 1
                    paramList.append(paramNum)
                    callQuadIndex += 1

                calleeName = self.quad_list[callQuadIndex - 2][2]

                calleeScope, calleeEntity = self.symbol_table.searchEntity(calleeName)
                calleeOffset = calleeEntity.offset
                self.output_lines.append(f"      addi fp,sp,{calleeOffset} \n")
                paramSetupDone = True

            if blockName != program_name:  # If we re not in the main program get the current blocks scope and framelength
                callerScope, callerEntity = self.symbol_table.searchEntity(blockName)
                callerFramelength = callerEntity.framelength
                callerScope = callerScope.nestingLevel

            else:  # If we re in the main program set scope to 0 and get the framelength from the global scope (index = 0)
                callerScope = 0
                callerFramelength = self.symbol_table.scopes[0].framelength

            if y == "CV":  # If we re passing a parameter by value
                self.loadvr(x, "t0")  # y is the argument value, variable or constant
                index = paramList.pop(0)
                offset = 12 + 4 * (index - 1)
                self.output_lines.append(f"      sw t0,-{offset}(fp) \n")

            if y == "REF":
                entityScope, entity = self.symbol_table.searchEntity(x)
                if entityScope.nestingLevel == callerScope:  # If we re handling a local reference
                    if entity.type in {"parameter", "είσοδος"}:
                        index = paramList.pop(0)
                        offset = 12 + 4 * (index - 1)
                        self.output_lines.append(f"      addi t0,sp,-{entity.offset} \n")
                        self.output_lines.append(f"      sw t0,-{offset}(fp) \n")
                    elif entity.type == "έξοδος":
                        index = paramList.pop(0)
                        offset = 12 + 4 * (index - 1)
                        self.output_lines.append(f"      lw t0,-{entity.offset}(sp) \n")
                        self.output_lines.append(f"      sw t0,-{offset}(fp) \n")

                else:  # If we re handling a non-local reference
                    if entity.type in {"parameter", "είσοδος"}:
                        index = paramList.pop(0)
                        offset = 12 + 4 * (index - 1)
                        self.gnlvcode(y)
                        self.output_lines.append(f"      sw t0,-{offset}(fp) \n")
                    elif entity.type == "έξοδος":
                        index = paramList.pop(0)
                        offset = 12 + 4 * (index - 1)
                        self.gnlvcode(y)
                        self.output_lines.append(f"      sw t0,-{offset}(fp) \n")

            elif y == "RET":
                entityScope, entity = self.symbol_table.searchEntity(x)
                self.output_lines.append(f"      addi t0,sp,-{entity.offset} \n")
                self.output_lines.append(f"      sw t0,-8(fp) \n")

        elif op == "call":
            calleeName = x
            calleeScope, calleeEntity = self.symbol_table.searchEntity(calleeName)
            calleeLevel = calleeScope.nestingLevel + 1

            if blockName == program_name:
                callerLevel = 0
                callerFramelength = self.symbol_table.scopes[0].framelength

            else:
                callerScope, callerEntity = self.symbol_table.searchEntity(blockName)
                callerLevel = callerScope.nestingLevel
                callerFramelength = callerEntity.framelength
                callerOffset = callerEntity.offset

            if paramSetupDone == False:
                self.output_lines.append(f"      addi fp,sp,{callerOffset} \n")

            if calleeLevel == callerLevel:
                self.output_lines.append(f"      lw t0,-4(sp) \n")
                self.output_lines.append(f"      sw t0,-4(fp) \n")
            else:
                self.output_lines.append(f"      sw sp,-4(fp) \n")


            self.output_lines.append(f"      addi sp,sp,{calleeEntity.offset} \n")
            self.output_lines.append(f"      jal L{calleeEntity.startingQuad} \n")
            self.output_lines.append(f"      addi sp,sp,-{calleeEntity.offset} \n")
            paramSetupDone = False


    def writeAsmToFile(self, file):
        asm_file = file[:-2] + "asm"
        with open(asm_file, "w") as asm_file:
            for line in self.output_lines:
                asm_file.write(line)


# Symbol table class - handles symbol management, keeps track of the scope and of the entity storage

class SymbolTable:

    def __init__(self):
        self.globalScope = Scope(0)   # Nesting level (depth level) starts at 0 for initialization
        self.scopes = [self.globalScope]    # List that holds all the scopes starting with the global scope
        self.depth = 0
        self.ownerEntity = None



    def addEntity(self, name, type, startingQuad=None):
        currentScope = self.scopes[-1]

        # debug log for symbol table entities
        # print(f"Adding entity: {name}, Type: {type}, to Scope Level: {currentScope.nestingLevel}")

        for entity in currentScope.listEntity:
            if entity.name == name:
                if entity.type == "parameter" and type in ("είσοδος", "έξοδος"):
                    entity.type = type
                    return entity
                elif entity.type == type:
                    raise Exception(f"Entity {name} already exists in this scope")
                else:
                    raise Exception(f"Error: Entity {name} exists as {entity.type} but tried to add as {type}")

        new_entity = Entity(name, type, startingQuad)

        # Functions and procedures do not consume stack space
        if type not in ("function", "procedure"):
            new_entity.offset = currentScope.framelength
            currentScope.framelength += 4
            #print(f"    -> Offset assigned: {new_entity.offset}, new frame length: {currentScope.framelength}")
        else:
            new_entity.offset = None
            #print(f"    -> No offset assigned (function/procedure).")

        currentScope.listEntity.append(new_entity)

        return new_entity


    def addScope(self, ownerEntity=None):
        newScope = Scope(len(self.scopes))
        newScope.ownerEntity = ownerEntity  # Track which function/procedure this belongs to
        self.scopes.append(newScope)
        self.depth += 1
        return newScope


    def deleteScope(self):
        if len(self.scopes) > 1:
            scope = self.scopes.pop()
            self.depth -= 1
            # print("Deleting scope" + str(self.depth))

            # If scope belongs to function/procedure save its framelength
            if scope.ownerEntity is not None:
                scope.ownerEntity.framelength = scope.framelength

        else:
            print("Cannot delete the global scope.")


    def addArgument(self, parMode, type):
        argument = Argument(parMode, type)
        currentScope = self.scopes[-1]

        if currentScope.listEntity:
            currentScope.listEntity[-1].argumentList.append(argument)
        else:
            print("No entity to add argument to.")


    def searchEntity(self, name):

        for scope in reversed(self.scopes):
            for entity in scope.listEntity:
                if entity.name == name:
                    return scope, entity
        raise Exception(f"Entity {name} not found in scope {scope.nestingLevel}.")


    def symbolTableGen(self):
        global symbolTable

        out = ""

        for scope in self.scopes:
            out += f"Nesting Level: {scope.nestingLevel}  "

            for entity in scope.listEntity:
                line = ""

                if entity.type == "function" or entity.type == "procedure":
                    line += f"{entity.name}/{entity.startingQuad}/{entity.offset}/{entity.type} "
                    for arg in entity.argumentList:
                        line += f"-> {arg.parMode} "

                elif entity.type in ("είσοδος", "έξοδος", "parameter"):
                    line += f"{entity.name}/{entity.offset}/{entity.type}"
                    """for arg in entity.argumentList:
                        line += f"/{arg.parMode} "
                    """
                else:
                    line += f"{entity.name}/{entity.offset}/{entity.type} "

                out += line + " "

            out += "\n"

        out += "========================================\n"

        symbolTable += out


    def writeSymTable(symbol_table, filename):

        global symbolTable

        out_filename = filename[:-3] + ".sym"

        with open(out_filename, "w", encoding="utf-8") as f:
            f.write(symbolTable)



# InterCodeGen class - handles intermediate code generation using quads

class InterCodeGen:

    # Constructor
    def __init__(self, quad_list, variables):
        self.symbolTable = SymbolTable()
        self.quad_list = quad_list  # list of quads (label, op, arg1, arg2, result)
        self.variables = variables  # list to store all program variables

        self.label = 0              # label counter for quads
        self.tempVarCounter = 0     # temporary variables counter (T_0, T_1, ..., T_n)


    # Returns the next quad label
    def nextQuad(self):
        return self.label + 1

    # Generates a new quad (label, operator, operand1, operand2, operand3)
    def genQuad(self, operator, operand1, operand2, operand3):
        self.label += 1
        quad = [str(self.label), str(operator), str(operand1), str(operand2), str(operand3)]
        self.quad_list.append(quad)
        return quad

    # Generates a new temporary variable
    def newTemp(self):

        temp = "T_" + str(self.tempVarCounter)
        self.tempVarCounter += 1
        self.variables.append(temp)
        #self.symbolTable.addEntity(temp, "temporary")  # add temporary variable entity, now added in newTemp() calls
        return temp

    # Creates an empty list for quad labels
    def emptyList(self):
        return []

    # Creates a list containing one element (x)
    def makeList(self, x):
        return [str(x)]

    # Merges two lists
    def mergeList(self, list1, list2):
        return list1 + list2

    # Backpatching
    """ Takes a list of quad labels that need to be updated
        and replaces their last argument with labelZ """
    def backpatch(self, listX, labelZ):
        z = str(labelZ)
        for label in listX:
            for quad in self.quad_list:
                if quad[0] == label:  # If label matches (label from listX is found in quad_list)
                    quad[4] = z       # Replace its 5th (last element) with the given label (labelZ)
                    break


    # Test - creates a .int file that contains the intermediate code
    def interCodeGen(self, file_name):

        quads = ""  # Empty string to store quads

        interCodeGen_file = file_name[:-2] + "int"  # Change file extension
        output_file = open(interCodeGen_file, "w", encoding="utf-8", errors="replace")

        for quad in self.quad_list:
            quads += quad[0] + " :"          # Add the label
            for j in range(1, 5):
                quads += " " + str(quad[j])  # Add operator, operand1, operand2, operand3
            quads += "\n"                    # Add new line between quads

        output_file.write(quads)  # Add quad to output file
        output_file.close()


# Lexical Analyzer class - reads source code file, breaks it down in tokens

class Lex:

    # Constructor
    def __init__(self, file_name):
        self.current_line = 1
        self.file_name = file_name
        self.token = None

        try:
            self.input_file = open(file_name, "r", encoding="utf-8", errors="replace")
        except FileNotFoundError:
            print(f"Error: file {file_name} not found.")


    # Destructor
    def __del__(self):
        print(f"Stopping analysis on file: {self.file_name}")


    # Method for showing error messages
    def error(self, message):
        print(f"Error in line: {self.current_line}: {message}")
        exit(1)


    # Returns next token from the code - the string, its family and the line it was found
    def next_Token(self) -> Token:

        global eof_flag

        # Check if end of file has been reached
        if eof_flag:
            return Token("EOF", "EOF", self.current_line)

        char = self.input_file.read(1)   # Read next character

        if char == "":
            eof_flag = True
            return Token("EOF", "EOF", self.current_line)
      
        # Skip whitespace characters
        while char.isspace():
            if char == "\n":
                self.current_line += 1

            char = self.input_file.read(1)


            # Handle EOF after skipping whitespace
            if char == "":
                eof_flag = True
                return Token("EOF", "EOF", self.current_line)



        # Perform digit analysis (check for numbers)
        if char.isdigit():
            num = char
            pos_before = self.input_file.tell()  # update position after each digit
            char = self.input_file.read(1)

            while char.isdigit():
                num += char
                pos_before = self.input_file.tell()  # store position before reading further
                char = self.input_file.read(1)

            # If a letter follows a number, it's an invalid variable name (e.g., "22a")
            if char.isalpha():
                print(f"Error: Invalid identifier at line {self.current_line}. "
                      f"Identifiers cannot start with a number.")
                exit(1)

            # Check if the number exceeds 30 digits
            if len(num) > 30:
                print(f"Error: Number exceeds 30 digits at line {self.current_line}")
                exit(1)

            # Check if number falls in range [-32767, 32767]

            if (int(num) <= - 32767 or int(num) >= 32767):
                print(f"Number '{num}' is out of range at line {self.current_line}")
                exit(1)

            # Step back one character
            # (since when the loop ends, the next character is not a digit,
            # we move the pointer back)
            if char:
                self.input_file.seek(pos_before)

            return Token(num, "number", self.current_line)


        # Perform identifier analysis (check for valid variable names)
        if char.isalpha():  # must start with letter
            identifier = char
            pos_before = self.input_file.tell()  # store pointer after reading initial letter
            char = self.input_file.read(1)

            while char and (char.isalnum() or char == "_"):  # can have letters and numbers afterwards (or _ for keywords)
                identifier += char
                pos_before = self.input_file.tell()  # update pointer after reading valid character
                char = self.input_file.read(1)

            if (len(identifier) > 30):
                print(f"Error: Identifier {identifier} exceeds 30 characters at line {self.current_line}")
                exit(1)

            if char:
                self.input_file.seek(pos_before)  # rewind exactly to where the identifier ended


            # Check if identifier is a keyword
            if identifier in keywords:
                return Token(identifier, "keyword", self.current_line)

            """
            # Check if identifier contains underscores but isn't a keyword (invalid)
            if "_" in identifier:
                print(f"Error: Invalid identifier '{identifier}' at line {self.current_line}. "
                      "Identifiers cannot contain underscores unless they are keywords.")
                exit(1)
            """

            # Otherwise, treat it as a valid identifier
            return Token(identifier, "id", self.current_line)



        # Recognize arithmetic operators: + and -
        if char in {"+", "-"}:
            return Token(char, "addOperator", self.current_line)

        # Recognize arithmetic operators: * and /
        if char in {"*", "/"}:
            return Token(char, "mulOperator", self.current_line)

        # Recognize delimiters
        if char in {";", ","}:
            return Token(char, "delimiter", self.current_line)

        # Recognize group symbols
        if char in {"(", ")", "[", "]", '"'}:
            return Token(char, "groupSymbol", self.current_line)

        # Recognise pass by reference symbol
        if char == "%":
            return Token(char, "passByReference", self.current_line)

        # Recognise assignment symbol ":=" and delimiter symbol ":"
        if char == ":":
            next_char = self.input_file.read(1)
            if next_char  == "=":
                char += next_char
                return Token(char, "assignment", self.current_line)
            else:
                return Token(char, "delimiter", self.current_line)

        # Recognise relational operators  "<=", "<" and "<>"
        if char == "<":
            next_char = self.input_file.read(1)
            if next_char == "=":
                char += next_char
                return Token(char, "relOperator", self.current_line)
            elif next_char == ">":
                char += next_char
                return Token(char, "relOperator", self.current_line)
            else:  # Just "<"
                self.input_file.seek(self.input_file.tell() - 1)
                return Token(char, "relOperator", self.current_line)

        # Recognise relational operators  ">=" and ">"
        if char == ">":
            next_char = self.input_file.read(1)
            if next_char == "=":
                char += next_char
                return Token(char, "relOperator", self.current_line)
            else:
                self.input_file.seek(self.input_file.tell() - 1)
                return Token(char, "relOperator", self.current_line)

        # Recognise relational operator "="
        if char == "=":
            return Token(char, "relOperator", self.current_line)

        # Check for comments in the form of { comment }
        if char == "{":
            # Read the next characters until we find the closing '}'
            next_char = self.input_file.read(1)

            while next_char != "}":
                if next_char == "":
                    # Handle EOF inside comment
                    eof_flag = True
                    print(f"Error: Unexpected end of file inside comment at line {self.current_line}")
                    exit(1)
                if next_char == "\n":
                    # Increment line number for multi line comments
                    self.current_line += 1
                next_char = self.input_file.read(1)

            # Now the comment is fully skipped, continue to the next token.
            char = self.input_file.read(1)

            # Skip whitespace characters after the comment
            while char.isspace():
                if char == "\n":
                    self.current_line += 1
                char = self.input_file.read(1)

            # If we reached EOF, return EOF token
            if char == "":
                eof_flag = True
                return Token("EOF", "EOF", self.current_line)


            # Move back one character to correctly process the next token
            self.input_file.seek(self.input_file.tell() - len(char.encode("utf-8")))
            return self.next_Token()


        # If none of the above, it's an unrecognized character
        print(f"Error: Unrecognized character '{char}' at line {self.current_line}")
        exit(1)



# Syntax Analyzer class - parses tokens from the Lexical analyzer to check syntax

class Parser:

    # Constructor
    def __init__(self, lexical_analyzer, intermediate_gen, symbol_table, final_code_gen):
        self.lexical_analyzer = lexical_analyzer
        self.intermediate_gen = intermediate_gen
        self.symbol_table = symbol_table
        self.final_code_gen = final_code_gen
        self.token = None
        self.inFunction = False  # Track if we re inside a function for the return statement
                                 # (if inside f : treat f := {something} as return {something})

        self.program_name = ""      # For intermediate code generation
        self.subprogram_name = ""     # For intermediate code generation


    # Start syntax analysis by getting the first token & calling the parsing functions
    def syntax_analyzer(self):
        self.token = self.get_token()
        self.program()
        print("Compilation successfully completed")


    # Gets the next token from the lexical analyzer
    def get_token(self):
        self.token = self.lexical_analyzer.next_Token()
        return self.token

    # Display error message and exit program
    def error(self, message):
        print(f"Syntax Error at line {self.token.line_number}: {message}")
        exit(1)


    def program(self):

        global token
        global program_name

        # Check if the first token is "πρόγραμμα"
        if self.token.recognised_string != "πρόγραμμα":
            self.error("'πρόγραμμα' is expected in the start of the program.")

        token = self.get_token()  # move on to the next token

        # Check for valid program ID
        if token.family != "id":
            self.error("Program name (id) expected after 'πρόγραμμα'.")

        self.program_name = token.recognised_string  # Store program name

        program_name = self.program_name  # Used in the final code generator

        token = self.get_token()  # move on to the next token

        # Calls program_block() to continue with the analysis
        self.program_block(program_name)

    def program_block(self, name):

        global token
        global program_name

        # Calls declarations() & subprograms()
        self.declarations()

        self.final_code_gen.output_lines.append(f"L0:   b L{program_name} \n")

        self.subprograms()

        start_quad = self.intermediate_gen.genQuad("begin_block", name, "_", "_")  # Begin block to mark beginning of program

        # Check for 'αρχή_προγράμματος"
        if token.recognised_string != "αρχή_προγράμματος":
            self.error("Expected 'αρχή_προγράμματος' before program statements.")

        token = self.get_token()

        self.sequence()

        # Check for 'τέλος_προγράμματος"
        if token.recognised_string != "τέλος_προγράμματος":
            self.error("Expected 'τέλος_προγράμματος' at the end of the program.")

        self.final_code_gen.output_lines.append(f"L{program_name}: \n")

        self.intermediate_gen.genQuad("halt", "_", "_", "_")  # Halt to stop execution after program statements
        self.intermediate_gen.genQuad("end_block", name, "_", "_")  # End block to mark end of program

        self.final_code_gen.assemblyBlock(self.program_name, start_quad)

        self.symbol_table.symbolTableGen()  # Test symbol table, creates .sym file



    def declarations(self):

        global token

        # 'δήλωση' not expected ( | ε )
        while token.recognised_string == "δήλωση":  # While 'δήλωση' appears
            token = self.get_token()
            self.varlist()  # Now, varlist() is responsible for checking IDs


    def varlist(self, mode=None):
        global token

        # Normal parameter or formal parameter handling
        if token.family == "id":
            # Add the entity at depth level 1 (inside function scope)
            if mode == "CV":  # If mode is CV (by value), treat it as είσοδος
                self.symbol_table.addEntity(f"{token.recognised_string}", "είσοδος")  # Add as είσοδος
                self.symbol_table.addArgument("CV", 0)  # Mark as CV (by value)


                if len(self.symbol_table.scopes) > 1:
                    parentScope = self.symbol_table.scopes[-2]  # Function scope
                    currentFunction = parentScope.listEntity[-1]  # Get most recent function
                    if hasattr(currentFunction, 'argumentList'):
                        currentFunction.argumentList.append(Argument("CV", token.recognised_string))
                    else:
                        print(f"Error: {currentFunction.name} is not a valid function.")
                else:
                    print("Error: No function scope found.")

            elif mode == "REF":  # If mode is REF (by reference), treat it as έξοδος
                self.symbol_table.addEntity(f"{token.recognised_string}", "έξοδος")  # Add as έξοδος
                self.symbol_table.addArgument("REF", 0)  # Mark as REF (by reference)

                if len(self.symbol_table.scopes) > 1:
                    parentScope = self.symbol_table.scopes[-2]  # Function scope
                    currentFunction = parentScope.listEntity[-1]  # Get most recent function
                    if hasattr(currentFunction, 'argumentList'):
                        currentFunction.argumentList.append(Argument("REF", token.recognised_string))
                    else:
                        print(f"Error: {currentFunction.name} is not a valid function.")
                else:
                    print("Error: No function scope found.")

            else:  # If no mode (regular parameter)
                self.symbol_table.addEntity(token.recognised_string, "parameter")  # Add as regular parameter

            token = self.get_token()

            # Handle commas between parameters
            while token.recognised_string == ",":  # Handle commas
                token = self.get_token()

                if token.family == "id":
                    if mode == "CV":  # If mode is CV, treat it as είσοδος
                        self.symbol_table.addEntity(f"{token.recognised_string}", "είσοδος")  # Add as είσοδος
                        self.symbol_table.addArgument("CV", 0)  # Mark as CV (by value)

                        if len(self.symbol_table.scopes) > 1:
                            parentScope = self.symbol_table.scopes[-2]  # Function scope
                            currentFunction = parentScope.listEntity[-1]  # Get most recent function
                            if hasattr(currentFunction, 'argumentList'):
                                currentFunction.argumentList.append(Argument("CV", token.recognised_string))
                            else:
                                print(f"Error: {currentFunction.name} is not a valid function.")
                        else:
                            print("Error: No function scope found.")

                    elif mode == "REF":  # If mode is REF, treat it as έξοδος
                        self.symbol_table.addEntity(f"{token.recognised_string}", "έξοδος")  # Add as έξοδος
                        self.symbol_table.addArgument("REF", 0)  # Mark as REF (by reference)

                        if len(self.symbol_table.scopes) > 1:
                            parentScope = self.symbol_table.scopes[-2]  # Function scope
                            currentFunction = parentScope.listEntity[-1]  # Get most recent function
                            if hasattr(currentFunction, 'argumentList'):
                                currentFunction.argumentList.append(Argument("REF", token.recognised_string))
                            else:
                                print(f"Error: {currentFunction.name} is not a valid function.")
                        else:
                            print("Error: No function scope found.")

                    else:  # If no mode (regular parameter)
                        self.symbol_table.addEntity(token.recognised_string, "parameter")  # Add as regular parameter


                    token = self.get_token()
                else:
                    self.error("Expected an identifier after ',' in variable list.")  # Handle error
        else:
            self.error(
                "Expected an identifier at the beginning of variable list.")  # Handle error for missing identifier


    def subprograms(self):

        global token

        while (token.recognised_string == "συνάρτηση" or token.recognised_string == "διαδικασία"):
            if (token.recognised_string == "συνάρτηση"):
                self.func()
            else:
                self.proc()


    def func(self):

        global token
        global function_names

        index = len(function_names)

        if (token.recognised_string == "συνάρτηση"):
            token = self.get_token()
        else:
            print("Expected 'συνάρτηση' at function declaration")

        # Get function name (id)
        if (token.family == "id"):
            self.subprogram_name = token.recognised_string  # Store function name
            function_names.append(token.recognised_string)

            func_entity = self.symbol_table.addEntity(token.recognised_string, "function",
                                        self.intermediate_gen.nextQuad() + 1)  # add function entity
            self.symbol_table.addScope(ownerEntity=func_entity)

            token = self.get_token()
        else:
            self.error("Expected function identifier after 'συνάρτηση'.")

        # Expect '('
        if (token.recognised_string == "("):
            token = self.get_token()
        else:
            self.error("Expected '(' after function identifier.")


        self.formalparlist()

        # Expect ')'
        if (token.recognised_string == ")"):
            token = self.get_token()
        else:
            self.error("Expected ')' after function parameter list.")


        self.subprograms()  # Placed here to emit nested functions first

        start_quad = self.intermediate_gen.nextQuad()  # Save the starting quad for the assemblyBlock call later on


        self.funcblock()


    def proc(self):

        global token
        global procedure_names

        index = len(procedure_names)

        if (token.recognised_string == "διαδικασία"):
            token = self.get_token()
        else:
            print("Expected 'διαδικασία' at procedure declaration")

        # Get procedure name (id)
        if (token.family == "id"):
            self.subprogram_name = token.recognised_string  # Store procedure name
            procedure_names.append(token.recognised_string)

            proc_entity = self.symbol_table.addEntity(token.recognised_string, "procedure",
                                                      self.intermediate_gen.nextQuad() + 1)  # add procedure entity
            self.symbol_table.addScope(ownerEntity=proc_entity)

            token = self.get_token()
        else:
            self.error("Expected procedure identifier after 'διαδικασία'.")

        # Expect '('
        if (token.recognised_string == "("):
            token = self.get_token()
        else:
            self.error("Expected '(' after procedure identifier.")

        self.formalparlist()

        # Expect ')'
        if (token.recognised_string == ")"):
            token = self.get_token()
        else:
            self.error("Expected ')' after procedure parameter list.")

        self.procblock()


    def formalparlist(self):

        global token

        while (token.family == "id"):
            self.varlist()

        # Check if we read ')' which means that no parameters are left
        if token.recognised_string == ")":
            return  # Returning without moving past ) since func() and proc() handle that themselves
        else:
            self.error("Expected ')' after formal parameter list.")


    def funcblock(self, skip_subprograms=False):
        global token
        global function_names
        index = len(function_names) - 1

        if (token.recognised_string == "διαπροσωπεία"):
            token = self.get_token()
        else:
            self.error("Expected 'διαπροσωπεία' at the beginning of function block")

        self.funcinput()
        self.funcoutput()

        if not skip_subprograms:
            self.declarations()
            self.subprograms()
        else:
            self.declarations()

        if (token.recognised_string == "αρχή_συνάρτησης"):
            current_scope = self.symbol_table.scopes[-1]
            entity_name = current_scope.ownerEntity.name
            start_quad = self.intermediate_gen.genQuad("begin_block", entity_name, "_",
                                                       "_")  # Begin block to mark beginning of procedure
            self.inFunction = True
            #start_quad = self.intermediate_gen.genQuad("begin_block", function_names[index], "_", "_")  # Begin block to mark beginning of procedure
            token = self.get_token()
        else:
            self.error("Expected 'αρχή_συνάρτησης' after function body")

        self.sequence()

        if (token.recognised_string == "τέλος_συνάρτησης"):
            self.inFunction = False
            token = self.get_token()
        else:
            self.error("Expected 'τέλος_συνάρτησης' at the end of the function block")

        index = len(function_names) - 1

        #  Get current scope and scope owner (function)
        current_scope = self.symbol_table.scopes[-1]
        func_entity = current_scope.ownerEntity
        func_entity.startingQuad = int(start_quad[0])

        # Assign framelength of the function before we delete the scope
        func_entity.offset = current_scope.framelength

        #self.intermediate_gen.genQuad("end_block", function_names[index], "_", "_")
        self.intermediate_gen.genQuad("end_block", entity_name, "_", "_")
        self.symbol_table.symbolTableGen()

        self.final_code_gen.assemblyBlock(function_names[index], start_quad)
        # self.final_code_gen.assemblyBlock(entity_name, start_quad)
        self.symbol_table.deleteScope()


    def procblock(self):

        global token
        global procedure_names
        index = len(procedure_names) - 1

        if (token.recognised_string == "διαπροσωπεία"):
            token = self.get_token()
        else:
            self.error("Expected 'διαπροσωπεία' at the beginning of function block")

        self.funcinput()
        self.funcoutput()

        self.declarations()

        self.subprograms()

        if (token.recognised_string == "αρχή_διαδικασίας"):
            current_scope = self.symbol_table.scopes[-1]
            entity_name = current_scope.ownerEntity.name
            start_quad = self.intermediate_gen.genQuad("begin_block", entity_name, "_",
                                                       "_")  # Begin block to mark beginning of procedure
            #start_quad = self.intermediate_gen.genQuad("begin_block", procedure_names[index], "_", "_")  # Begin block to mark beginning of procedure
            token = self.get_token()
        else:
            self.error("Expected 'αρχή_διαδικασίας' after function body")

        self.sequence()

        if (token.recognised_string == "τέλος_διαδικασίας"):
            token = self.get_token()
        else:
            self.error("Expected 'τέλος_διαδικασίας' at the end of the function block")

        index = len(procedure_names) - 1

        # Get current scope and scope owner (procedure)
        current_scope = self.symbol_table.scopes[-1]
        proc_entity = current_scope.ownerEntity
        proc_entity.startingQuad = int(start_quad[0])

        # Assign framelength of the procedure before we delete the scope
        proc_entity.offset = current_scope.framelength


        #self.intermediate_gen.genQuad("end_block", procedure_names[index], "_", "_")
        self.intermediate_gen.genQuad("end_block", entity_name, "_", "_")

        self.symbol_table.symbolTableGen()

        self.final_code_gen.assemblyBlock(procedure_names[index], start_quad)
        #self.final_code_gen.assemblyBlock(entity_name, start_quad)
        self.symbol_table.deleteScope()


    def funcinput(self):

        global token

        # If we find "είσοδος" then call varlist, else: do nothing (no error() call happens)
        if (token.recognised_string == "είσοδος"):
            token = self.get_token()
            self.varlist(mode = "CV")


    def funcoutput(self):

        global token

        # If we find "εξοδος" then call varlist, else: do nothing (no error() call happens)
        if (token.recognised_string == "έξοδος"):
            token = self.get_token()
            self.varlist(mode = "REF")


    def sequence(self):

        global token

        # Expect at least one statement
        self.statement()

        # Allow multiple statements only after ";"
        while (token.recognised_string == ";"):
            token = self.get_token()  # Move past ";"
            self.statement()  # Process next statement


    def statement(self):

        global token

        # Check if we have an assignment (ID followed by ":=")
        if (token.family == "id"):  # Read "ID"
            id = self.token.recognised_string  # Store the identifier for the assignment quad
            token = self.get_token()  # Move to the next token

            if (token.recognised_string == ":="):  # If ":=" is read, then its an assignment
                self.assignment_stat(id)
            else:
                self.error("Expected ':=' after assignment identifier")

        elif token.recognised_string == "εάν":
            self.if_stat()

        elif token.recognised_string == "όσο":
            self.while_stat()

        elif token.recognised_string == "επανάλαβε":
            self.do_stat()

        elif token.recognised_string == "για":
            self.for_stat()

        elif token.recognised_string == "διάβασε":
            self.input_stat()

        elif token.recognised_string == "γράψε":
            self.print_stat()

        elif token.recognised_string == "εκτέλεσε":
            self.call_stat()


    def assignment_stat(self, id):

        global token
        global function_names

        e_place = ""

        if (token.recognised_string == ":="):
            token = self.get_token()    # Move to the next token
            e_place = self.expression()    # Handle the expression and store the expression

            if id == self.subprogram_name and self.inFunction:
                # We re in a function and assigning to its name :: treat as return statement
                self.intermediate_gen.genQuad("retv", e_place, "_", "_")

            # Check if the expression is a function (handle case where we have z := function(x, y))
            elif e_place in function_names:
                w = self.intermediate_gen.newTemp()
                self.symbol_table.addEntity(w, "temporary", None)
                self.intermediate_gen.genQuad("par", w, "RET", "_")
                self.intermediate_gen.genQuad("call", e_place, "_", "_")
                self.intermediate_gen.genQuad(":=", w, "_", id)
            else:
                # If not a function, do regular assignment
                self.intermediate_gen.genQuad(":=", e_place, "_", id)  # Generate assignment quad
        else:
            self.error("Expected ':=' after assignment identifier")


    def if_stat(self):

        global token

        true_list = self.intermediate_gen.emptyList()  # List of quads with condition thats true
        false_list = self.intermediate_gen.emptyList()  # List of quads with condition thats false

        if_list = self.intermediate_gen.emptyList()  # List for handling the end of the if-statement

        # Expects "εάν"
        if (token.recognised_string == "εάν"):
            token = self.get_token()

            true_list, false_list = self.condition()  # Handle the condition part, save results on true / false lists

            # Backpatch true condition to the next quad after the "τότε" block
            self.intermediate_gen.backpatch(true_list, self.intermediate_gen.nextQuad())


            # Expects "τότε" after condition
            if (token.recognised_string == "τότε"):
                token = self.get_token()

                # Handle the sequence of statements on the "τότε" (then) part
                self.sequence()

                # Mark the point to jump after the then block
                if_list = self.intermediate_gen.makeList(self.intermediate_gen.nextQuad())
                self.intermediate_gen.genQuad("jump", "_", "_", "_")

                # Backpatch false condition to the next point after then
                self.intermediate_gen.backpatch(false_list, self.intermediate_gen.nextQuad())

                # Call the optional else_part() function
                self.elsepart()

                # Backpatch the if list (where the then block ends) to jump after the else part
                self.intermediate_gen.backpatch(if_list, self.intermediate_gen.nextQuad())

            else:
                self.error("Expected 'τότε' after the condition in the if statement.")

            # Check for the "εάν_τέλος" part to end the if statement
            if (token.recognised_string == "εάν_τέλος"):
                token = self.get_token()

            else:
                self.error("Expected 'εάν_τέλος' at the end of the if statement")


    def elsepart(self):

        global token

        if (token.recognised_string == "αλλιώς"):

            token = self.get_token()

            # Handle the sequence of statements on the "αλλιώς" (else) part
            self.sequence()


    def while_stat(self):

        global token

        if (token.recognised_string == "όσο"):
            token = self.get_token()

            b_true = self.intermediate_gen.emptyList()
            b_false = self.intermediate_gen.emptyList()

            # Save the condition
            b_quad = self.intermediate_gen.nextQuad()

            # Get true and false lists from the condition
            b_true, b_false = self.condition()

            # Connect true list to the loop body
            self.intermediate_gen.backpatch(b_true, self.intermediate_gen.nextQuad())

            if (token.recognised_string == "επανάλαβε"):
                token = self.get_token()

            else:
                self.error("Expected 'επανάλαβε' after condition in while loop.")

            self.sequence()

            # Jump to the condition
            self.intermediate_gen.genQuad("jump", "_", "_", b_quad)

            # Connect false list to the code after the loop
            self.intermediate_gen.backpatch(b_false, self.intermediate_gen.nextQuad())

            if (token.recognised_string == "όσο_τέλος"):
                token = self.get_token()
            else:
                self.error("Expected 'όσο_τέλος' to close the loop.")


    def do_stat(self):

        global token

        true_list = self.intermediate_gen.emptyList()
        false_list = self.intermediate_gen.emptyList()

        if (token.recognised_string == "επανάλαβε"):
            token = self.get_token()

            s_quad = self.intermediate_gen.nextQuad()  # Save the start of the loop

            self.sequence()

            if (token.recognised_string == "μέχρι"):
                token = self.get_token()

            else:
                self.error("Expected 'μέχρι' after the loop body.")

            true_list, false_list = self.condition()  # Evaluate condition and store its results in true, false lists

            # If the condition is false, repeat the loop
            self.intermediate_gen.backpatch(false_list, s_quad)

            # If the condition is true, exit the loop
            self.intermediate_gen.backpatch(true_list, self.intermediate_gen.nextQuad())

        else:
            self.error("Expected 'επανάλαβε' at the beginning of the do-while loop.")


    def for_stat(self):

        global token

        if (token.recognised_string == "για"):
            token = self.get_token()
        else:
            self.error("Expected 'για' at beginning of for loop.")

        if (token.family == "id"):
            loop_var = self.token.recognised_string
            token = self.get_token()
        else:
            self.error("Expected ID after 'για'.")

        if (token.recognised_string == ":="):
            token = self.get_token()
        else:
            self.error("Expected ':=' after 'ID.")

        start_value = self.expression()
        self.intermediate_gen.genQuad(":=", start_value, "_", loop_var)

        if (token.recognised_string == "έως"):
            token = self.get_token()
        else:
            self.error("Expected 'έως' after ':='.")

        final_val = self.expression()


        step_val = "1"
        if token.recognised_string == "με_βήμα":
            token = self.get_token()
            step_val = self.expression()
            

        loop_check = self.intermediate_gen.nextQuad()
        self.intermediate_gen.genQuad("<=", loop_var, final_val, "_")
        

        false_jump = self.intermediate_gen.makeList(self.intermediate_gen.nextQuad())
        self.intermediate_gen.genQuad("jump", "_", "_", "_")

        if (token.recognised_string == "επανάλαβε"):
            token = self.get_token()
        else:
            self.error("Expected 'επανάλαβε' after expressions in for loop.")

        self.sequence()
        

        temp = self.intermediate_gen.newTemp()
        self.symbol_table.addEntity(temp, "temporary", None)
        self.intermediate_gen.genQuad("+", loop_var, step_val, temp)
        self.intermediate_gen.genQuad(":=", temp, "_", loop_var)


        self.intermediate_gen.genQuad("jump", "_", "_", loop_check)


        self.intermediate_gen.backpatch(false_jump, self.intermediate_gen.nextQuad())
        
        if (token.recognised_string == "για_τέλος"):
            token = self.get_token()
        else:
            self.error("Expected 'για_τέλος' to close the for loop.")


    def step(self):

        global token

        if (token.recognised_string == "με_βήμα"):
            token = self.get_token()

            self.expression()


    def print_stat(self):

        global token

        e_place = ""

        if (token.recognised_string == "γράψε"):
            token = self.get_token()
        else:
            self.error("Expected 'γράψε' at the beginning of print statement.")

        e_place = self.expression()
        self.intermediate_gen.genQuad("out", e_place, "_", "_")


    def input_stat(self):

        global token

        id_place = ""

        if (token.recognised_string == "διάβασε"):
            token = self.get_token()  # Move to the next token
        else:
            self.error("Expected 'γράψε' at the beginning of input statement.")

        if (token.family == "id"):  # Read "ID"
            id_place = token.recognised_string
            self.intermediate_gen.genQuad("in", id_place, "_", "_")
            token = self.get_token()  # Move to the next token
        else:
            self.error("Expected an identifier after 'διάβασε'.")


    def call_stat(self):

        global token
        global call_name

        if (token.recognised_string == "εκτέλεσε"):
            token = self.get_token()  # Move to the next token
        else:
            self.error("Expected 'εκτέλεσε' at the beginning of call statement.")

        if (token.family == "id"):  # Read "ID"
            call_name = token.recognised_string  # Store function / procedure name
            token = self.get_token()  # Move to the next token
        else:
            self.error("Expected an identifier after 'εκτέλεσε'.")

        self.idtail(call_name)


    def idtail(self, id_name):

        global token
        global call_name
        global function_names
        global procedure_names

        if (token.recognised_string == "("):
            self.actualpars()   # Handle actual parameters

            # Check if we re dealing with a function, or procedure
            if (id_name in function_names):  # If its a function
                w = self.intermediate_gen.newTemp()
                self.symbol_table.addEntity(w, "temporary", None)
                self.intermediate_gen.genQuad("par", w, "RET", "_")
                self.intermediate_gen.genQuad("call", id_name, "_", "_")
                return w
            elif (id_name in procedure_names):
                self.intermediate_gen.genQuad("call", id_name, "_", "_")
                return None

        # Otherwise, do nothing (handles empty case)
        return None


    def actualpars(self):

        global token

        # Expect '(' to start the actual parameters
        if (token.recognised_string == "("):
            token = self.get_token()
        else:
            self.error("Expected '(' at the beginning of actual parameters ")

        # Parse the parameter list
        self.actualparlist()

        # Expect ')' to close the actual parameters
        if (token.recognised_string == ")"):
            token = self.get_token()
        else:
            self.error("Expected ')' at the end of actual parameters ")


    def actualparlist(self):

        global token

        # Check if we have actual parameters, else return nothing
        if (token.recognised_string != ")"):

            self.actualparitem()  # Handle the first parameter

            while token.recognised_string == ",":
                token = self.get_token()  # Move past ','
                self.actualparitem()  # Handle the next parameter


    def actualparitem(self):

        global token

        if (token.recognised_string == "%"):   # Pass by reference (% before variable)

            token = self.get_token()   # Move past '%'

            if (token.family == "id"):
                varname = token.recognised_string
                self.intermediate_gen.genQuad("par", varname, "REF", "_")

                token = self.get_token()
            else:
                self.error("Expected ID after '%' in actual parameter.")

        else:   # Pass by value (variable)
            expression = self.expression()
            self.intermediate_gen.genQuad("par", expression, "CV", "_")


    def condition(self):

        global token

        # Initialize true & false lists for boolean term (b)
        b_true = self.intermediate_gen.emptyList()
        b_false = self.intermediate_gen.emptyList()

        # Initialize temporary lists for individual bool terms (q1, q2, ..., qn)
        q1_true = self.intermediate_gen.emptyList()
        q1_false = self.intermediate_gen.emptyList()
        q2_true = self.intermediate_gen.emptyList()
        q2_false = self.intermediate_gen.emptyList()

        # Handle first boolean term - store first bool term results in q1
        q1_true, q1_false = self.boolterm()

        # Quad transfer from q1 list to b list
        b_true = q1_true
        b_false = q1_false

        # Repeat for multiple OR (ή) operators
        while (token.recognised_string == "ή"):
            # Backpatch previous false list to point to the next instruction
            self.intermediate_gen.backpatch(b_false, self.intermediate_gen.nextQuad())
            token = self.get_token()   # Move past 'ή'

            # Handle the next boolean term - store new bool term results in q2
            q2_true, q2_false = self.boolterm()

            b_true = self.intermediate_gen.mergeList(b_true, q2_true)  # Merge true lists
            b_false = q2_false  # False list takes the value of q2 false list

        return b_true, b_false  # Return true, false lists


    def boolterm(self):

        global token

        # Initialize true & false lists for boolean term (q)
        q_true = self.intermediate_gen.emptyList()
        q_false = self.intermediate_gen.emptyList()

        # Initialize temporary lists for individual bool terms (r1, r2, ..., rn)
        r1_true = self.intermediate_gen.emptyList()
        r1_false = self.intermediate_gen.emptyList()
        r2_true = self.intermediate_gen.emptyList()
        r2_false = self.intermediate_gen.emptyList()

        # Handle first boolean term - store first bool term results in r1
        r1_true, r1_false = self.boolfactor()

        # Quad transfer from q1 list to b list
        q_true = r1_true
        q_false = r1_false

        # Repeat for multiple AND (και) operators
        while (token.recognised_string == "και"):
            # Backpatch previous true list to point to the next instruction
            self.intermediate_gen.backpatch(q_true, self.intermediate_gen.nextQuad())
            token = self.get_token()  # Move past 'και'

            # Handle the next boolean term - store new bool term results in r2
            r2_true, r2_false = self.boolfactor()

            q_false = self.intermediate_gen.mergeList(q_false, r2_false)  # Merge false lists
            q_true = r2_true  # True list takes the value of r2 true list

        return q_true, q_false  # Return true, false lists


    def boolfactor(self):

        global token

        r_true = self.intermediate_gen.emptyList()
        r_false = self.intermediate_gen.emptyList()

        b_true = self.intermediate_gen.emptyList()
        b_false = self.intermediate_gen.emptyList()

        e1_place = ""
        e2_place = ""
        relop = ""

        # Handle NOT [condition]
        if (token.recognised_string == "όχι"):
            token = self.get_token()

            if (token.recognised_string == "["):
                token = self.get_token()
            else:
                self.error("Expected '[' after όχι")

            b_true, b_false = self.condition()  # Call condition() and get b_true, b_false from it

            if (token.recognised_string == "]"):
                token = self.get_token()
            else:
                self.error("Expected ']' after condition")

            # Swap and transfer quads from b list to r list
            r_true = b_false
            r_false = b_true

        # Handle [condition]
        elif (token.recognised_string == "["):
            token = self.get_token()

            b_true, b_false = self.condition()  # Call condition() and get b_true, b_false from it

            if (token.recognised_string == "]"):
                token = self.get_token()
            else:
                self.error("Expected ']' after condition")

            # Transfer quads from b list to r list
            r_true = b_true
            r_false = b_false

        # Handle relational expression (e1_place relop e2_place)
        else:
            e1_place = self.expression()  # Get 1st expression
            relop = self.relational_oper()  # Get relational operation
            e2_place = self.expression()  # Get 2nd expression

            # Create first quad for the relational operator
            nq = self.intermediate_gen.nextQuad()
            r_true = self.intermediate_gen.makeList(nq)  # Create list for true conditions
            self.intermediate_gen.genQuad(relop, e1_place, e2_place, "_")  # Create relational operator quad

            # Create second squad for the jump
            nq = self.intermediate_gen.nextQuad()
            r_false = self.intermediate_gen.makeList(nq)  # Create list for false conditions
            self.intermediate_gen.genQuad("jump", "_", "_", "_")  # Create quad jump

        return r_true, r_false

    def expression(self):

        global token

        sign = self.optional_sign()

        t1_place = ""
        t2_place = ""
        e_place = ""

        self.optional_sign()

        t1_place = self.term()  # Calls term and stores the first term

        if sign == "-":
            w = self.intermediate_gen.newTemp()
            self.symbol_table.addEntity(w, "temporary", None)
            self.intermediate_gen.genQuad("-", "0", t1_place, w)
            t1_place = w

        # Handle addition & subtraction (+, -)
        while (token.recognised_string == "+" or token.recognised_string == "-"):

            op = token.recognised_string  # Stores operator + or -

            # Dont move on to the next token, add_oper() will handle that
            self.add_oper()
            t2_place = self.term()  # Calls term and stores the second term

            w = self.intermediate_gen.newTemp()  # Creates new temporary variable for current result
            self.symbol_table.addEntity(w, "temporary", None)
            self.intermediate_gen.genQuad(op, t1_place, t2_place, w)  # Creates quad that adds current result to the new t2
            t1_place = w  # Current result is stored in t1 for it to be used in case we have another t2

        e_place = t1_place  # If there isnt another t2 then the result will be t1
        return e_place



    def term(self):

        global token

        f1_place = ""
        f2_place = ""
        t_place = ""

        f1_place = self.factor()  # Calls factor and stores the first term

        # Handle multiplication and division (*, /)
        while (token.recognised_string == "*" or token.recognised_string == "/"):

            op = token.recognised_string  # Stores operator * or /

            # Dont move on to the next token, mul_oper() will handle that
            self.mul_oper()
            f2_place = self.factor()  # Calls factor and stores the second term

            w = self.intermediate_gen.newTemp()  # Creates new temporary variable for current result
            self.symbol_table.addEntity(w, "temporary", None)
            self.intermediate_gen.genQuad(op, f1_place, f2_place, w)  # Creates quad that adds current result to the new f2
            f1_place = w  # Current result is stored in f1 for it to be used in case we have another f2

        t_place = f1_place  # If there isnt another f2 then the result will be f1
        return t_place


    def factor(self):

        global token

        e_place = ""  # To store expression
        f_place = ""  # To store factor value
        id_place = ""  # To store id value

        if (token.family == "number"):
            f_place = token.recognised_string  # Store number
            token = self.get_token()

        elif (token.recognised_string == "("):
            token = self.get_token()

            e_place = self.expression()  # Call expresion() and store the expression

            if (token.recognised_string == ")"):
                token = self.get_token()
            else:
                self.error("Expected ')' after expression")

            f_place = e_place  # Transfer e_place to f_place

        elif (token.family == "id"):
            id_place = token.recognised_string  # Store id
            token = self.get_token()

            result = self.idtail(id_place)

            if result is not None:
                f_place = result  # function call returning temporary variable
            else:
                f_place = id_place

            #f_place = id_place  # Transfer id_place to f_place

        else:
            self.error("Expected factor: INTEGER, '(' expression ')', or ID.")

        return f_place  # Return the final factor value (number, expression, or id)


    def relational_oper(self):

        global token
        relop = ""

        if token.recognised_string == "=":
            relop = token.recognised_string
            token = self.get_token()  # Move past '='
        elif token.recognised_string == "<=":
            relop = token.recognised_string
            token = self.get_token()  # Move past '<='
        elif token.recognised_string == ">=":
            relop = token.recognised_string
            token = self.get_token()  # Move past '>='
        elif token.recognised_string == "<>":
            relop = token.recognised_string
            token = self.get_token()  # Move past '<>'
        elif token.recognised_string == "<":
            relop = token.recognised_string
            token = self.get_token()  # Move past '<'
        elif token.recognised_string == ">":
            relop = token.recognised_string
            token = self.get_token()  # Move past '>'
        else:
            self.error("Expected a relational operator.")
        return relop  # For intermediate code generation (boolfactor)

    def add_oper(self):

        global token

        if token.recognised_string == "+" or token.recognised_string == "-":
            token = self.get_token()  # Move past the '+' or '-' operator
        else:
            self.error("Expected '+' or '-' operator.")


    def mul_oper(self):

        global token

        if token.recognised_string == "*" or token.recognised_string == "/":
            token = self.get_token()  # Move past the '*' or '/' operator
        else:
            self.error("Expected '*' or '/' operator.")


    def optional_sign(self):

        global token

        if token.recognised_string == "+":
            self.add_oper()
            return None
        elif token.recognised_string == "-":
            self.add_oper()
            return "-"
        return None


# Main function

def main():

    intermediateGen = InterCodeGen([], [])  # Lists will be populated during compilation

    symbolTable = SymbolTable()             # Initialize the Symbol Table
    finalCodeGen = FinalCodeGen(intermediateGen.quad_list,
                                symbolTable)  # Give quad_list and symbolTable args to finalCodeGen
    lexer = Lex(sys.argv[1])                 # Initialize the Lexical Analyzer
    parser = Parser(lexer, intermediateGen, symbolTable, finalCodeGen)  # Initialize the Syntax Analyzer


    # Start the syntax analysis
    parser.syntax_analyzer()

    intermediateGen.interCodeGen(sys.argv[1])  # Test intermediate code, creates .int file

    symbolTable.writeSymTable(sys.argv[1])  # Test symbol table, creates .sym file

    finalCodeGen.writeAsmToFile(sys.argv[1]) # Test final code, creates .asm file

    """
    while token.family != "EOF":
        print(token)
        token = lexer.next_Token()  # Get the next token
    """

# Define some global variables
if (__name__ == "__main__"):

    if len(sys.argv) < 2:
        print("Usage: python GreekPPCompiler.py <filename.gr>")
        sys.exit(1)

    if not sys.argv[1].lower().endswith(".gr"):
        print("Error: Invalid file extension. Input file should end with '.gr'")
        sys.exit(1)

    # Keywords of the Greek++ language
    keywords = {"πρόγραμμα", "δήλωση",
                "εάν", "τότε", "αλλιώς", "εάν_τέλος",
                "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος",
                "για", "έως", "με_βήμα", "για_τέλος",
                "διάβασε", "γράψε",
                "συνάρτηση", "διαδικασία", "διαπροσωπεία",
                "είσοδος", "έξοδος",
                "αρχή_συνάρτησης", "τέλος_συνάρτησης",
                "αρχή_διαδικασίας", "τέλος_διαδικασίαs",
                "αρχή_προγράμματος", "τέλος_προγράμματος",
                "ή", "και", "εκτέλεσε"}

    token = 0
    eof_flag = False
    input_file = open(sys.argv[1], "r", encoding="utf-8", errors="replace")
    call_name = ""  # Used in call_stat() to store function - procedure name for intermediate code generation
    function_names = []  # Store function names for intermediate code generation
    procedure_names = []  # Store procedure names for intermediate code generation
    program_name = ""  # Declared as global because we cant create an instance of the parser
                    # (that contains program_name) on the final code generator

    symbolTable = ""
    paramSetupDone = False  # Flag for allocating the memory for the function parameters (initializes fp) - used in final code gen
    paramList = []

    # Main call
    main()
