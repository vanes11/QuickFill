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

# print(c['RightParenthesisTok'])


def Cpos(s,k):
    if(k>= 0):
        return k
    else:
        return len(s) + k


cpos = Cpos("laure", -1)
# print(cpos)


def TokenSeq(*tokens):
    """ contruit une sequence(concatenation)d'expression regulieres """
    TokenSeqResult = ""
    for token in tokens:
        TokenSeqResult = TokenSeqResult+token
    return TokenSeqResult

# print(TokenSeq(ClasseC ['HyphenTok'], ClasseC ['EndTok']))

#print(c['Bottom'])
def Pos(s,r1,r2,c):
    """ 
        Retourne l'indice de debut du cieme matching de l'expression reguliere 
        TokenSeq(r1,r2)
    """
    #print(len(s))
    r = TokenSeq(r1, r2)
    r = re.compile(r)
    RegulationExpression = r.findall(s)
   
    if len(RegulationExpression) >= abs(c):
        e = abs(c)-1
        if c > 0:
            
            res = re.search(RegulationExpression[e],s)
            t = res.start()
           
                
        else:
            RegulationExpression.reverse()
            res = re.search(RegulationExpression[e],s)
            t = res.start()
        return t
    else:
        return BOTTOM

pos = Pos("22van 11laure12van3remeo11", ClasseC ['NumTok'],ClasseC ['AlphTok'],5)
#print(pos)


def GenerateRegularExpressionLeft(s,k):
    """ 
    Retourne l'ensemble des expressions regulieres qui existennt dans  s[k1:k] 
    pour k1 variant de 0 a k-1
    """
    k1 = 0
    r1 = []
    Tokens = []
    while  k1 <= k-1 :
        #print(k1)
        for cle in ClasseC:
            Token = ClasseC[cle]
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s[k1:k])
            
            if Test != None:
                # comment sortir du for, lorque Test
                k1 = k1 + Test.end()-1
                Tokens.append((k1,Token))
                
    Taille = len(Tokens)
    i = 0
    #print(Tokens)
    Tokens.reverse()
    while  i < Taille :
        i = i +11
        Expression = "".join([str(elt[1]) for elt in Tokens[i: Taille]])
        r1.append((Tokens[i][0],Expression))
    return r1   


def GenerateRegularExpressionRigth(s,k):
    """ 
    Retourne l'ensemble des expressions regulieres qui existennt dans  s[k1:k] 
    pour k1 variant de 0 a k-1
    """
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
            # comment sortir du for, lorque Test
                k1 = k1 + Test.end()-1
                """ print("valeur de k1:",k1)
                print(Token) """
                Tokens.append((k1,Token))
            
    Taille = len(Tokens)
    #print(Tokens)
    Tokens.reverse()
    i = 0
    while  i < Taille:
        i = i +1
        Expression = "".join([str(elt[1]) for elt in Tokens[i: Taille]])
        r1.append((Tokens[i][0],Expression))
    return r1   




test1 = GenerateRegularExpressionLeft("425-706-7709",5)
print(test1)
test = GenerateRegularExpressionRigth("425-706-7709",4)
print(test)




def MatchExpression(l,s):
    """ 
    etant donnee une l, cette fonction retourne l'indice(l'occurence) de s 
    """
    try:
        return l.index(s)

    except ValueError:
        return 0



def GeneratePosition(s,k):
    """  
    retourne l'ensemble des differentes facons de representer une position
    donnee dans une chaine donnee avec les primitives du langage 
    """
    result = set([Cpos(s,k), Cpos(s,-(len(s)-k))])

    R1List = GenerateRegularExpressionLeft(s,k)
    print(R1List)
    print(R1List[1][1])
    R2List = GenerateRegularExpressionRigth(s,k)
    print(R2List[1][1])
    print(R2List)

    for r1 in R1List :
        for r2 in R2List :
            print("valeur de r1:",r1)
            print("valeur de r2:",r2)
            r12 = TokenSeq(r1[1],r2[1])
            print("valeur de r12:",r12)
            r12 =  re.compile(r12)
            MatchingList = r12.findall(s)
            print(MatchingList)
            print(r1)
            print(r2)
            print(r1[0])
            c = MatchExpression(MatchingList,s[r1[0], r2[0]])
            c1 = len(MatchingList)
            c1 = -(c1 -c +1)
            result = result.union(set([Pos(s,r1[1],r2[1],c),Pos(s,r1[1],r2[1],c1)]))
            

    return 0
         
#positions = GeneratePosition("425-706-7709",4)
#print(positions)




def GenerateSubstring(entre,s):
    """  """
    result = {}

