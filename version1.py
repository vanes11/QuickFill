from graphviz import *
from collections import *
from collections.abc import Iterable
import sys,codecs,locale
import csv
import re
import json




""" ++++++++++++++++++++++ Debut Zone de definition des constantes et variable global ++++++++++++++++ """

BOTTOM =  "⊥"
ClasseC = {}
MesNode = {} #distionnaire ayant pour cles une valeur et valeur un chemins allant de la source a la destination
valit = 0 #permet de varie la cles de chemin

""" ++++++++++++++++++++++ Fin Zone de definition des constantes et variable global ++++++++++++++++ """



""" ***************** Debut Zone d'écriture des fonctions******************** """
#Fonction permetant de determiner tous les chemin allant de la source a la destination 

# This class represents a directed graph
# using adjacency list representation
class Graph:

    def __init__(self, vertices):
        # No. of vertices
        self.V = vertices
        # default dictionary to store graph
        self.graph = defaultdict(list)
        

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''
    def printAllPathsUtil(self, u, d, visited, path):

        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)

        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            
            global MesNode
            global valit
            valtest = []
            for elt in path:
                valtest.append(elt)
            
            MesNode[valit] = valtest
            valit = valit + 1 
                
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.graph[u]:
                if visited[i]== False:
                    self.printAllPathsUtil(i, d, visited, path)
                    
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False


    # Prints all paths from 's' to 'd'
    def printAllPaths(self, s, d):

        # Mark all the vertices as not visited
        visited =[False]*(self.V)

        # Create an array to store paths
        path = []

        # Call the recursive helper function to print all paths
        self.printAllPathsUtil(s, d, visited, path)
        

#convert list of iterable in a signe  list

def flatten(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x
            

#Etape 0) Fonction de recuperation  des exemples

def GetExamples():

    S =[]
    s = set()
    sigma = {}
    d = {}
    sortie = ""
    decoupe = []

    with open("data.txt","r", newline=None) as f:
        for line in f:
            line = line.replace("\n", "")
            decoupe = line.split("---")
            if len(decoupe)==1:
                if decoupe[0]=="***":
                    S.append(s)
                    s = set()
            else:
                example =  decoupe[0]
                sortie  =  decoupe[1]
                example =  example.split("+++")
                for i in range(len(example)):
                    sigma["v"+str(i+1)]  = example[i]

                x = (json.dumps(sigma),sortie) 
                s = s.union(set([x]))
                sigma = {}
    
    S.append(s)

    return S

########################################Fin Etape 0#################################################


#Etape 1) Fonction de creaion de la classe  C de Tokens utiliser dans les primitives de notre langage

def GetClassC():
    """
     Defintion de la classe de token C,
    Il s'agit d'un dico dont les cles st les noms de tokens et
    les valeurs st les expressions regulieres correspondantes 
     """ # a present on a 23 tokens dans ClassC
    ClasseC ={}

    with open('classeC.csv', mode='r') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=';')
        for token in csv_reader:
            ClasseC[token[0]] = token[1]
        ClasseC['SemiColonTok'] = ";"
    return ClasseC

########################################Fin Etape 1#################################################


#Etape 2) Definition des primitives de permetant implementation de GeneratePostion

def Cpos(s,k):
    """ CPos est un constructeur de position, il permet de representer une  position de la gauche vers la droite et de la droite vers la droite """
    if(k>= 0):
        return k
    else:
        return len(s) + k


def TokenSeq(*tokens):
    """ contruit une sequence(concatenation)d'expression regulieres """
    TokenSeqResult = ""
    for token in tokens:
        TokenSeqResult = TokenSeqResult+token
    return TokenSeqResult


def Pos(s,r1,r2,c):
    """ 
        Retourne l'indice de debut de r2 dans  le cieme matching de l'expression reguliere 
        TokenSeq(r1,r2)
    """
    r = TokenSeq(r1, r2) ; r = re.compile(r)
    r1 = re.compile(r1) ; r2 = re.compile(r2)
    RegularExpression = r.findall(s) # retourne la liste des chaines qui match l'expression reguliere r dans s
    
    if len(RegularExpression) >= abs(c):
        e = abs(c)-1 # -1 car on veut recuperer le cieme element dans RegulaExpression dont l'element d'indice c-1 car le comptage commence a -1
        if c > 0:
            res = re.search(re.escape(RegularExpression[e]),s)
            t1 = res.group()
            res1 = re.search(r1,t1) # on recupere  l'occurrence de r1 dans res
            Taille = res1.end() - res1.start()  # taille de res1
            t = res.start() + Taille       
                
        else:
            e = len(RegularExpression) + c  # comme c est negatif, on applique son cpos et on applique le meme principe precedent
            res = re.search(re.escape(RegularExpression[e]),s)
            t1 = res.group()
            res1 = re.search(r1,t1) # on recupere l'occurrence de r1 dans rest1
            Taille = res1.end() - res1.start()  # on recupere la taille
            t = res.start() + Taille
        return t
    else:
        return BOTTOM


def GenerateRegularExpressionLeft(s,k):
    """ 
    Retourne l'ensemble des expressions regulieres qui existent dans  s[k1:k] 
    pour k1 variant de 0 a k-1
    """
    k1 = 0 #on commence la recherche en debut de chaine
    r1 = []
    Tokens = [] # liste des tokens dans la sous chaine s[k1:k]
    while  k1 <= k-1 :
        for cle in ClasseC:
            Token = ClasseC[cle]
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s[k1:k])
            
            if Test != None:
                k1 = k1 + Test.start()
                Tokens.append((k1,Token,cle))# 0n stoke  le tuplet contenant l'indice de k1 du token en k1, la valeur du token associe et la cle(nom du token correspondant)
                k1 =  k1 + Test.end()
              
                break
    Taille = len(Tokens)
    i = 0
    while  i < Taille : # on construit les tokens correspondant a la sous chaine s[k1:k]
        Expression = "".join([str(elt[1]) for elt in Tokens[i: Taille]]) # ecriture de valeurs de tokens
        Expression2 = ",".join([str(elt[2]) for elt in Tokens[i: Taille]])# ecriture sur forme de cle separe par les virgules: Numtok, Hyphentok...
        r1.append((Tokens[i][0],Expression,Tokens[i: Taille],Expression2))
        # r1 est un liste de quatuplet(a,b,c,d): a represente k1, b l'expression reguliere associe, c la sous liste de Tokens correspondant.et d les tokens correspondant
        i = i +1
    return r1   


def GenerateRegularExpressionRigth(s,k):
    
    """ Retourne l'ensemble des expressions regulieres qui existent dans  s[k:k2] 
    pour k2 variant de k a len(s) """ # meme principe que precedement
   
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
                k1 = k1 + 1  #on avance pour continuer le parcours
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


def MatchExpression(l,s):
    """ 
    etant donnee une liste  l, cette fonction retourne l'indice(l'occurence) de s  dans l s'il trouve
    """
    try:
        return l.index(s) + 1 # +1 parceque l'indxation dans les liste commence a 0

    except ValueError:
        return 0

def GetBestKey(s):
    """ prend une chaine(nondigitToc) et retoune le type(cle) de l'expression reguliere correspondante. """
    k1 = "NonAlphtok"
    k2 = "NonspaceTok"
   
    keylist = list(ClasseC.keys())
    k1 = keylist.index(k1)
    k2 = keylist.index(k2)


  
    for i in range((k1+1),k2):
        Token = ClasseC[keylist[i]]
        
        TokenComp = re.compile(Token)
        Test = TokenComp.match(s)
        if Test != None:
            return keylist[i]
    
    return ''
    

def ExpressionConcatenate(entree, s):
    """ retourne la formule concatenate(de SubStr2) et concatenate(de ConstStr) qui permet d'obtenir s a partir de entree """
    k1 = 0
    r1 = []
    Tokens = []
    ExpressionExecute = []
    ExpressionExecuteFormule = []
    P1 = []
    P2 = []

    k=len(s)
    booleen = False

    while  k1 <= k-1 :
        for cle in ClasseC:
            Token = ClasseC[cle]
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s[k1:k])
            
            if Test != None:
                k1 = k1 + Test.start()
                if cle == 'NonDigitTok' :
                    bestkey = GetBestKey(Test.group())
                    if bestkey != '':
                        cle = bestkey
                        Token = ClasseC[cle]
                
                Tokens.append((k1,Token,cle,Test.group()))
                k1 =  k1 + Test.end()
              
                break


    for elt in Tokens:
        booleen = False
        for key in entree:
            elt = list(elt)
            chaine = elt[3]
            expression = elt[1]
            Tokenname = elt[2]
            TokenComp = re.compile(expression)
            Test = TokenComp.findall(entree[key])

            for p in range(len(Test)):

                K = len(chaine)
                res = [Test[p][i: j] for i in range(len(Test[p])) for j in range(i + 1, len(Test[p]) + 1) if len(Test[p][i:j]) == K]

                if chaine in res:

                    if len(chaine) == len(Test[p]): 
                        result = (p,-2)
                        booleen = booleen or True
                    else:
                        if res[0] == chaine:
                            result = (p,0,len(chaine))
                            booleen = booleen or True
                        elif res[-1] == chaine:
                            result = (p,-1,len(chaine))
                            booleen = booleen or True
                        else:
                            booleen = booleen or False

                    break
            

            if booleen:
                break
            else:
                booleen = booleen or False
        
        if booleen:
            ExpressionExecute.append((key,expression,result))
            ExpressionExecuteFormule.append("SubStr2(" + key + "," + Tokenname + "," + str(list(result)[0]+1) + ")")
        else:
            ExpressionExecute.append(chaine)
            ExpressionExecuteFormule.append("ConstStr(" + chaine + ")")
       
    
   
    P1.append(ExpressionExecute)
    P2.append(ExpressionExecuteFormule)




   
    return [P1,P2]



def ExpressionConcatenateOfString(s):
    """ retourne l'expression reguliere qui match une sortie s, s etant une chaine de caractere """
    k1 = 0
    r1 = []
    Tokens = []
    ExpressionExecuteFormule = ""
    k=len(s)
   

    while  k1 <= k-1 :
        for cle in ClasseC:
            Token = ClasseC[cle]
            TokenComp = re.compile(Token)
            Test = TokenComp.match(s[k1:k])
            
            if Test != None:
                k1 = k1 + Test.start()
                
                if cle == 'NonDigitTok' :
                    bestkey = GetBestKey(Test.group())
                    if bestkey != '':
                        cle = bestkey
                        Token = ClasseC[cle]
                
                Tokens.append((k1,Token,cle,Test.group()))
                k1 =  k1 + Test.end()
              
                break

    

    for elt in Tokens:
        ExpressionExecuteFormule = ExpressionExecuteFormule + " " + list(elt)[2]
        
    
    
    return ExpressionExecuteFormule


def ExpressionConcatenateOfStringSigma(entre):
    """ retourne l'expression reguliere qui match l'entree sigma, sigma etant un dic de chaine de caractere"""
    DiskExpression= {}

    for key in entre:
        s = entre[key]
        k1 = 0
        r1 = []
        Tokens = []
        ExpressionExecuteFormule = ""
        k=len(s)
    

        while  k1 <= k-1 :
            for cle in ClasseC:
                Token = ClasseC[cle]
                TokenComp = re.compile(Token)
                Test = TokenComp.match(s[k1:k])
                
                if Test != None:
                    k1 = k1 + Test.start()
                    if cle == 'NonDigitTok' :
                        bestkey = GetBestKey(Test.group())
                        if bestkey != '':
                            cle = bestkey
                            Token = ClasseC[cle]
                    
                    Tokens.append((k1,Token,cle,Test.group()))
                    k1 =  k1 + Test.end()
                
                    break

        

        for elt in Tokens:
            ExpressionExecuteFormule = ExpressionExecuteFormule + " " + list(elt)[2]

        DiskExpression[key] = ExpressionExecuteFormule
        
    
    
    return DiskExpression



def ExpressionConstString(entree, s):
    """ retourne la formule concatenate de constString qui permet d'obtrenir s a partir de entree """
    exp = []
    for key in entree:
        if entree[key] in s:
            s = s.replace(entree[key],key)

    Expression2 = "|".join(entree.keys())
    Expression2 = "(" + Expression2 + ")"
    disssos = re.split(Expression2,s)

    for elt in disssos:
        if elt != '':
            if elt in entree.keys():
                exp.append(elt)
            else:
                exp.append("ConstStr(" + elt +  ")")
             
    
    
    return exp
   
    

########################################Fin Etape 2#################################################

#Etape 3) implementation de GeneratePostion

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
    R1List = GenerateRegularExpressionLeft(s,k)  #  liste des expressions regulieres dans la chaine s[0:k-1]
    R2List = GenerateRegularExpressionRigth(s,k) # Liste des expressions regulieres dans la chaine s[k:len(s)]
    for r1 in R1List :
        for r2 in R2List :
            r12 = TokenSeq(r1[1],r2[1])
            r12 = re.compile(r12)
            MatchingList = r12.findall(s)# liste de toutes les occurrences de qui match r12 dans s
            c = MatchExpression(MatchingList,s[r1[0]:r2[0]+1])
            c1 = len(MatchingList)
            if c!=0 and (r1[2][len(r1[2])-1][1] != r2[2][0][1]): 
                # cette deuxieme condition sur if nous permet d'exclure le ou la fin de r1 est  de meme type que le debut de r2, car ceci pret a confusion, on ne sait plus dean ce cas determiner l;indice de debut de r2
                c1 = -(c1 -c +1)   # c1 nous permet de parcourir la chaine de la droite vers la gauche
                PosChain = "Pos("+"TokenSeq("+r1[3]+"),TokenSeq("+r2[3]+"),"+str(c)+")"
                POsList.append(PosChain) 
                PosChain = "Pos("+"TokenSeq("+r1[3]+"),TokenSeq("+r2[3]+"),"+str(c1)+")"
                POsList.append(PosChain)

                result = result.union(set([Pos(s,r1[1],r2[1],c),Pos(s,r1[1],r2[1],c1)]))  # result n'est rien d'autres que que k

    return result,set(POsList)
         
########################################Fin Etape 3#################################################

#Etape 4) Definition des primitives de permetant implementation de GenerateStr 


def SubStr(s,p1,p2):
    """ 
    Expression de sous chaine tel que formuler dans l'article, un peu != de celle de python.l'indexation commence a 0
    """
    # par la suite on utile la fonction substring de python a ajoutant a l'indice de fin
    p2 = p2+1
    return s[p1:p2]


def SubStrs(s,p1,p2):
    """
    Retourne la liste de sous chaine de s pouvant etre former avec les elements de p1 et p2: p1 et p2 etant les ensembles de positions , 
    """
    SubList = []  # pour affichage
    SubChain = ""
    p1 = list(p1); p2 = list(p2)
    for i in p1:
        for j in  p2:
            #result = result.union(set([SubStr(s,i,j)])) # ce ci n'est pertinent que lorsque l'ensemble p1 tout comme p2
            # represente les valeurs diff, ce qui n'est pas le cas pour nous
            #SubChain = "SubStr("+s+","+str(i)+","+str(j)+")"
            SubChain = "SubStr("+s+","+i+","+j+")"# pour  le formatage, on laisse i et j pour avoir les expressions pos et cpos
            SubList.append(SubChain)
    
    return set(SubList)



########################################Fin Etape 4#################################################

#Etape 5) Implementation de GenerateSubstring, fonction principale de GenerateStr


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
            Y1 = GeneratePosition(entree[cle],k) # Y1 est un tuple car GeneratePosition retourne un tuple
            Y1 = Y1[1]  # ensemble de facons de retourner l'indince de debut de s sans entree
            Y1 = list(Y1)
            for i in range(len(Y1)):

                Y1[i] = Y1[i].replace(entree[cle],cle,10)


            Y2 = GeneratePosition(entree[cle], k1)
            Y2 = Y2[1]
            Y2 = list(Y2)
            for i in range(len(Y2)):
                Y2[i] = Y2[i].replace(entree[cle],cle,10)
                

            SubResult = SubStrs(cle,Y1,Y2) # le resultat de Substrs est deja un set            
            result = result.union(SubResult) 
                  
            
    return result


    
    
def  GenerateStr(entree, s):
    """ 
    cette fonction retourne  l'ensemble des facons d'obtenir s a partir de l'etat d'entree sigma
    elle retourne un dag, une structure de donnee qui permet de representer des grands ensembles
    elle utilse le principe de l'algorithme CYK, base sur la programmation dynamique, qui consiste a reconnaitre un mot
    dans un langage en passant  par sa table de transition.
    """
    EtaTilda = set() ; PsiTilda = set() 
    """ EtaSource = 0
    EtaTarget = len(s) """  
    W = {}    # table de transition, pour chaque arrete (i,j) associe l'etique qui est un ensemble d'expressions at0mique

    for i in range(len(s)+1):      
        EtaTilda = EtaTilda.union(set([i]))  # construction de l'ensemble des noeuds

    for i in range(len(s)+1):
        k = i+1
        for j in range(k,len(s)+1):
            PsiTilda = PsiTilda.union(set([(i,j)]))   # ensemble des aretes
            #PsiTilda = list(PsiTilda)
    
    for i in PsiTilda:                                # Pour chaque arete
        x = "ConstStr("+s[i[0]:i[1]]+")"                # s[i:j] =  SubStr(i,j), c'est pourquoi je concerve i[1] au lieu de i[1]-1
        ConstString = set([x])
        SubString = GenerateSubstring(entree,s[i[0]:i[1]])
        ConstString = ConstString.union(SubString) 
        
        W[i] = ConstString  
    
    baseformule = ExpressionConcatenate(entree , s)
    baseformule = baseformule[-1][0]
    
    if baseformule != [] :
        baseformule = "Concatenate (" + ",".join(baseformule) + " )"
        W[(0,len(s))] =  W[(0,len(s))].union(set([baseformule]))
    
    EtaTilda = list(EtaTilda)
    return W , EtaTilda



def PrintDag(Listenoeud , generatestring ,entree, s):
    """ 
    prend une chaine s et son resultat GenerateStr associe i.e la table de transition et la liste des noeuds et affiche le dag correspondant
    """
    sys.stdout.reconfigure(encoding='utf-8')
    dot = Digraph(name='GenerateStr',comment='Test')


    for elt in list(Listenoeud):
        if elt == list(Listenoeud)[0]:
            dot.node(str(elt) , str(elt),color="Red")
        elif elt == list(Listenoeud)[-1]:
            dot.node( str(elt) ,str(elt) ,shape="doublecircle")
        else:
            dot.node(str(elt) , str(elt))
    if len(list(Listenoeud)) != 0:       
        for cle in generatestring:
            r = "Const" ; r = re.compile(r)       
            target =list(generatestring[cle])
           
            val1 = target[0]
            label1="{"+val1 +"}"
            dot.edge(str(cle[0]) , str(cle[1]) , label=label1)

        
    dot.attr(label= "entree_sigma = " + str(entree)  +",s = "+s)
    dot.attr(fontsize='25')
    dot.format = 'png'
    dot.render()




########################################Fin Etape 5#################################################

#Etape 6) Definition des primitives de permetant implementation de IntersectDag 

def SizeNoeud(n,W):
    size = 0
    if n ==0 :
        return 1   
    else:
        for i in range(n):
            if (i,n) in W.keys():
                size = size + SizeNoeud(i,W)*(len(W[(i,n)])) # +1 parceque on ajoute l'expression atomique ConstStr dans la construction de w                                                                                                                                                                                                                                                                                                                          

    return size



def SizeDag(EtaTarget, W):
    """ 
    Permet de retourner le nombre d'element d'un ensemble d'expression: 
    c'est la taille des Dags  qui nous interesse particulierement.
    """
    if W != {} :
        return SizeNoeud(EtaTarget,W)
    else:
        return 0



def IntersectConstStr(s1,s2):
    if s1 == s2 : # s1 et s2 sont sur la forme ConstStr(s1),....
        return s1
    else:
        return BOTTOM



def IntersectRegex(t1,t2):
    """ 
    Prend en entree deux expression regulieres (sur la forme TokenSeq) et le retoune leur intersection
    """
    t1 =  t1.split(",")
    t2 = t2.split(",")
    t1[0] = t1[0].replace("TokenSeq(","")
    t1[-1] = t1[-1].replace(")","")
    t2[0] = t2[0].replace("TokenSeq(","")
    t2[-1] = t2[-1].replace(")","")
    t3 = [] # TokenSeq resultat des tokenseq t1 et t2 
    
    if len(t1) != len(t2):
        return BOTTOM

    else:
        for i in range(len(t1)):
            if t1[i] == t2[i]:
                t3.append(t1[i])


        if len(t3) == 0:
            return BOTTOM

        else:
            Expression = ",".join(t3)
            Expression = "TokenSeq("+Expression+")"
            return Expression






def IntersectPos(p1,p2):
    """ 
    P1 et p2 sont des ensemble d'elements de type Pos(r1,r2,c)
    """
    if p1.startswith("Cpos") and p2.startswith("Cpos"):
        return IntersectCpos(p1,p2)
    

    elif p1.startswith("Pos") and p2.startswith("Pos"):
        
        
        p1 = p1.split("Pos(",1)
        p2 = p2.split("Pos(",1)
        p11=[]
        p22=[]
        

        if p1[1].rfind('TokenSeq') >=0:
            l = p1[1].rfind('TokenSeq')-1
            p11.append(p1[1][0:l])
            k = p1[1][l+1:len(p1[1])]
            n = k.index(')')
            p11.append(k[0:n+1])
            p11.append(k[n+2:len(k)-1])
    

        if p2[1].rfind('TokenSeq') >=0:
            l = p2[1].rfind('TokenSeq')-1
            p22.append(p2[1][0:l])
            k=p2[1][l+1:len(p2[1])]
            n = k.index(')')
            p22.append(k[0:n+1])
            p22.append(k[n+2:len(k)-1])
  
            
        
        
        if p11[2] != p22[2]:  # p1[2] et p2[2] represente c et c'. si c!= c' alors c inter c' = {} et l'intersection de pos devient impossible
            return BOTTOM
            
        x = IntersectRegex(p11[0],p22[0]) # p1[0] et p2[0] representent les expressions regulieres r1 et r1'
        y = IntersectRegex(p11[1],p22[1])
    

        if x != BOTTOM and y != BOTTOM :
            Expression = "Pos("+x+","+y+","+p11[2]+")"
            return Expression

        else:
            return BOTTOM

    else:
         return BOTTOM
   


def IntersectCpos(s1,s2):
    # le resultat est sur la forme Cpos(s1) , s1 et s2 sont sur cette meme forme
    if s1 == s2:
        return s1
    else:
        return BOTTOM



def IntersectSubstr(s1,s2):
    """
    Intersection de 2 sous expressions subStr() 
    """
    s11=[]
    s22=[]
    s1 = s1.split(",",1)
    s2 = s2.split(",",1)
    
    if s1[1].rfind('Cpos') >=0:
        if  s1[1].rfind('Cpos') == 0:
            l = s1[1].rfind('Pos')-1
            s11.append(s1[1][0:l])
            s11.append(s1[1][l+1:len(s1[1])-1])
        else:
            l = s1[1].rfind('Cpos')-1
            s11.append(s1[1][0:l])
            s11.append(s1[1][l+1:len(s1[1])-1])
    else:
            l = s1[1].rfind('Pos')-1
            s11.append(s1[1][0:l])
            s11.append(s1[1][l+1:len(s1[1])-1])


    if s2[1].rfind('Cpos') >=0:
        if  s2[1].rfind('Cpos') == 0:
            l = s2[1].rfind('Pos')-1
            s22.append(s2[1][0:l])
            s22.append(s2[1][l+1:len(s2[1])-1])
        else:
            l = s2[1].rfind('Cpos')-1
            s22.append(s2[1][0:l])
            s22.append(s2[1][l+1:len(s2[1])-1])
    else:
            l = s2[1].rfind('Pos')-1
            s22.append(s2[1][0:l])
            s22.append(s2[1][l+1:len(s2[1])-1])


    s1[0] = s1[0].replace("SubStr(","")
    s2[0] = s2[0].replace("SubStr(","")
    


    x = IntersectPos(s11[0],s22[0])
    y = IntersectPos(s11[1],s22[1])

    if x != BOTTOM and y != BOTTOM:
        Expression = "SubStr("+s1[0]+","+x+","+y+")"
        return Expression

    else: 
        return BOTTOM





def Intersect(f1,f2):
    """ 
    f1 et f2 sont les ensembles d'expressions atomiques.
    """
    result = set()
    """ cpos1 = []
    cpos2 = [] # liste des expressions atomiques contenant Cpos() dans f1     f1 = list(f1) """
    f1 = list(f1)
    f2 = list(f2)
    s1 = ""
    s2 = ""
    
    
    indice1  = [i for i in range(len(f1)) if f1[i].startswith('Const')]
    indice2  = [i for i in range(len(f2)) if f2[i].startswith('Const')]


    
    if indice1!=[] and indice2!=[] :
        
        s1 = f1[indice1[0]] #pn extrait le cas particulier des constantes.
        s2 = f2[indice2[0]]
        f1.remove(s1)
        f2.remove(s2)

    if IntersectConstStr(s1, s2) != BOTTOM: # cas des constrs
        result = result.union(set([s1]))

    # cas des expressions Substr avec  Pos 
    for elt1 in f1:
        for elt2 in f2:
            if elt1.startswith('SubStr') and elt2.startswith('SubStr'):
                x = IntersectSubstr(elt1,elt2)  # elt1 et elt2 st sur la forme SubStr(vi,pos(....),Pos(,,,))
                if x != BOTTOM: # ce x est de la forme IntersetPos
                    result = result.union(set([x]))

    return result


def RenomageDag(EtaTilda, W12):
    Renomage = {}
    EtaTildaNew = []
    W12New = {}
    for i in range(len(EtaTilda)):
        Renomage[EtaTilda[i]] = i
        EtaTildaNew.append(i)
    
    for key in W12:
        W12New[(Renomage[key[0]], Renomage[key[1]])] = W12[key]
        
    return EtaTildaNew , W12New
    



########################################Fin Etape 6#################################################





#Etape 7) Implementation de IntersectDag

def IntersectDag(EtaTilda1,W1,EtaTilda2,W2):
    """ 
    Cette fonction prend en entree deux graphes et retourne leur intersection
    """
    
    

    # si on admet les expressions loops, il va falloir faire la fonction IntersectLoop pour gerer ce cas
    EtaTilda1 = list(EtaTilda1)
    EtaTilda2 = list(EtaTilda2) 
    EtaTilda = []
    EtaTildaCopy = []
    PsiTilda = []
    PsiTildaCopy = []
   
    W12 = {}  # table de transition du graphe resultat
    
    if len(EtaTilda1) == len(EtaTilda2):
        
        #print("++++++++++++++++++++++++++1" ,EtaTilda1,"\n" )
        #print("++++++++++++++++++++++++++2" ,EtaTilda2 , "\n")
        
        if (0,len(EtaTilda1)-1) in W1.keys() and (0,len(EtaTilda2)-1) in W2.keys():
            baseformule1 = list(W1[(0,len(EtaTilda1)-1)])
            baseformule2 = list(W2[(0,len(EtaTilda2)-1)])
            indice1  = [i for i in range(len(baseformule1)) if baseformule1[i].startswith('Concatenate')]
            indice2  = [i for i in range(len(baseformule2)) if baseformule2[i].startswith('Concatenate')]

            if indice1!=[] and indice2!=[] :
                
                elt = baseformule1[indice1[0]]
                elt2 = baseformule2[indice2[0]]
                
                if elt == elt2:
                    
                    W12[((0,0),(len(EtaTilda1)-1,len(EtaTilda2)-1))] = set([elt]) 
                    W1[(0,len(EtaTilda1)-1)] = list(W1[(0,len(EtaTilda1)-1)])
                    W1[(0,len(EtaTilda1)-1)].remove(elt)
                    W1[(0,len(EtaTilda1)-1)] = set(W1[(0,len(EtaTilda1)-1)])
                    W2[(0,len(EtaTilda2)-1)] = list(W2[(0,len(EtaTilda2)-1)])
                    W2[(0,len(EtaTilda2)-1)].remove(elt2)
                    W2[(0,len(EtaTilda2)-1)] = set(W2[(0,len(EtaTilda2)-1)])
                
            
        
        # construction de l'ensemble de noeuds  cadidats du graphe resultat
        
       
        for i in EtaTilda1:
            for j in EtaTilda2:
                if j==i:
                    EtaTilda.append((i,j))
                    EtaTildaCopy.append((i,j))
           

        # construction de l'ensemble des aretes candidats
        for i in range(len(EtaTilda)):
            elt = EtaTilda[i]
            k = i+1
            for j in range(k,len(EtaTilda)):
                elt2 = EtaTilda[j]
                PsiTilda.append((elt,elt2))
                PsiTildaCopy.append((elt,elt2))


        VarieCase = 0
        # calculons les intersection pour elements surprimer les transistions non importants et obtenir le graphe resultat.
        for elt in PsiTilda:
            # Intersect prend  en entre 2 ensembles d'expression atomiques correspondant aux etiquettes des arretes entre 2 noeuds pris dans les 2 Dags
            if (elt[0][0],elt[1][0]) in W1.keys() and (elt[0][1],elt[1][1]) in W2.keys():
                x = Intersect(W1[(elt[0][0],elt[1][0])],W2[(elt[0][1],elt[1][1])])
            else:
                x = set()
            
            
            if x == set() or x == set(['']):
                PsiTildaCopy.remove(elt)
                
            else:
               
                if  elt in W12.keys():
                    W12[elt] = W12[elt].union(x) 
                else:
                    W12[elt] = x

                
            
            if EtaTilda[VarieCase] != elt[0]:

                DoitSupp = True
                
                for key in W12:
                    if EtaTilda[VarieCase] == key[0]:
                        if W12[key] != set():
                            DoitSupp = False
                            break
                            
                                    
                if DoitSupp:
                    EtaTildaCopy.remove(EtaTilda[VarieCase])

                VarieCase = VarieCase + 1
        
        
        
        DoitPasSupp = ((EtaTilda[VarieCase], EtaTilda[len(EtaTilda)-1]) in  W12.keys()) and (W12[(EtaTilda[VarieCase], EtaTilda[len(EtaTilda)-1])]!= set())
        DoitSupp = not(DoitPasSupp)
        
        if DoitSupp :
              EtaTildaCopy.remove(EtaTilda[VarieCase])

    
                    
                
    else:
        if (0,len(EtaTilda1)-1) in W1.keys() and (0,len(EtaTilda2)-1) in W2.keys():
            baseformule1 = list(W1[(0,len(EtaTilda1)-1)])
            baseformule2 = list(W2[(0,len(EtaTilda2)-1)])
            indice1  = [i for i in range(len(baseformule1)) if baseformule1[i].startswith('Concatenate')]
            indice2  = [i for i in range(len(baseformule2)) if baseformule2[i].startswith('Concatenate')]
            
            
            

            if indice1!=[] and indice2!=[] :
                
                elt = baseformule1[indice1[0]]
                elt2 = baseformule2[indice2[0]]
                if elt == elt2:
                    W12[((0,0),(len(EtaTilda1)-1,len(EtaTilda2)-1))] = set([elt])
                    EtaTilda.append((0,0))
                    EtaTilda.append((len(EtaTilda1)-1,len(EtaTilda2)-1))
            
    
    
    

    if len(EtaTildaCopy)  == len(EtaTilda) and EtaTilda != []:
            
            EtaTilda, W12 = RenomageDag(EtaTildaCopy,W12)
            g = Graph(len(EtaTilda))
            for elt in list(W12.keys()):
                g.addEdge(elt[0], elt[1])
            
            s = EtaTilda[0]
            d = EtaTilda[-1]
            global MesNode
            global valit
            MesNode = {}
            valit = 0
            g.printAllPaths(s, d)
            WK = {}
            for elt in MesNode:
                for i in range(len(MesNode[elt])-1):
                    if (MesNode[elt][i],MesNode[elt][i+1]) not in WK.keys():
                        WK[(MesNode[elt][i],MesNode[elt][i+1])] = W12[(MesNode[elt][i],MesNode[elt][i+1])]
            return  WK , EtaTilda
    else:
        if  EtaTilda != [] :
            VerifCas2 = ((EtaTilda[0], EtaTilda[len(EtaTilda)-1]) in  W12.keys()) and (W12[(EtaTilda[0], EtaTilda[len(EtaTilda)-1])]!= set()) and (W12[(EtaTilda[0], EtaTilda[len(EtaTilda)-1])]!= set(['']))
            if VerifCas2:
                EtaTildaNew = [0,1]
                W12New={}
                W12New[(0,1)] = W12[(EtaTilda[0], EtaTilda[len(EtaTilda)-1])]
                return  W12New , EtaTildaNew
            else:
                return {},[]
        else:
            return {},[]


########################################Fin Etape 7#################################################

#Etape 8) Definition des primitives de permetant implementation de  GeneratePartition

def Comp(EtaTilda1,W1,EtaTilda2,W2): 
    """
    prende en entree deux dags(trace expression) caracteriser chacun par son ensemble  de noeud et sa table transistion
    e dit si oui ou non ces deux sont compabtibles ou pas 
    """
    if W1!={} and W2!={}:
        
        x,y = IntersectDag(EtaTilda1,W1,EtaTilda2,W2)
        if x != {}:
            return True
        else:
            return False
    else:
       
        return False



def z(EtaTilda1,w1, EtaTilda2,w2,EtaTilda3,w3):
    """
    Teste la compatibilite de ensembles de trace expressions couples avec un troisime ensemble 
    """
    if w1!={} and w2!={}:
        
        w12 , EtaTilda12 = IntersectDag(EtaTilda1,w1,EtaTilda2,w2)
        
        if (Comp(EtaTilda1,w1,EtaTilda3,w3) ==  Comp(EtaTilda2,w2,EtaTilda3,w3) and (Comp(EtaTilda12, w12 ,EtaTilda3,w3))==True) :
            return 1
        else:
            return 0
    
    else:
        return 0


def CS1(EtaTilda1,w1, EtaTilda2,w2,p1,p2,T):
    """ 
    permet de mesurer la concordance de partition en ce qui concerne concerne la compatibilite de leurs ensmbles
    de traces et leur intersection avec les autres ensembles de traces.
    On prendra p1 et p2 lors du parcours dans GeneratePartition pour trouver la paire de grand score de compatibilite
    T est une liste de tuples; l'elementt gauche de chahque tuple est aussi un tuple
    """
    # T = {({sigma1},(w1,EtaTilda))}
    cs1 = 0 # variable resultat
    for i in range(len(T)):
        if i != p1 and i != p2:
            cs1 = cs1 + z(EtaTilda1,w1, EtaTilda2,w2,T[i][1][1],T[i][1][0])

    return cs1



def CS2(EtaTilda1,w1, EtaTilda2,w2):
    """ 
    """
    if w1!={} and w2!={}:
        
        w12,EtaTilda12 = IntersectDag(EtaTilda1,w1, EtaTilda2,w2)
        if w12 != {}:
            x = SizeDag (EtaTilda12[-1],w12) #numerateur           
            size1 = SizeDag(EtaTilda1[-1],w1)
            size2 = SizeDag(EtaTilda2[-1],w2)
            result = x/max(size1,size2)

            return  result
        else:
            return 0
    
    else:
        
        return 0

def CS(EtaTilda1,w1, EtaTilda2,w2,p1,p2,T):
    """ Calcul du score de compatibilite. p1 et p2 representent les positiion du Dag1 et Dag2 dans T respectivement """
    # T est le resultat de GenerateStr converti en liste
    cs1 = CS1(EtaTilda1,w1, EtaTilda2,w2,p1,p2,T)
    cs2 =  CS2(EtaTilda1,w1, EtaTilda2,w2)

    return ((cs1,cs2),(p1,p2)) # les indices p1 et p2 vont nous permettre de recuperer  les entree(sigma correspondant)



def ComparaisonCS(CSa, CSb):
    """ compare deux scores de compatibilites Csa et CSb avec les entree correspondantes;
    C'est un CSa est un tuple de tuples ((cs1,cs2),(p1 p2)) , p1 et p2 representant les indice de Dag1,
    Dag2 dans le tableau T resultat de GenerateStr.
    """

    if (CSa[0][0] > CSb[0][0]) or (CSa[0][0]== CSb[0][0] and CSa[0][1] > CSb[0][1]):
        return CSa

    else:
        return CSb # tuple de tuples de forme: ((cs1,cs2),(p1 p2)):p1 indice du prmier elemnt dans T et p2 ..


def TestCompatibilite(T):
    """
    Teste s'il exite dans un ensembles de couples deux couple compatible 
    """
    for i in range(len(T)):
        for j in range(i+1,len(T)):
            if Comp(T[i][1][1],T[i][1][0],T[j][1][1],T[j][1][0]):
                return True

    return False


def LargestCS(T):
    """ retourne les deux couples qui ont le plus grand score de compatibilite sur ensemble de trace  """
    ScoreList = []
    for i in range(len(T)):
        for j in range(i+1,len(T)):
            score = CS(T[i][1][1],T[i][1][0],T[j][1][1],T[j][1][0],i,j,T)
            ScoreList.append(score)

    ScoreMax = ScoreList[0] # initialisation du score max

    for  i in range(1,len(ScoreList)):
        ScoreMax = ComparaisonCS(ScoreMax,ScoreList[i])

    return ScoreMax # est un tuble de tuple tout comme un element resultat de la fonction CS()


def TestCompatibiliteNew(T):
    """ verifie  s'il exite encore des couple compabtibles, son but est le meme que TestCompatibilite precedent """
    e1 = '' 
    e2 = ''
    f = ''
    booleen = False

    for i in range(len(T)):
        for j in range(i+1,len(T)):
            
            listeformule1 = list(T[i][1])
            listeformule2 = list(T[j][1])


            valtest1 = list(set(listeformule1[1][0]).intersection(set(listeformule2[1][0])))
            valtest2 = list(set(listeformule1[1][1]).intersection(set(listeformule2[1][1])))


            if len(listeformule1[1][0]) == len(listeformule2[1][0]) and len(listeformule1[1][0]) == len(valtest1):
                f = (listeformule1[0][0],listeformule1[1][0])
                e1 = i
                e2 = j
                booleen = True
                return booleen,e1,e2,f

            elif len(listeformule1[1][1]) == len(listeformule2[1][1]) and len(listeformule1[1][1]) == len(valtest2):
                f = (listeformule1[0][1],listeformule1[1][1])
                e1 = i
                e2 = j
                booleen = True
                return booleen,e1,e2,f




    return booleen,e1,e2,f



def ConvertListOfDickToString(L):
    newList = []
    for elt in L:
        newList.append(json.dumps(elt))
    
    exp =  ",".join(newList)

    return exp


########################################Fin Etape 8#################################################



#Etape 9) Implementation de GeneratePartition

def GeneratePartition(T):

    """ Permet partitionner l'ensemble d'entrees en des ensembles qui  demandent les memes traitements
    i.e qui vont satisfaire la meme formule boolenne. Le but etant  de dimunuer les coups computationnel.
    T est le resultat de  GenerateStr i.e un ens  de tuples; l'elementt gauche de chaque tuple est aussi un tuple
    """
    T = list(T)
    vtest = 1
    while TestCompatibilite(T):
            
        ScoreMax = LargestCS(T)
        FirstIndexe = ScoreMax[1][0]
        SecondIndexe = ScoreMax[1][1]
        
        partition = [T[FirstIndexe][0],T[SecondIndexe][0]]
        intersect =  IntersectDag(T[FirstIndexe][1][1],T[FirstIndexe][1][0],T[SecondIndexe][1][1],T[SecondIndexe][1][0])
        
        
        # enlevons les elts T[FirstIndexe] et T[SecondIndexe]
        T  = [item for item in T if item != T[FirstIndexe] and item != T[SecondIndexe]]
        # ajoutons la partion forme 
        T.append((partition,intersect))

        
        
    return T  # T est liste de tuple de tuples de la forme: (({ens des entree},(W du Dag correspondant, EtaTilda corespondant)))




########################################Fin Etape 9#################################################


#Etape 10) Definition des primitives de permetant implementation de GenerateBoolClassifier


def PredicatContruction(SigmaSet1, SigmaSet2):
    """ 
    Prend deux ensembles d'entree et contruit une liste qui contient  pour  chaque elt de l'union de ces deux ensembles
    le predicat qui match cet elt . ainsi que le complementaire de ce predicat.

    Mais nous ne retournons ici que la liste des predicats, leurs complementaires  seront geres lors du calcul de CSP
    """
    SigmaSet = SigmaSet1.union(SigmaSet2)
    Preds = []
    r = [] # pour la construction de l'expression reguliere pour une expression, on prefaire stocker le resultat sur forme de list
    
    for elt in SigmaSet:
        elt = json.loads(elt)
        r = []
        for key in elt:
            express = GenerateRegularExpressionLeft(elt[key],len(elt[key]))
            
            if express != []:
                r.append((express[0][1] , express[0][3]))
        

        Preds.append((elt , r))
      

    return Preds


def MachingPredicat(SigmaElement, Predicat):
    """ 
    Permet de savoir si le predicat Predicat satisfait l'etat d'entree SigmaElement
    Predicat est une liste d'expression regulieres , tel que la concatenation peut macth ou pas l'obje SigmaElement
    """
    i = 0
    SigmaElementConvert = json.loads(SigmaElement)
    PredicatElementConvert = Predicat[0]
    
   
    if len(SigmaElementConvert) == len(PredicatElementConvert):
        for elt in SigmaElementConvert:
            r1 = re.compile(Predicat[1][i][0]) # Predicat est une liste de meme taille que l'element  dictionnaire SigmaElement
            r2 = re.search(r1, SigmaElementConvert[elt])
            if r2 == None :
                return False
            
            i = i +1

        return True
    else:
        return False


def CSP(Predicat, SigmaSet1, SigmaSet2):
    """ 
    calcul le score declassification d'un predicat par rapport aux deux ebembls
    """
    csp1 = set() ; csp2 = set()
    # csp1 contient l'ensemb des elements de SigmaSet 1 qui sastifait predicat et csp2 contient les elements de Sigma2 qui ne stisfont pas predicat
    
    for elt in SigmaSet1 :
        if MachingPredicat(elt,Predicat):
            csp1 = csp1.union(elt)

    for elt in SigmaSet2 :
        if not(MachingPredicat(elt,Predicat)):
            csp2 = csp2.union(elt)


    csp = len(csp1) * len(csp2)
    NonCsp = len(SigmaSet1 - csp1) * len(SigmaSet2-csp2)

    return csp, NonCsp


def LargestCSP(Preds,SigmaSet1,SigmaSet2):
    """ 
    prend un liste de predicat et retoune le predicat de plus grand score de classification
    pour chaque predication contenu dans Preds, on calcul son score et celui de son complementaire
    """
    ScoreList = []
    for elt in Preds:
        csp , NonCsp = CSP(elt,SigmaSet1,SigmaSet2)
        ScoreList.append((elt,csp))# on garde le predicat et son complementaire
        newPredicate = [elt,'#'] # contruction du complementaire de elt: elt est un predicat dont une liste.
        ScoreList.append((newPredicate,NonCsp))

    # tri du tableau du score par ordre croissant du deuxieme element du tuple
    ScoreList.sort(key=lambda x:x[1])
    return ScoreList[-1][0]



def PresentInBoolClassier(entree, B):
    expr1 = ExpressionConcatenateOfStringSigma(entree)
    for elt in B:
        expr2 = B[elt][0][0]
        booleen = True
        if len(expr2.keys()) == len(expr1.keys()):
            for elt2 in expr2:
                if expr2[elt2] != expr1[elt2]:
                    booleen = False
                    break
        
        if booleen:
            return elt
    
    return ''






########################################Fin Etape 10#################################################

#Etape 11) Implementation de GenerateBoolClassifier

def GenerateBoolClassifier(SigmaSet1, SigmaSet2):

    """
    Genere les schemas booleens pour chaque partion generer precedement:
    Prend en entree deux ensembles d'entree s1,s2 et construit la condition booleenne 
    qui satisfait tous les elemnts de s1 mais pas pour s2
    """

    SigmaSet11 = SigmaSet1
    b =  [False]

    while SigmaSet11 != set():
        OldSigmaSet1 = SigmaSet11
        SigmaSet22 = SigmaSet2 
        SigmaSet111 = SigmaSet11 
        d = [True]

        while SigmaSet22 != set() :
            
            OldSigmaSet2 = SigmaSet22
            Preds =  PredicatContruction(SigmaSet111, SigmaSet22)
            # prenons dans Preds le predicat ayant le plus grand score de classification.
            
            LargestPredicat = LargestCSP(Preds,SigmaSet111, SigmaSet22)
            
            d.append(LargestPredicat) # on construit d
            
            SigmaSet111Rest = set()   # elements de SigmaSet111Rest  qui ne satisfont pas LargestPredicat
            SigmaSet2Rest = set() # elements de SigmaSet2Rest qui ne satisfont pas LargestPredicat
            
            if LargestPredicat[-1] =='#':
                for elt in SigmaSet111 :
                   
                    if MachingPredicat(elt,LargestPredicat[0:-1][0]):
                        SigmaSet111Rest  = SigmaSet111Rest .union(set([elt]))

                for elt in SigmaSet22 :
                   
                    if MachingPredicat(elt,LargestPredicat[0:-1][0]):
                        SigmaSet2Rest  = SigmaSet2Rest .union(set([elt]))


            else:

                for elt in SigmaSet111 :
                    if not(MachingPredicat(elt,LargestPredicat)):
                        SigmaSet111Rest  = SigmaSet111Rest .union(set([elt]))

                for elt in SigmaSet22 :
                    if not(MachingPredicat(elt,LargestPredicat)):
                        SigmaSet2Rest  = SigmaSet2Rest .union(set([elt]))

            SigmaSet111 = SigmaSet111 - SigmaSet111Rest
            SigmaSet22 = SigmaSet22 - SigmaSet2Rest
            
                        
            if OldSigmaSet2 == SigmaSet22:
                return 'FAIL'

        
        SigmaSet11 = SigmaSet11 - SigmaSet111
        b.append(d)
        

        if OldSigmaSet1 == SigmaSet11:
            return 'FAIL'

    return b




def MathStringexpression(Listformular):
    maformule = ""
    maformule = str(Listformular[0])
    maformule = maformule + " V " 
    
    if Listformular[-1] == "#":
         maformule =  maformule + "¬ ( "
         for i in range(1,(len(Listformular)-1)):
             if "v" in str(Listformular[i]):
                 maformule =  maformule + "Match( " +  Listformular[i] + "," + "TokenSeq("+ Listformular[i+2] +")," + "1)"
                 i = i + 2
             if i < (len(Listformular)-1):
                 maformule =  maformule + " ∧ "
         
         maformule =  maformule + " ) "
    else:
        maformule =  maformule + "( "
        for i in range(1,(len(Listformular)-1)):
            if type(Listformular[i]) ==str and "v" in Listformular[i]:
                maformule =  maformule + "Match( " +  Listformular[i] + "," + "TokenSeq("+ Listformular[i+2] +")," + "1)"
                i = i + 2
            
            if i < (len(Listformular)-1):
                 maformule =  maformule + " ∧ "
        
        maformule =  maformule + " ) "        
    
    return maformule



def ListOfCancatenateExpression(dagExpression):
    
    CanatenateString = ""
    CanatenateString = "Concatenate( "
    chainlist = []
    
    for item in dagExpression:
       chain = []
       for elt in item:
           if type(elt) == tuple:
               chain.append(list(item[elt])[0])
       
       chainlist.append(chain)
    
    chainlist  = list(flatten(chainlist))
    
    
    if len(chainlist) > 1:
      CanatenateString = CanatenateString + ",".join(chainlist) + " )"
    else:
      CanatenateString = ",".join(chainlist) 
    
    return CanatenateString




def MathStringexpressionCaseFail(entree):
    
    catexp = ExpressionConcatenateOfStringSigma(json.loads(entree))

    maformule = ""
    maformule = str(False)
    maformule = maformule + " V " 
    maformule =  maformule + "( "
    tokens = ""
    
    
    for key in catexp:
        tokens = catexp[key][1:len(catexp[key])]
        tokens = tokens.replace(" " , ",")

        maformule =  maformule + "Match(" +  key + "," + "TokenSeq("+ tokens +")," + "1)"
        maformule =  maformule + " ∧ "
    
    return  maformule[0:len(maformule)-len(" ∧ ")]



########################################Fin Etape 11#################################################

# Etape 12)Implementation de l'algorithme principale GenerateStringProgramm, qui  utilise toutes les fonctions precedentes

def GenerateStringProgram(S): #S est l'ensemble des paires d'exemples d'entrees sorties
    """ 
     Prend un ensemble de paires d'exemples  (entree, sortie) et retourne l'ensemble des programmes coherents avec  les exemples
    i.e  retourne l'ensemble de programmes qui permettent d'obtenir les sorties s a partir des entrees
    """
    T = []
    SigmaSet = set()
    newSetForme = set()
    B = {}  # resultat de GenerateBoolclassifier
    for elt in S:
        GenerateStrResult = GenerateStr(json.loads(elt[0]),elt[1])
        T.append((elt[0],GenerateStrResult))

    T =  GeneratePartition(T) # T est desormais une liste de tuple
        
    for  elt in S:
        SigmaSet =  SigmaSet.union(set([elt[0]]))

    for elt in T:
        newSetForme = set() 

        if type(elt[0]) == list:
            newSetForme = newSetForme.union(set(list(flatten(elt[0])))) 
        else:
            newSetForme = newSetForme.union(set([elt[0]]))

        SigmaMoins = SigmaSet - newSetForme
        
        valeureDeRetour = GenerateBoolClassifier(newSetForme,SigmaMoins)
        
        if valeureDeRetour == 'FAIL':
             B[str(newSetForme)] = 'FAIL'
        else:
            B[str(newSetForme)] = list(flatten(valeureDeRetour))

    # trions les elements de T (de la forme (Sigmaset, TraceSet)) dans l'ordre croissant de taill  de size(TraceSet)
   
    #T.sort(key=lambda x:SizeDag(len(x[0])-1,x[1]))  # tri de la liste T par ordre croissant des seconds elements du tuple.

    StringProgram = "" # ensemble resultatsss
    StringProgram = StringProgram + "Switch("
    
    for elt in B : 
       
            
        for elt2 in T:
            newSetForme2 = set() 
            if type(elt2[0]) == list:
                newSetForme2 = newSetForme2.union(set(list(flatten(elt2[0])))) 
            else:
                newSetForme2 = newSetForme2.union(set([elt2[0]]))
            
            if str(newSetForme2) == elt:
                break
        
        if B[elt] != 'FAIL':
            StringProgram = StringProgram + "("+ MathStringexpression(B[elt]) +","+ ListOfCancatenateExpression(elt2[1])+"),"
        
        else:
            StringProgram = StringProgram + "("+ MathStringexpressionCaseFail(list(newSetForme2)[0])+","+ ListOfCancatenateExpression(elt2[1])+"),"

    
    print(len(B.keys()))
    StringProgram  = StringProgram[0:len(StringProgram)-1]+ ")"
    return StringProgram 

########################################Fin Implementation#################################################



""" ***************** Debut Zone de test  et validation des fonctions******************** """

######################Debut test fonction GetclassC################################
ClasseC = GetClassC()
#######################Fin test fonction GetclassC###############################


######################Debut test fonction Cpos################################
""" cpos = Cpos("laure", -1)
print(cpos) """
#######################Fin test fonction Cpos###############################


######################Debut test fonction pos################################
""" pos = Pos("-706-7709-", ClasseC['NumTok'],ClasseC['HyphenTok'],-1)
#pos1 = Pos("425-706-7709", ClasseC['NumTok'],ClasseC['HyphenTok'],-2)
print(pos)
#print(pos1)
 """
#######################Fin test fonction poss###############################


######################Debut test fonction GenerateRegularExpressionRigth################################
""" test = GenerateRegularExpressionRigth("425-706-7709",4)
print(test) """
#######################Fin test fonction GenerateRegularExpressionRigth###############################


######################Debut test fonction GenerateRegularExpressionLeft################################
""" test = GenerateRegularExpressionLeft("425-706-7709",4)
print(test) """
#######################Fin test fonction GenerateRegularExpressionLeft###############################


######################Debut test fonction SubStrs###############################
""" test = SubStrs("425-706-7709",{"Pos(HyphenTok,NumTok,1)"},{"cpos(2)","Pos(NumTok, TokenSeq(HyphenTok,NumTok),2)"})
print(test) """
#######################Fin test fonction SubStrs###############################


######################Debut test fonction GenerateSubstring###############################
""" test = GenerateSubstring({"v1":"425-706-7709"},"706") """
#######################Fin test fonction GenerateSubstring###############################


######################Debut test fonction GenerateSubstring###############################
""" w1,EtaTilda1  = GenerateStr({"v1": "-706-7709"}, "70")
print(EtaTilda1)
print(len(w1[(0,2)]))
w2,EtaTilda2  = GenerateStr({"v1": "-706-7709"}, "06")
print(EtaTilda2)
print(len(w2[(0,2)])) """
#######################Fin test fonction GenerateSubstring###############################


######################Debut test fonction IntersectSubstr###############################

""" s1="SubStr(-706-7709,Pos(-706-7709,TokenSeq(HyphenTok),TokenSeq(NumTok,HyphenTok),-1),Pos(-706-7709,TokenSeq(HyphenTok),TokenSeq(NumTok),1))"
s2="SubStr(-706-7709,Pos(-706-7709,TokenSeq(HyphenTok),TokenSeq(NumTok,HyphenTok),-1),Pos(-706-7709,TokenSeq(HyphenTok),TokenSeq(NumTok),1))"
test = IntersectSubstr(s1,s2)
print(test) """
  
""" test1 =IntersectSubstr("SubStr(-706-7709,Cpos(-706-7709,2),Cpos(-706-7709,-7))","SubStr(-706-7709,Cpos(-706-7709,2),Cpos(-706-7709,-7))")
print("valeur de test1: ",test1) """

#######################Fin test fonction IntersectSubstr###############################

######################Debut test fonction GenerateStr###############################

#W1,EtaTilda1  =  GenerateStr({"v1": "Alex", "v2": "Asst."}, "Alex(Asst.)")
# print(EtaTilda1)
# print(len(w1[(0,2)]))
#W2,EtaTilda2  =  GenerateStr({"v1": "Jim", "v2": "Manager"}, "Jim(Manager)")
# print(EtaTilda2)
# print(len(w2[(0,2)]))

#######################Fin test fonction GenerateStr###############################

""" x,intersect = IntersectDag(EtaTilda1,W1,EtaTilda2,W2)
print(intersect)

for elt in x:
    print(elt,"\n",x[elt],"\n\n")
 """
#PrintDag(x,intersect,{"v1": "-506-7309"}, "506")

""" T = []
T.append((set({"v1": "-706-7709"}),(w1,EtaTilda1)))
T.append((set({"v1": "-706-7709"}),(w2,EtaTilda2)))

print("avant :  ", T)
print(GeneratePartition(T))
print(" :  ", T) """

""" positions,poslist = GeneratePosition("425-706-7709",6)
print(poslist)
print(positions)
print(len(poslist)) """

"""  ** Implementation de GenerateBoolClassifier*** """

#r2 , r3 = ExpressionConcatenate(inputelement,outputelement)
#ExpressionConcatenateOfString("Leorge Ciprian Necula")
#print(Executionfonction({"v1": "Keorge Ciprian paul"}, r2))
#print(Executionfonction({"v1": "Ken McMillan Alpha"}, r2))
#print(ExpressionConstString({"v1": "Alex","v2": "Asst."} ,"Alex(Asst.)" ))
    
""" x,y = GenerateStr({"v1": "425-706-7709"},"70")
print(x)

GenerateStringProgramm(liste_ensemble_exemples[0]) """


""" ***************** Fin Zone de test  et validation des fonctions******************** """



""" ***************** Debut Zone de test  et validation du programme principale******************** """
""" 
testSize = SizeDag(2,{(0,1):{1,2,3},(0,2):{7,8,9},(1,2):{4,5,6}})
print(testSize) """

""" liste_ensemble_exemples = GetExamples()
 
S = liste_ensemble_exemples[2]

print(GenerateStringProgram(S)) 
 """
""" ***************** Fin Zone de test  et validation du programme principale******************** """