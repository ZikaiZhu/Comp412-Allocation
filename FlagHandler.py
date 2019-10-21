from Scanner import Scanner
from DoublyLinkedList import DoublyLinkedList
from Parser import Parser
import sys
pattern_dict = {-2: "SPACE", -1 : "ERROR", 0 : "MEMOP", 1 : "LOADI", 2 : "ARITHOP", 3 : "OUTPUT", 4 : "NOP", 5 : "CONSTANT", 6 : "REGISTER", 7 : "COMMA", 8 : "INTO", 9 : "ENDFILE"}
operation_dict = {"load" : 0, "store": 1, "loadI": 2, "add": 3, "sub": 4,
                  "mult": 5, "lshift": 6, "rshift": 7, "output": 8, "nop": 9, "constant": 10, "register": 11, "comma": 12, "into": 13}
reversed_dict = {0 : "load", 1 : "store", 2 : "loadI", 3 : "add", 4 : "sub", 5 : "mult", 6 : "lshift", 7 : "rshift", 8 : "output", 9 : "nop", 10 : "constant", 11 : "register", 12 : "comma", 13 : "into"}
class FlagHandler:
    def __init__(self, filename):
        self.filename = filename
        self.buffer = None
        self.index = 0

    def h_handler(self):
        print ("COMP 412, Fall 2019 Front End (lab 1)")
        print ("Command Syntax:")
        print ("	./412fe [flags] filename")
        print ("Required arguments:")
        print ("	filename  is the pathname (absolute or relative) to the input file")
        print ("Optional flags:")
        print ("	-h	 prints this message")
        print ("	-s	 prints tokens in token stream")
        print ("	-p	 invokes parser and reports on success or failure")
        print ("	-r	 prints human readable version of parser's IR")

    def s_handler(self):
        scanner = Scanner(self.filename)
        for i in scanner.scan_big():
            print (pattern_dict[i[0]], i[1], "line" + str(i[2]))

    def p_handler(self):
        file = open(self.filename)
        scanner = Scanner(self.filename)
        parser = Parser()
        line = file.readline()
        line_count = 1
        head = DoublyLinkedList()
        prev_node = DoublyLinkedList()
        prev_node.set_prev(head)
        grammar_error = False
        grammar_error_count = 0
        lexical_error = False
        success_count = 0
        while line:
            res = []
            while line[0] == "/" and len(line) > 2 and line[1] == "/":
                line = file.readline()
                line_count += 1
                if not line:
                    res.append((9, "", line_count - 1))
                    #if not lexical_error and not grammar_error:
                        #print("Successfully parsed the ILOC file, finding " + str(success_count) + " ILOC operations")
                    return head.next.next, lexical_error or grammar_error
            if line[-1] != '\n':
                line = line + '\n'
            self.buffer = line
            encountered_error = False
            while self.buffer[self.index] != "\n":
                word_pair = self.word_scan(line_count)
                if word_pair[0] == -1:
                    lexical_error = True
                    encountered_error = True
                    break
                if word_pair[0] != -2:
                    res.append(word_pair)
                if self.index == len(self.buffer):
                    break
            if not encountered_error:
                cur_node = parser.parse_line(res)
                if cur_node:
                    success_count += 1
                    prev_node.set_next(cur_node)
                    prev_node = prev_node.next
                else:
                    if line[0] != "\n":
                        grammar_error = True
                        grammar_error_count += 1
            self.buffer = ""
            self.index = 0
            line = file.readline()
            line_count += 1
        file.close()
        #if not lexical_error and not grammar_error:
            #print("Successfully parsed the ILOC file, finding " + str(success_count) + " ILOC operations")
        #else:
        if grammar_error:
            print("Parser found " + str(grammar_error_count) + " syntax errors")
        #print (lexical_error)
        #print (grammar_error)
        return head.next.next, lexical_error or grammar_error

    def r_handler(self):
        cur_node, flag = self.p_handler()
        if not flag:
            while cur_node != None:
                res = []
                if cur_node.opcode != None:
                    res.append(reversed_dict[(cur_node.opcode)])
                if cur_node.first_operand[0] != "empty":
                    res.append(cur_node.first_operand[0])
                    if cur_node.second_operand[0] != "empty":
                        res.append(cur_node.second_operand[0])
                        if cur_node.third_operand[0] != "empty":
                            res.append(cur_node.third_operand[0])
                    elif cur_node.third_operand[0] != "empty":
                        res.append(cur_node.third_operand[0])
                print (res)
                cur_node = cur_node.next
        else:
            print("The parse was not successful caused by errors", file=sys.stderr)
            return None
        return None

    def x_handler(self):
        res = self.p_handler()[0]
        some = res.rename_algorithm()
        while some != None:
            strres = ""
            strres += reversed_dict[some.get_opcode()]
            strres += " "
            if some.get_firstOperand()[1] != "empty":
                strres += some.get_firstOperand()[1]
            else:
                if some.get_firstOperand()[0] != "empty":
                    strres += some.get_firstOperand()[0]
            if some.get_secondOperand()[0] != "empty":
                strres += ", "
                strres += some.get_secondOperand()[1]
            if some.get_thirdOperand()[0] != "empty":
                strres += " => "
                strres += some.get_thirdOperand()[1]
            print (strres)
            some = some.next

    def number_handler(self, k):
        res = self.p_handler()[0]
        renamed = res.rename_algorithm()
        answer = renamed.allocate_physical(k)
        return answer

    def word_scan(self, line_count):
        cur_char = self.buffer[self.index]
        # case for first char being s
        if cur_char == "s":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "u":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "b":
                    self.index += 1
                    return 2, "sub", line_count
                print ("Lexical Error: Found error when trying to complete word sub on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            elif next_char == "t":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "o":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "r":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "e":
                            self.index += 1
                            return 0, "store", line_count
                        print ("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print ("Lexical Error: Found error when trying to complete word store on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being comma
        elif cur_char == ",":
            self.index += 1
            return 7, "comma", line_count
        # case for first char being space
        elif cur_char.isspace():
            self.index += 1
            return -2, "space", line_count
        elif cur_char == "/":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "/":
                self.index = len(self.buffer) - 1
                return -2, "space", line_count
            print ("Lexical Error: / cannot be not followed by another /")
            return -1, str(line_count), line_count
        #case for first char being l
        elif cur_char == "l":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "o":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "a":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "d":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "I":
                            self.index += 1
                            return 1, "loadI", line_count
                        return 0, "load", line_count
                    print("Lexical Error: Found error when trying to complete word loadI on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete word loadI on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            elif next_char == "s":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "h":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "i":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "f":
                            self.index += 1
                            next_char = self.buffer[self.index]
                            if next_char == "t":
                                self.index += 1
                                return 2, "lshift", line_count
                            print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                            return -1, str(line_count), line_count
                        print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete word lshift on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being m
        elif cur_char == "m":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "u":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "l":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "t":
                        self.index += 1
                        return 2, "mult", line_count
                    print("Lexical Error: Found error when trying to complete the word mult on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete the word mult on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete the word mult on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being a
        elif cur_char == "a":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "d":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "d":
                    self.index += 1
                    return 2, "add", line_count
                print("Lexical Error: Invalid word ad" + next_char + " on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Invalid word a" + next_char + " on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being n
        elif cur_char == "n":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "o":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "p":
                    self.index += 1
                    return 4, "nop", line_count
                print("Lexical Error: Found error when trying to complete the word nop on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete the word nop on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being o
        elif cur_char == "o":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "u":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "t":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "p":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "u":
                            self.index += 1
                            next_char = self.buffer[self.index]
                            if next_char == "t":
                                self.index += 1
                                return 3, "output", line_count
                            print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                            return -1, str(line_count), line_count
                        print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            print("Lexical Error: Found error when trying to complete the word output on line" + str(line_count), file=sys.stderr)
            return -1, str(line_count), line_count
        # case for first char being =
        elif cur_char == "=":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == ">":
                self.index += 1
                return 8, "into", line_count
            else:
                print("Lexical Error: The second parameter for into should be >, line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
        # case for the first char being r
        elif cur_char == "r":
            self.index += 1
            next_char = self.buffer[self.index]
            if next_char == "s":
                self.index += 1
                next_char = self.buffer[self.index]
                if next_char == "h":
                    self.index += 1
                    next_char = self.buffer[self.index]
                    if next_char == "i":
                        self.index += 1
                        next_char = self.buffer[self.index]
                        if next_char == "f":
                            self.index += 1
                            next_char = self.buffer[self.index]
                            if next_char == "t":
                                self.index += 1
                                return 2, "rshift", line_count
                            print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                            return -1, str(line_count), line_count
                        print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                        return -1, str(line_count), line_count
                    print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                    return -1, str(line_count), line_count
                print("Lexical Error: Found error when trying to complete the word rshift on line" + str(line_count), file=sys.stderr)
                return -1, str(line_count), line_count
            if next_char.isdigit():
                if '0' <= next_char <= '9':
                    total = int(next_char)
                    self.index += 1
                    next_char = self.buffer[self.index]
                    while "0" <= next_char <= "9":
                        num = int(next_char)
                        total = total * 10 + num
                        self.index += 1
                        next_char = self.buffer[self.index]
                    return 6, "r" + str(total), line_count
                print("Lexical Error: Register does not support leading zeros on line" + line_count, file=sys.stderr)
                return -1, str(line_count), line_count
        # case when this is a number
        elif cur_char.isdigit():
            if cur_char == "0":
                self.index += 1
                return 5, cur_char, line_count
            elif '1' <= cur_char <= '9':
                cur_total = int(cur_char)
                self.index += 1
                next_char = self.buffer[self.index]
                while "0" <= next_char <= "9":
                    num = int(next_char)
                    cur_total = cur_total * 10 + num
                    self.index += 1
                    next_char = self.buffer[self.index]
                return 5, str(cur_total), line_count
            print("Lexical Error: Constant does not support leading zeros on line" + line_count, file=sys.stderr)
            return -1, str(line_count), line_count
        # case when all the above opcode recognization failed
        print ("Lexical Error: letter " + cur_char + " is not a valid input: line" + str(line_count), file=sys.stderr)
        return -1, str(line_count), line_count




#handler = FlagHandler("cc5.txt")
#res = handler.p_handler()[0]
#renamed = res.rename_algorithm()
#answer = renamed.allocate_physical(7)





