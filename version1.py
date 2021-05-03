import csv
import re



# definition des constantes:
BOTTOM =  "⊥"



def GetClassC():
    """
     Defintion de la classe de token C,
    Il s'agit d'un dico dont les cles st les noms de tokens et
    les valeurs st les expressions regulieres correspondantes 
     """
    ClasseC ={}

    with open('classeC.csv', mode='r') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=';')
        for token in csv_reader:
            ClasseC[token[0]] = token[1]
        ClasseC['SemiColonTok'] = ";"
    return ClasseC

ClasseC = GetClassC()


def Cpos(s,k):
    if(k>= 0):
        return k
    else:
        return len(s) + k


cpos = Cpos("laure", -1)


def TokenSeq(*tokens):
    """ contruit une sequence(concatenation)d'expression regulieres """
    TokenSeqResult = ""
    for token in tokens:
        TokenSeqResult = TokenSeqResult+token
    return TokenSeqResult


def Pos(s,r1,r2,c):
    """ 
        Retourne l'indice de debut du cieme matching de l'expression reguliere 
        TokenSeq(r1,r2)
    """
    r = TokenSeq(r1, r2)
    
    r = re.compile(r)
    r1 = re.compile(r1)
    r2 = re.compile(r2)
    RegulationExpression = r.findall(s)
    
    if len(RegulationExpression) >= abs(c):
        e = abs(c)-1
        if c > 0:
            
            res = re.search(RegulationExpression[e],s)
            res1 = re.search(r1,s)
            Taille = res1.end() - res1.start() 
            t = res.start() + Taille       
                
        else:
            e = len(RegulationExpression) + c
            res = re.search(RegulationExpression[e],s)
            res1 = re.search(r1,s)
            Taille = res1.end() - res1.start() 
            t = res.start() + Taille
        return t
    else:
        return BOTTOM

""" pos = Pos("425-706-7709", ClasseC['HyphenTok'],ClasseC['NumTok'],-2)
pos1 = Pos("425-706-7709", ClasseC['NumTok'],ClasseC['HyphenTok'],-2)
print(pos)
print(pos1)
 """


def GenerateRegularExpressionLeft(s,k):
    """ 
    Retourne l'ensemble des expressions regulieres qui existennt dans  s[k1:k] 
    pour k1 variant de 0 a k-1
    """
    k1 = 0
    r1 = []
    Tokens = []
    while  k1 <= k-1 :
        for cle in ClasseC:
            Token = ClasseC[cle]
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s[k1:k])
            
            if Test != None:
                k1 = k1 + Test.start()
                Tokens.append((k1,Token,cle))
                k1 =  k1 + Test.end()
              
                break
    Taille = len(Tokens)
    i = 0
    while  i < Taille :
        Expression = "".join([str(elt[1]) for elt in Tokens[i: Taille]])
        Expression2 = ",".join([str(elt[2]) for elt in Tokens[i: Taille]])#donne l'ecriture sur forme de cle: Numtok, Hyphentok...
        r1.append((Tokens[i][0],Expression,Tokens[i: Taille],Expression2))
        i = i +1
    return r1   


def GenerateRegularExpressionRigth(s,k):
    
    """ Retourne l'ensemble des expressions regulieres qui existennt dans  s[k1:k] 
    pour k1 variant de 0 a k-1 """
   
    k1 = k
    r1 = []
    Tokens = []
    Longueur = len(s)
    while  k1 < Longueur:
        for cle in ClasseC:  
            Token = ClasseC[cle]
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s[k1:Longueur])
            
            if Test != None:
                k1 = k1 + Test.end()-1 # on doit nomalement faire end()-1, mais pour respecter l'indexation de python on prend end()
                Tokens.append((k1,Token,cle))
                k1 = k1 + 1
                break

    Taille = len(Tokens)
    #print(Tokens)
    i = 0
    while  i < Taille:
        Expression = "".join([str(elt[1]) for elt in Tokens[0: i+1]])
        Expression2 = ",".join([str(elt[2]) for elt in Tokens[0: i+1]])
        r1.append((Tokens[i][0],Expression,Tokens[0: i+1],Expression2))
        i = i +1
    return r1   

""" test = GenerateRegularExpressionRigth("425-706-7709",4)
print(test) """


def MatchExpression(l,s):
    """ 
    etant donnee une l, cette fonction retourne l'indice(l'occurence) de s 
    """
    try:
        return l.index(s) + 1

    except ValueError:
        return 0



def GeneratePosition(s,k):
     
    """ retourne l'ensemble des differentes facons de representer une position
    donnee dans une chaine donnee avec les primitives du langage  """
    POsList = []  # variable de formatage 
    PosChain = ""
    result = set([Cpos(s,k), Cpos(s,-(len(s)-k))])
    PosChain = "Cpos("+s+","+str(k)+")"
    POsList.append(PosChain)
    PosChain = "Cpos("+s+",-"+str((len(s)-k))+")"
    POsList.append(PosChain)
    #print(result)
    R1List = GenerateRegularExpressionLeft(s,k)
    #print(R1List)
    #print("****")
    R2List = GenerateRegularExpressionRigth(s,k)
   
    #print(R2List)

    for r1 in R1List :
        for r2 in R2List :
            r12 = TokenSeq(r1[1],r2[1])
            r12 = re.compile(r12)
            MatchingList = r12.findall(s)
            c = MatchExpression(MatchingList,s[r1[0]:r2[0]+1])
            c1 = len(MatchingList)
            if c!=0 and (r1[2][len(r1[2])-1][1] != r2[2][0][1]):
        
                c1 = -(c1 -c +1)
                PosChain = "Pos("+s+",TokenSeq("+r1[3]+"),TokenSeq("+r2[3]+"),"+str(c)+")"
                POsList.append(PosChain)
                PosChain = "Pos("+s+",TokenSeq("+r1[3]+"),TokenSeq("+r2[3]+"),"+str(c1)+")"
                POsList.append(PosChain)

                result = result.union(set([Pos(s,r1[1],r2[1],c),Pos(s,r1[1],r2[1],c1)]))

    return result,set(POsList)
         
positions,poslist = GeneratePosition("425-706-7709",4)
print(positions)
print(poslist)



def GenerateSubstring(entre,s):
    """  """
    result = {}

