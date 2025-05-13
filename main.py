							
# int precedence (char value);	- Trixie
# main - Trixie	
# string evaluateFloatExp (stack <float> mystack, string postfix); - Trixie

print("The SNOL environment is now active, you may proceed with giving your commands.\n")

while input != "EXIT!":
    prompt = input("Command: ")

    commands(prompt)

    match prompt: 
        case 0:
            print("ERROR: The command does not match any valid command in SNOL.")
        case 1: 
            if syntaxValidation(input_str, 1):
                tokenizer.BEG(input_str)
        case 2: 
            if syntaxValidation(input_str, 1):
                tokenizer.BEG(input_str)
        case 3:
            print("\nInterpreter is now terminated...")
            return
        case 4:
            if not syntaxValidation(input_str, 4):
                continue
            if tokenizer.varValidation(input_str):
                value = tokenizer.getValue(input_str)
                postfixConversion(value)
        case 5:
            if syntaxValidation(input_str, 5):
                tokenizer.assignmentOp(input_str)
        case 6:
            manual()

    
