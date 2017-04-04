from collections import defaultdict

def getpure(key, inclause):

    for row in inclause:
        for item in row:
            if item == "~" + key:
                return False
    return True

def getpure1(key, inclause):
    for row in inclause:
        for item in row:
            if item == key:
                return False
    return True

def purelit(unique,initclauses):
    # pure = []
    for key in unique:
        if key.find("~") == -1 and getpure(key, initclauses):
            return key,1

    for key in unique:
        if key.find("~") != -1 and getpure1(key, initclauses):
            return key,0

    return None,None

def unit_clause_assign(clause, model):
    P, value = None, None
    for literal in clause:
        sym, positive = inspect_literal(literal)
        if sym in model:
            
            if model[sym] == positive:
                return None, None  
        elif P:
            return None, None      
        else:
            
            P, value = sym, positive
    return P, value


def inspect_literal(literal):
    if literal[0] == '~':
        return literal[1:], 0
    else:
        return literal, 1

def eval(clauses,model):
    flag = 0
    for lit in clauses:
        if lit[0]=="~":
            if lit[1:] not in model:
                return None
            if model[lit[1:]]==0:
                return 1
        else:
            if lit not in model:
                return None
            if model[lit]==1:
                return 1
    return 0


def checkfalse(clauses,model):
    if eval(clauses,model)==1:
        return False
    elif eval(clauses,model)==0:
        return True
    return False

def checktrue(clauses,model):
    for lit in clauses:
        if lit[0]=="~":
            if lit[1:] not in model:
                return False
            if model[lit[1:]] == 0:
                return True
        else:
            if lit not in model:
                return False
            if model[lit]==1:
                return True
    return True

def getunknown(initclauses,model):
    unknownclauses=[]
    for row in initclauses:
        flag=0
        for lit in row:
            if model[lit]==0:
                flag=1
                break
        if flag==1:
            unknownclauses.append(row)
    return unknownclauses

def getunit(clauses, model):
    for clause in clauses:
        P, value = unit_clause_assign(clause, model)
        if P:
            return P, value
    return None, None

def dpll(initclauses,unique,model):

    unknownclauses=[]

    for cl in initclauses:
        if checkfalse(cl,model):
            return False
        if not checktrue(cl,model):
            unknownclauses.append(cl)

    if unknownclauses == []:
        return model

    pure,val=purelit(unique,unknownclauses)

    if pure!=None:
        if(pure.find("~")==-1):
            model[pure]=1
            for item in unique:
                if item == pure:
                    unique.remove(item)
        else:
            model[pure[1:]] = 1
            for item in unique:
                if item == pure[1:]:
                    unique.remove(item)
        
        return dpll(unknownclauses, unique, model)

    unit,val=getunit(unknownclauses,model)

    if unit!=None:
        if unit[0]=="~":
            if val==0:
                model[unit[1:]] = 1
            else:
                model[unit[1:]] = 0
            for item in unique:
                if item == unit[1:]:
                    unique.remove(item)
        else:
            model[unit] = val
            for item in unique:
                if item == unit:
                    unique.remove(item)

        return dpll(unknownclauses, unique, model)

    if len(unique)>0:
        first=unique[0]
        modelcopy=defaultdict(int)
        for elem in model:
            modelcopy[elem]=model[elem]
        if (first.find("~") == -1):
            model[first] = 1
            for item in unique:
                if item == first:
                    unique.remove(item)
        else:
            model[first] = 0
            for item in unique:
                if item == pure[1:]:
                    unique.remove(item)
        
        if (first.find("~") == -1):
            modelcopy[first] = 0
            for item in unique:
                if item == first:
                    unique.remove(item)
        else:
            modelcopy[first] = 1
            for item in unique:
                if item == first[1:]:
                    unique.remove(item)


        return dpll(unknownclauses, unique, model) or dpll(unknownclauses, unique, modelcopy)




file=open("input.txt","r")
content=file.read().splitlines()
firstline=content[0]
guests=(int)(firstline.split()[0])
tables=(int)(firstline.split()[1])


frenmy=[]
for i in range(guests):
    row = []
    for j in range(guests):
        if(i>j):
            row.append('X')
        else:
            row.append('0')
    frenmy.append(row)

for i in content[1:]:
    row=i.split()
    g1 = (int)(row[0])
    g2 = (int)(row[1])
    ch = row[2]
    if ch=='F':
        cur = frenmy[g1 - 1]
        cur[g2 - 1] = '1'
    if ch=='E':
        cur = frenmy[g1 - 1]
        cur[g2 - 1] = '-1'

literallist=[]
initclauses=[]
for i in range(guests):
    row1=[]
    row2 = []
    for j in range(tables):
        strlit1="x"+str(i + 1) +"-"+ str(j + 1)
        row1.append(strlit1)
        if(tables>1):
            strlit2 = "~x" + str(i + 1) +"-"+ str(j + 1)
            row2.append(strlit2)
    if(row1!=[]):
        initclauses.append(row1)
    if (row2 != []):
        initclauses.append(row2)

for j in range(tables):
    for i in range(guests):
        for k in range(i+1,guests):
            if(frenmy[i][k]=='1'):
                row1 = []
                strlit1="~x"+str(i + 1) +"-"+ str(j + 1)
                strlit2 = "x" + str(k + 1) +"-"+ str(j + 1)
                row1.append(strlit1)
                row1.append(strlit2)
                initclauses.append(row1)
                
                row1=[]
                strlit3 = "x" + str(i + 1) +"-"+ str(j + 1)
                strlit4 = "~x" + str(k + 1) +"-"+ str(j + 1)
                row1.append(strlit3)
                row1.append(strlit4)
                initclauses.append(row1)
                

for j in range(tables):
    for i in range(guests):
        for k in range(i+1,guests):
            if(frenmy[i][k]=='-1'):
                row1 = []
                strlit1 = "~x" + str(i + 1) +"-"+ str(j + 1)
                strlit2 = "~x" + str(k + 1) +"-"+ str(j + 1)
                row1.append(strlit1)
                row1.append(strlit2)
                initclauses.append(row1)

unique = defaultdict(int)
uniqueelements=[]
for row in initclauses:
    for item in row:
        unique[item]=unique[item]+1

for key in unique:
    if key.find("~") == -1:
        uniqueelements.append(key)

model = defaultdict(int)

ans = dpll(initclauses,uniqueelements, model)

out = open("output.txt", "w")

if ans == 0:
    out.write("no")
else:
    anslist = []

    for key in model.keys():
        if key > 0 and model[key] == 1:
            anslist.append(key[1:])


    anslist.sort()
    added = []
    out.write("yes\n")
    for line in anslist:
        itms = line.split("-")
        if itms[0] in added:
            continue
        added.append(itms[0])
        out.write("%s %s \n" % (itms[0], itms[1]))