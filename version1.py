import csv
import re



# definition des constantes:
BOTTOM =  "⊥"


""" 1) **** definition de la classe  C de Tokens utiliser dans les primitives de notre langage **** """


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



""" 2) **** Definition des primitives de baseses **** """


def Cpos(s,k):
    if(k>= 0):
        return k
    else:
        return len(s) + k


#cpos = Cpos("laure", -1)
#print(cpos)


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
    
    """ Retourne l'ensemble des expressions regulieres qui existennt dans  s[k:k2] 
    pour k2 variant de k a len(s) """
   
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


""" 3)*** implementation de GeneratePostion, cette fonction s'appuie sur les precedentes **** """



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
    R1List = GenerateRegularExpressionLeft(s,k)
    R2List = GenerateRegularExpressionRigth(s,k)

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
         
""" positions,poslist = GeneratePosition("425-706-7709",6)
print(poslist)
print(positions)
print(len(poslist)) """




def SubStr(s,p1,p2):
    """ 
    Expression de sous chaine tel que formuler dans l'article, un peu != de celle de python.l'indexation commence a 0
    """
    # par la suite on utile la fonction substring de python a ajoutant a l'indice de fin
    p2 = p2+1
    return s[p1:p2]




def SubStrs(s,p1,p2):
    """
    p1 et ps sont les ensemble de positions 
    """
    SubList = []  # pour affichage
    SubChain = ""
    for i in p1:
        for j in  p2:
            #result = result.union(set([SubStr(s,i,j)])) # ce ci n'est pertinent que lorsque l'ensemble p1 tout comme p2
            # represente les valeurs diff, ce qui n'est pas le cas pour nous
            #SubChain = "SubStr("+s+","+str(i)+","+str(j)+")"
            SubChain = "SubStr("+s+","+i+","+j+")"# pour  le formatage, on laisse i et j pour avoir les expressions pos et cpos
            SubList.append(SubChain)
    
    return set(SubList)


""" test = SubStrs("425-706-7709",{"Pos(HyphenTok,NumTok,1)"},{"cpos(2)","Pos(NumTok, TokenSeq(HyphenTok,NumTok),2)"})
print(test) """


""" 4) **** Implementation de GenerateSubstring, fonction principale de GenerateStr *** """


def GenerateSubstring(entree,s):
    """ 
    Pour un etat d'entree sigma et une sortir s, cette fonction retourne l'ensemble des expressions Substr() 
    de notre langage qui permette d'obtenir d'extraire la chaine s dans l'entree sigma.
    l'etat d'entree sigma est un dictionnaire : les cle sont  vi et les valeurs sont des chaine de caracteres.
    ---------
    Ce qui nous interesse c'est l'affichage avec les expression pos et cpos, car la valeur est unique.
    """
    result = set()
    for cle in entree:
        # cle = vi, nom de colonne
        if s in entree[cle]:
            k = entree[cle].index(s)
            
            k1 = len(s)+k-1
            Y1 = GeneratePosition(entree[cle],k)
            Y1 = Y1[1] # je ne comprend pas pourquoi Y1 et Y2 sont des tuplets d'ensemble
            #print("valeur de Y1: ",Y1)
            Y2 = GeneratePosition(entree[cle], k1)
            #print("valeur de Y2: ",Y2[1])
            Y2 = Y2[1] # je ne comprend pas pourquoi Y1 et Y2 sont des tuplets d'ensemble
            SubResult = SubStrs(entree[cle],Y1,Y2) # le resultat de Substrs est deja un set
            
            #print("Result final: ",SubResult)
            result = result.union(SubResult) 

    return result

""" test = GenerateSubstring({"v1":"425-706-7709"},"706")
print(len(test)) """


def  GenerateStr(entree, s):
    """ 
    cette fonction retourne  l'ensemble des facons d'obtenir s a partir del'etat d'entree sigma
    elle retourne un dag, une structure de donnee qui permet de representer des grand ensemble
    elle utilse le principe de l'algorithme CUK, base sur la programmation dynamique, qui consiste a reconnaitre un mot
    dans un langage en passant  par sa table de transition.
    """

    EtaTilda = set() # ensemble des noeuds du dag resultat
    EtaSource = set([0]) 
    EtaTarget = set([len(s)]) 
    PsiTilda = set() #ensemble des aretes de notre dag
    W = {} # table de transition, pour chaque arrete (i,j) associe l'etique qui est un ensemble d'expressions at0mique

    for i in range(len(s)+1):
        EtaTilda = EtaTarget.union(set([i])) 

    for i in range(len(s)+1):
        k = i+1
        for j in range(k,len(s)+1):

            PsiTilda = PsiTilda.union(set([(i,j)]))
   
    for i in PsiTilda:      
        x = "ConstStr("+s[i[0]:i[1]]+")"
        #print("valeur de x est :", x)
        ConstString = set([x])
        SubString = GenerateSubstring(entree,s[i[0]:i[1]])
        #print("valeurs de SubString est : ",SubString)
        ConstString = ConstString.union(SubString) 
        W[i] = ConstString  
    #print(W[(0,1)])
    print(len(W[(0,3)]))
    return 0 # retourne un dag

#generatestring  = GenerateStr({"v1": "425-706-7709"}, "706")
#print(generatestring)




