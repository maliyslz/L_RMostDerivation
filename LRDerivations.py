FILE_LL = "ll.txt"
FILE_LR = "lr.txt"
FILE_INPUT = "input.txt"

ll_no=1
def check_input(input,ll_table):
    temp=[]
    checked_input=[]
    while True:
        if input == "$":
            temp.append("$")
            break
        for i in range(1, len(ll_table[0])):
            index, new_string = find_and_remove_substring(input, ll_table[0][i])
            if index == 0:
                input = new_string
                temp.append(ll_table[0][i])
                break
            if i == len(ll_table[0])-1:
                return 0
    checked_input.extend(reversed(temp))
    return checked_input

def find_and_remove_substring(string, substring):
    index = string.find(substring)
    if index == 0:
        string = string[:index] + string[index+len(substring):]
    return index, string

def reverse_and_convert_to_str(lst):
    return ''.join(lst[::-1])

def print_list(lst, is_spaced):
    separator = " " if is_spaced else ""
    return separator.join(lst)

def align(text, length):
    return str(text).ljust(length)

def write_rule_to_stack(rule): 
    temp = []
    result_stack = [] 
    right_side_of_rule = rule[3:]
    all_elements = [row[0] for row in ll_table[1:]]
    all_elements.extend(ll_table[0][1:])
    all_elements.remove('$')
    while right_side_of_rule:
        for i in range(len(all_elements)):
            index, new_string = find_and_remove_substring(right_side_of_rule, all_elements[i])
            if index == 0:
                right_side_of_rule = new_string
                temp.append(all_elements[i])
                break
            if i == len(all_elements)-1:
                return 0
    result_stack.extend(reversed(temp))
    return temp


def find_next_action(action_stack,input_stack):
    global ll_no
    x=-1
    y=-1
    if ll_no == 1:
        action_stack=ll_table[1][0]
        for item in ll_table[1]:
            if item!="" and item!=action_stack:
                y=ll_table[1].index(item)
                x=1
                break
    elif action_stack[-1]==input_stack[-1]:
        print(f"{align(ll_no,2)} | {align(print_list(action_stack,0),15)} | {align(reverse_and_convert_to_str(input_stack),15)} | Match and remove {input_stack[-1]}")
        ll_no+=1
        action_stack.pop()
        input_stack.pop()

    for i in range(len(ll_table)):
        if action_stack[-1] in ll_table[i][0] :
            x=i
            break
    for  j in range(len(ll_table[0])):
        if y==-1 and input_stack[-1] in ll_table[0][j]:
            y=j
    if(ll_table[x][y]==""):
        if action_stack[-1] =="$":
            return f"REJECTED (There are no elements left in the stack)"
        return f"REJECTED ({action_stack[-1]} does not have an action/step for {input_stack[-1]})"
    return ll_table[x][y]

def LL_der(input_LL):
    global ll_no
    try:
        ll_no=1
        print("NO | STACK           | INPUT           |ACTION")
        action_stack=['$']
        input_stack=check_input(input_LL,ll_table)
        if input_stack == 0:
            print("\nThe input string contains undefined characters.")
            return
        next_action=[]
        while("REJECT" not in next_action):
            next_action=find_next_action(action_stack,input_stack) 
            print(f"{align(ll_no,2)} | {align(print_list(action_stack,0),15)} | {align(reverse_and_convert_to_str(input_stack),15)} | {align(next_action,15)}")
            if "REJECT" in next_action:
                return
            if ll_no != 1:
                action_stack.pop()
                if(action_stack==input_stack):
                    ll_no+=1
                    print(f"{align(ll_no,2)} | {align(print_list(action_stack,0),15)} | {align(reverse_and_convert_to_str(input_stack),15)} | ACCEPT")
                    break
            
            ll_no+=1
            if(next_action[3]!="ϵ"):
                checked_next_action=write_rule_to_stack(next_action)
                if checked_next_action == 0:
                    print("\nThe table contains undefined characters.")
                    return
                while(len(checked_next_action)!=0):
                    action_stack.append(checked_next_action.pop())
    except IndexError:
        print("An index error occurred. Please check your input and table data.")

def LR_der(input_LR):
    try:
        print("NO | STATE STACK     | READ            | INPUT           |ACTION")
        no=1
        state_stack=[]
        state_stack.append(lr_table[2][0][6:])
        input=input_LR
        next=0
        action_Str=""
        while "REJECT" not in action_Str:
            strRead=input[next]
            set_of_rules=action(state_stack[-1],strRead)
            action_Str=set_of_rules[1]
            rules=set_of_rules[0]
            print(f"{align(no,2)} | {align(print_list(state_stack,1),15)} | {align(strRead,15)} | {align(input,15)} | {align(action_Str,15)}")
            if(set_of_rules[2]==0 or set_of_rules[2]==1):
                break
            elif set_of_rules[2]==2:
                state_stack.append(set_of_rules[3])
                next+=1
            elif set_of_rules[2]==3:
                for i in range(len(rules[3:])):
                    state_stack.pop()
                input=input.replace(rules[3:],rules[0])
                next=input.index(rules[0])

            no+=1
    except IndexError:
        print("An index error occurred. Please check your input and table data.")

        
def action(state,readstr):
    situation=0
    state=str(state)
    for i in range(len(lr_table)):
        if state in lr_table[i][0]:
            x=i
            break
    if readstr in lr_table[1]:
        y=lr_table[1].index(readstr)
    if lr_table[x][y]=="":
        return lr_table[x][y],f"REJECTED (State {state} does not have an action/step for {readstr})",situation
    if lr_table[x][y]=="Accept":
        message=lr_table[x][y]
        situation=1
    elif "State" in lr_table[x][y]:
        message="Shift to state "+lr_table[x][y][6:]
        situation=2
    else :
        message="Reverse "+lr_table[x][y]
        situation=3
    return lr_table[x][y],message,situation,lr_table[x][y][6:]

try:
    with open(FILE_LL, "r", encoding="utf-8") as file:
        content = file.readlines()
    ll_table = [row.strip().split(";") for row in (line.replace(" ", "") for line in content)]
    print("Read LL(1) parsing table from file ll.txt.")
except FileNotFoundError:
    print("Error: Unable to find ll.txt file.")
    exit()

try:
    with open(FILE_LR, "r",encoding="utf-8") as file:
        content = file.readlines()
    lr_table = [row.strip().split(";") for row in (line.replace(" ", "") for line in content) ]
    print("Read LR(1) parsing table from file lr.txt.")
except FileNotFoundError:
    print("Error: Unable to find lr.txt file.")
    exit()

try:
    with open(FILE_INPUT, "r",encoding="utf-8") as file:
        inputfile = file.readlines()
    inputs=[row.strip().split(";") for row in (line.replace(" ", "") for line in inputfile) ]
    print("Read input strings from file input.txt.")
except FileNotFoundError:
    print("Error: Unable to find input.txt file.")
    exit()
     
index_of_inputs=inputs[0].index("input")
index_of_tables=inputs[0].index("table")
for i in range(1,len(inputs)):
    try:
        if(inputs[i][index_of_tables]=="LL"):
            print(f"\nProcessing input string {inputs[i][index_of_inputs]} for LL(1) parsing table.\n")
            LL_der(inputs[i][index_of_inputs])
        elif inputs[i][index_of_tables]=="LR":
            print(f"\nProcessing input string {inputs[i][index_of_inputs]} for LR(1) parsing table.\n")
            LR_der(inputs[i][index_of_inputs])
        else:
            print("\nInvalid Table Value\n")
    except Exception as e:
        print(f"Error processing input string {inputs[i][index_of_inputs]}: {e}")