//NAME: Zikai Zhu
//NETID: zz51

Description:
Parser.py(the parser), Scanner.py(the scanner), FlagHandler.py(the flag handler), DoublyLinkedList.py(the class that I wrote for the IR), lab1.py(where it handles the commands) are the source codes for my frontend project. 412fe is the script to start the program.

Command Syntax:
	./412fe [flags] filename

	Required arguments:
	filename is the pathname (absolute or relative) to the input file

    	-h prints helper message that guides the user
    	-s prints tokens in token stream
    	-p invokes parser and reports on success or failure
    	-r prints human readable version of parser's IR

Running instruction:

Open the folder that is created by unzipping the tar file and run the script according to the command syntax should be fine.

Design decisions:

For this frontend project, I used Python 3 to write the code(so in the 412fe script I used python3). Also, I chose to write a doubly linked list object that has a ‘previous’ and a ‘next’ field to represent the IR of the parser result. 

Another important design decision that I made was that if there is a lexical error already on a specific line, I would not bother to parse that line and return a grammar error as it is impossible for a line to be lexically wrong to be parsed successfully so that is why my error message for some of the test cases are different from the ones of the ref solution(where it also prints the grammar error)

Also, for the -s flags, if there is a lexical error in the line, it would skip that line and ignore if there are more lexical errors on that line.
