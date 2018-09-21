import random

letras=["A", "B", "C"]
simbolos=["⇒", "¬"]
teoremas=["⇒(A,⇒(B,A))", "⇒(⇒(A,⇒(B,C)),⇒(⇒(A,B),⇒(A,C)))", "⇒(⇒(¬(A),¬(B)),⇒(B,A))"]
ejemplos=[] # son (string, string, float), por ejemplo ("⇒(A,A)", "⇒(A,⇒(B,A))", 1).
cadena=[] #va a ser una lista de enunciados que cada uno se genera agarrando al anterior y enchufandole algo.


def enunRandom(n): #genera un enunciado al azar de como mucho n pisos (por ej, ⇒(A,⇒(B,A)) tiene 3 pisos).
    if n==1:
        return random.choice(letras)
    else:
        if(random.uniform(0, 1)<0.8):
            s=random.choice(simbolos)
            if s=="¬":
                return "¬("+enunRandom(n-1)+")"
            if s=="⇒":
                return "⇒("+enunRandom(n-1)+","+enunRandom(n-1)+")"
        else:
            return random.choice(letras)

def reemplazoRandom(t): #le das un enunciado t y le enchufa algo random.
    #t=random.choice(teoremas)
    l=[]
    for i in range(0, len(letras)):
        l.append(letras[i])
    random.shuffle(l)
    while not l[0] in t:
        l.pop(0)
    return t.replace(l[0], enunRandom(2))

def armarCadena(n, t): #arma una cadena que tiene como primer elemento al enunciado t, y tiene exactamente n elementos.
    c=[]
    c.append(t)
    for _ in range(n-1):
        c.append(reemplazoRandom(c[len(c)-1]))
    return c

def agregarCadena1(c): #agarra la cadena c. para cada par de elementos j,i en c con 1<j<=i arma el ejemplo (i,j,1), o sea, guarda en ejemplos "desde el enunciado i se puede llegar al j" (por eso puntaje 1).
    for i in range(1, len(c)):
        for j in range(0, i+1):
            ejemplos.append((c[i],c[j],1))
    return ejemplos

def agregarCadena0(c, d): #agarra las cadenas c,d (hay que armarlas con distinto t). para cada par de elementos j,i con j en c, i en d, con 1<j<=i arma el ejemplo (i,j,1), o sea, guarda en ejemplos "desde el enunciado i NO se puede llegar al j" (por eso puntaje 0).
    for i in range(1, len(c)):
        for j in range(0, i+1):
            ejemplos.append((c[i],d[j],0))
    return ejemplos

def armarEjemplos(n): #llena la lista ejemplos. Hace 15n con 1 y 15n con 0
    for i in range(0, 3):
        for _ in range(n):
            agregarCadena1(armarCadena(3, teoremas[i]))
            agregarCadena0(armarCadena(3, teoremas[i]), armarCadena(3, teoremas[(i+random.randint(1,2))%3]))

armarEjemplos(3000) # en total se generan 30*n ejemplos (mitad con 0, mitad con 1)

unique_examples = set([])
for ejemplo in ejemplos:
    unique_examples.add(ejemplo)

with open('unique_logic.txt', 'w') as out:
    for s1, s2, score in unique_examples:
        out.write(f'{s1} {s2} {score} \n')
