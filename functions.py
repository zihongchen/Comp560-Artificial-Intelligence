import string
import random
import unittest
import numpy as np
import math

def setup(file_name):
    #open the file
    file=open(file_name,"r")
    #read the first line
    dim=int(file.readline(1))
    #creating arrays
    letter_array=[[0]*dim for i in range(dim)]
    solution=np.array([[0]*dim for i in range(dim)])
    #letter_dict: keys are the letters,
    ##values are an array: first index: operation
    ###example: 11+
    ##second value: array with places of the letter
    letter_dict=dict()
    #loop through each line and put it in an array
    y=0
    for line in file:
        if line=='\n':
            next
        elif y==dim:
            #add letter operations
            oper=line.strip().split(":")
            letter_dict[oper[0]][0]=oper[1]
            next
        else:
            #adding value to array
            letter_array[y]=list(line.strip())
            #adding letter to dictionary and location
            x=0
            for key in list(line.strip()):
                if key in letter_dict:
                    letter_dict[key].append([y,x])
                else:
                    letter_dict[key]=["",[y,x]]
                x=x+1
            y=y+1
    return letter_array,solution,letter_dict
        
#row checker:
def row_checker(row,matrix):
    copy_mat=matrix[row].copy()
    copy_mat=[x for x in copy_mat if x != 0]
    return len(copy_mat)==len(set(copy_mat))
#column checker:
def column_checker(column,matrix):
    copy_mat=[row[column] for row in matrix].copy()
    copy_mat=[x for x in copy_mat if x != 0]
    return len(copy_mat)==len(set(copy_mat))

#letter_checker: based on location
#assumptions are that - and / only have two numbers
## true if there is a value eqaul to zero or if all the values satisfy the letter requirements
def letter_check(location,matrix,letter_array,letter_dict):
    #letter array is the martix of letters
    #letter dictionary is
        ##key is letter
        ##value is array
            ###1st value is total and operation
            ### the other values are locations of the letter
    letter=letter_array[location[0]][location[1]]
    oper=letter_dict.get(letter)[0][-1]
    #check if oper is a digit or not because some values can only be a digit with no operation 
    if oper.isdigit(): 
        total=int(letter_dict.get(letter)[0])
    else:
        total=int(letter_dict.get(letter)[0][:-1])
    values=letter_dict.get(letter)[1:]
    #for + and * not to add a operation 
    first=True
    ##there are only two values for - and /
    if(oper == "-")|(oper == '/'):
        val0=values[0]
        val1=values[1]
        num0=int(matrix[val0[0]][val0[1]])
        num1=int(matrix[val1[0]][val1[1]])
        if(num1==0)|(num0==0):
            return True
        if num0>=num1:
            total_num=str(num0)+oper+str(num1)
        else:
            total_num=str(num1)+oper+str(num0)
    #for + and *
    else:
        for val in values:
            num=matrix[val[0]][val[1]]
            if(num==0):
                return True
            if first:
                total_num=str(num)
                first=False
            else:
                total_num=total_num+oper+str(num)
    #so using eval it calucalute a math operation
    return int(total)==eval(total_num)
#checks if value at location is not 0
def check_no_zero(location,matrix):
    return matrix[location[0]][location[1]]!=0
#checks all the assumptions for the whole matrix
def check_all(matrix,letter_array,letter_dict):
    for y in range(0,len(matrix)):
            for x in range(0,len(matrix)):
                if not (check_no_zero([x,y],matrix)==
                    letter_check([x,y],matrix,letter_array,letter_dict)==
                    column_checker(y,matrix)==
                    row_checker(x,matrix)==
                    True):
                        return False
    return True
    
    
def simple_back(letter_array,matrix,letter_dict):
    #i is counter
    i=0
    row=0
    column=0
    #looping
    while(True):
        i=1+i
        #check if martix is complete
        if check_all(matrix,letter_array,letter_dict):
            return matrix, i
        else:
            #if value is 0 make it 1
            if matrix[row,column]==0:
                matrix[row,column]=1
             #check if we can move to the next node
            elif (True==
                    letter_check([row,column],matrix,letter_array,letter_dict)==
                    column_checker(column,matrix)==
                    row_checker(row,matrix)
                    ):
                        #if the location is at the end of the row
                        if(column==len(matrix)-1):
                            column=0
                            row=1+row
                        else:
                            column=column+1
            #if the node does not work and is the last value 
            elif matrix[row,column]==len(matrix):
                #goes through each of the values backwards and sets them to zero if they are the last value
                while matrix[row,column]==len(matrix):
                    matrix[row,column]=0
                    if column==0:
                        # at the first location and tried all combinations.
                        if row==0:
                              return "No Solution",i
                        column=len(matrix)-1
                        row=row-1
                    else:
                        column=column-1
                matrix[row,column]=matrix[row,column]+1
            else:
                matrix[row,column]=matrix[row,column]+1
# finds prime factors for multiplicaton                
def prime_factors(n):
    x=list()
    x.append(1)
    while n%2==0:
        x.append(2)
        n=n/2
    for i in range(3,int(math.sqrt(n))+1,2):
        while n%i==0:
            x.append(int(i))
            n=n/i
    if n>2:
        x.append(int(n))
    return x

def quick_get_choices_letters(file_name):
    letter_array,matrix,letter_dict=setup(file_name)
    return get_choices_letters(matrix,letter_dict)

# builds martix with all the possible choices
def get_choices_letters(solution,letter_dict):
    choices=[[0]*len(solution) for i in range(0,len(solution))]
    for key in letter_dict.keys():
        length=len(letter_dict.get(key))-1
        oper=letter_dict.get(key)[0][-1]
        locations=letter_dict.get(key)[1:]
        if oper.isdigit(): 
            total=int(letter_dict.get(key)[0])
        else:
            total=int(letter_dict.get(key)[0][:-1])
        options=[]
        #addtion
        if oper=="+":
            for pos in range(1,len(solution)+1):
                # if the pos is greater or equal to the total, no number can be added to it to make it the total
                if pos>=total:
                    continue
                    ## if the total-value/(length of the letter size -1) is greater than the maximum value possible, it can not be a solution
                elif math.floor((total-pos)/(length-1))>len(solution):
                    continue
                options.append(pos)
        elif oper=="*":
            primes=prime_factors(total)
            for pos in range(1,len(solution)+1):
                #check if the guess's factors are in the total's factor
                # if the all the pos's prime factors are not in the total's prime factors, then do not include them
                if all(elem in primes for elem in prime_factors(pos)):
                    ## if the total/value is greater than the maximum value possible**(length of the letter size -1), it can not be a solution
                    if (total/pos)<=(len(solution)**(length-1)):
                        options.append(pos)
        elif oper=="-":
            for pos in range(1,len(solution)+1):
                if total+pos<len(solution)+1:
                    options.append(pos)
                    options.append(total+pos)
        elif oper=="/":
            for pos in range(1,len(solution)+1):
                if total*pos<len(solution)+1:
                    options.append(pos)
                    options.append(total*pos)
        else:
            options=[total]
        for loc in locations:
                choices[loc[0]][loc[1]]=list(set(options))
    ##to start is the array of locations of where we should start
    ##ordered by size of location
    to_start=dict()
    for i in range(0,len(choices)):
        for j in range(0,len(choices)):
            to_start[str(i)+str(j)]=len(choices[i][j])
    to_start = sorted(to_start.items(), key=lambda x: x[1])
    return choices,to_start
## added letter restrictiongs
##changes are the letters contrictions and starting with the most
def complex_back(letter_array,matrix,letter_dict):
    #builds choices and the location to start the choices
    choices,to_start=get_choices_letters(matrix,letter_dict)
    i=0
    # is the value at the most constranted location 
    j=0
    row=int(to_start[j][0][0])
    column=int(to_start[j][0][1])
    while(True):
        i=1+i
        if check_all(matrix,letter_array,letter_dict):
            return matrix, i
        else:
            if matrix[row,column]==0:
                matrix[row,column]=choices[row][column][0]
                #choices=remove_location_possibilites(row,column,choices,matrix)
            elif (True==
                    letter_check([row,column],matrix,letter_array,letter_dict)==
                    column_checker(column,matrix)==
                    row_checker(row,matrix)
                    ):
                j=j+1
                row=int(to_start[j][0][0])
                column=int(to_start[j][0][1])
                ## checks if the matrix value is the last possible value in the choices array
            elif matrix[row,column]==choices[row][column][-1]:
                last_one=choices[row][column][-1]
                ##go through each of the previous values, if they are the last value of the choice martix then set it to 0 and go the the next previous location and do the same check
                while matrix[row,column]==last_one:
                    #choices=add_location_possibilites(row,column,choices,matrix,letter_dict,letter_array)
                    matrix[row,column]=0
                    j=j-1
                    if j==-1:
                        return "No Solution",i
                    row=int(to_start[j][0][0])
                    column=int(to_start[j][0][1])
                    ##last_one is the last choice in the choice martix of that location
                    last_one=choices[row][column][-1]
                if matrix[row,column]==0:
                    matrix[row,column]=choices[row][column][0]
                    #remove poss
                    #choices=remove_location_possibilites(row,column,choices,matrix)
                else:
                    ## ind is the index value of the choices of that location's current value
                    ind=(choices[row][column]).index(matrix[row,column])
                    matrix[row,column]=choices[row][column][ind+1]
                    #choices=remove_location_possibilites(row,column,choices,matrix)
            else:
                ## ind is the index value of the choices of that location's current value
                ind=(choices[row][column]).index(matrix[row,column])
                matrix[row,column]=choices[row][column][ind+1]
                #choices=remove_location_possibilites(row,column,choices,matrix)

### these are possible other function we were planing to use but it was too complex
## removes possibilites from rows and columns of choices
# def remove_location_possibilites(row,column, choices, matrix):
#     value_remove=matrix[row,column]
#     for i in range(0,len(choices)):
#         if i != row:
#             #to stop error from element not in list and do not remove all elements from list
#             if (value_remove in choices[i][column])&len(choices[i][column])>1:
#                 choices[i][column].remove(value_remove)
#         if i != column:
#             if (value_remove in choices[row][i])&len(choices[row][i])>1:
#                 choices[row][i].remove(value_remove)
#     return choices


##remove letter choices  
##not using it because i got confused
# def remove_letter(value,row,column,choices,letter_dict,letter_array):
#     key=letter_array[row][column]
#     length=len(letter_dict.get(key))-1
#     oper=letter_dict.get(key)[0][-1]
#     if oper.isdigit(): 
#         total=int(letter_dict.get(key)[0])
#     else:
#         total=int(letter_dict.get(key)[0][:-1])
#         return choices
#     #ignoring + and * because they are completated
#     if oper=="+":
#         if length==2:
#             choices[row][column].remove(total-value)
#         return choices
#     elif oper=="*":
#         return choices
#     elif oper=="-":
#         for pos in range(1,len(solution)+1):
#             if total+pos<len(solution)+1:
#                 options.append(pos)
#                 options.append(total+pos)
#         if value>total:
#             value-total=total
#             options.remove(value)
#             options.remove(total)
#     elif oper=="/":
#         for pos in range(1,len(solution)+1):
#             if total*pos<len(solution)+1:
#                 options.append(pos)
#                 options.append(total*pos)
#         options.remove(value)
#         if value>total:
#             value/total=total
#             options.remove(total)
            
#     else:
#         options=[total]
#     for loc in locations:
#             choices[loc[0]][loc[1]]=list(set(options))
    
    

##add letter choices
# def add_letter(value,row,column,choice,letter_dict,letter_array):
#     key=letter_array[row][column]
#     length=len(letter_dict.get(key))-1
#     oper=letter_dict.get(key)[0][-1]
#     if oper.isdigit(): 
#         total=int(letter_dict.get(key)[0])
#     else:
#         total=int(letter_dict.get(key)[0][:-1])
#     options=[]
#     pos=value
#     #addtion
#     if oper=="+":
#         if not ((pos<=total)|(math.floor((total-pos)/(length-1))>len(letter_array))):
#             choice[row][column].append(pos)
#     elif oper=="*":
#         primes=prime_factors(total)
#         #check if the guess's factors are in the total's factor
#         if all(elem in primes for elem in prime_factors(pos)):
#             # checks if it can fit inside the given space.
#             ##thinking about it
#             if (total/pos)<=(len(letter_array)**(length-1)):
#                    choice[row][column].append(pos)
#     elif oper=="-":
#         if total+pos<len(letter_array)+1:
#                choice[row][column].append(pos)
#     elif oper=="/":
#         for pos in range(1,len(letter_array)+1):
#             if total*pos<len(letter_array)+1:
#                 choice[row][column].append(pos)
#     else:
#         choice[row][column]=[total]
#     choice[row][column]=list(set(choice[row][column]))
#     return choice[row][column]
    


# ##adds possibilities from rows and columns of choices
# def add_location_possibilites(row,column, choices, matrix,letter_dict,letter_array):
#     value_add=matrix[row,column]
#     for i in range(0,len(choices)):
#         if i != row:
#             #do not want to add multiple values
#             if not value_add in choices[i][column]:
#                 choices[i][column]=add_letter(value_add,i,column,choices,letter_dict,letter_array)
#         if i != column:
#             if not value_add in choices[row][i]:
#                 choices[row][i]=add_letter(value_add,row,i,choices,letter_dict,letter_array)
#     return choices
    
                
                
## combines all the searches                
def combination_searches(file_name):
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    letter_array,matrix,letter_dict=setup(file_name)
    sol_back,ib=simple_back(letter_array,matrix.copy(),letter_dict)
    sol_back_com,ibc=complex_back(letter_array,matrix.copy(),letter_dict)
    if sol_back=="No Solution":
        print(sol_back)
    else:
        for i in range(0,len(sol_back_com)):
            line = ' '.join(str(e) for e in sol_back_com[i])
            print(line)
    print()
    print(ib)
    print(ibc)