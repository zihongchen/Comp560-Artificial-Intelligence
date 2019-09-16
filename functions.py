import string
import random
import unittest
import numpy as np

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
def letter_check(location,matrix,letter_array,letter_dict):
    letter=letter_array[location[0]][location[1]]
    oper=letter_dict.get(letter)[0][-1]
    if oper.isdigit(): 
        total=int(letter_dict.get(letter)[0])
    else:
        total=int(letter_dict.get(letter)[0][:-1])
    values=letter_dict.get(letter)[1:]
    first=True
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
    return int(total)==eval(total_num)

def check_no_zero(location,matrix):
    return matrix[location[0]][location[1]]!=0
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
    i=0
    row=0
    column=0
    while(True):
        i=1+i
        ##
        if i>1000:
            print(matrix)
        ##
        if check_all(matrix,letter_array,letter_dict):
            return matrix, i
        else:
            if matrix[row,column]==0:
                matrix[row,column]=1
            elif (True==
                    letter_check([row,column],matrix,letter_array,letter_dict)==
                    column_checker(column,matrix)==
                    row_checker(row,matrix)
                    ):
                        if(column==len(matrix)-1):
                            column=0
                            row=1+row
                        else:
                            column=column+1
            elif matrix[row,column]==len(matrix):
                matrix[row,column]=0
                if column==0:
                    column=len(matrix)-1
                    row=row-1
                else:
                    column=column-1
                    if matrix[row,column]==len(matrix):
                        while matrix[row,column]==len(matrix):
                            matrix[row,column]=0
                            if column==0:
                                column=len(matrix)-1
                                row=row-1
                            else:
                                column=column-1
                    else:
                        matrix[row,column]=matrix[row,column]+1
            else:
                matrix[row,column]=matrix[row,column]+1