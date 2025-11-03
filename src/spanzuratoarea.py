# --- Citire și prelucrare cuvinte ---
cuvinte = {}               
linii_invalide = 0                                                              
with open('data//words.txt', 'r', encoding='utf-8-sig') as fisier:            
    for linie in fisier:                                                        
        thing = linie.strip('\n')            
        if linie.count(';') == 2:             
            thing = thing.split(';')          
            if len(thing[0]) < 1 and len(thing[1]) < 1 and len(thing[2]) < 1:      
                print('\nEmpty member(s)!!!\n')
                linii_invalide += 1                  
                continue
            if len(thing[1]) == len(thing[2]):    
                cuvinte[thing[2].lower()] = thing[1].lower().replace('*', '_')
        else:                                
            print('\nline formatted wrongly!!!\n')
            linii_invalide += 1

# --- Variabile globale ---
lista_cuvinte = list(cuvinte.keys())
raspuns = ''            
ascuns = []            
raspuns_len = 0        
estimat_silabe = 0   
ghicit = False        
litere_ghicite = []    
litere_ghicite_n = 0  
incercari = 0         
total_incercari = 0   
gresit_consecutiv = 0  

litere = {chr(ch): 0 for ch in range(97, 123)}
for ch in 'ăâîșț':
    litere[ch] = 0

consoane = 'rntlscmbpdgfvșțhzjkxywq'   
vocale = 'aieuoăâî'                    
lungime_c = len(consoane)             
lungime_v = len(vocale)                
diftong = ('ea', 'oa', 'ia')         
hiat = ('ou', 'uu', 'ii', 'ao')        
dift_gasite = set()                 
cns_i = 0                           
vcl_i = 0                       
tura = 'V'                           
fortat = ''                      

# --- Alege tura pentru consoane sau vocale---
def alege_tura():
    global estimat_silabe, vocale, raspuns_len, fortat, gresit_consecutiv
    global vcl_i, lungime_v, cns_i, lungime_c, tura

    cuv_ascuns = ''.join(ascuns)            
    for i in range(raspuns_len - 1):
        v1, v2 = cuv_ascuns[i], cuv_ascuns[i + 1]
        if (i, i + 1) in dift_gasite:
            continue
        elif v1 + v2 not in hiat and v1 in vocale and v2 in vocale:
            if v1 == v2: continue
            elif v1 + v2 in diftong or (v1 not in 'ăâî' and v2 in 'iu'):
                estimat_silabe += 1            
                dift_gasite.add((i, i + 1))
 
    if gresit_consecutiv >= 3:         
        gresit_consecutiv = 0
        if tura == 'C' and vcl_i < lungime_v: tura = 'V'
        elif tura == 'V' and cns_i < lungime_c: tura = 'C'
        return

    if estimat_silabe < 1: tura = 'C'         

    for i in range(1, raspuns_len - 1):                 
        l1, l2 = cuv_ascuns[i - 1], cuv_ascuns[i + 1]
        if cuv_ascuns[i] == '_' and '_' not in l1 + l2:
            if l1 in 'cg' and l2 in 'ei': fortat = 'h'   
            elif l1 in vocale and l2 in vocale: tura = 'C' 
            elif l1 in consoane and l2 in consoane: tura = 'V' 
            else: tura = 'V'

    if ascuns[-1] == '_' and ascuns[-2] in consoane: tura = 'V'  
    if vcl_i >= lungime_v: tura = 'C' 
    if cns_i >= lungime_c: tura = 'V' 

# --- Bot alege următoarea literă ---
def bot():
    global litere, vocale, vcl_i, lungime_v, cns_i, lungime_c, tura

    if vcl_i >= lungime_v and cns_i >= lungime_c: return None  

    if tura == 'V':
        while vcl_i < lungime_v and litere[vocale[vcl_i]] != 0: vcl_i += 1 
        if vcl_i < lungime_v: return vocale[vcl_i]   
        tura = 'C'  
        return bot()
    else:           
        while cns_i < lungime_c and litere[consoane[cns_i]] != 0: cns_i += 1
        if cns_i < lungime_c: return consoane[cns_i]
        tura = 'V'
        return bot()

# --- Joc ---
def joc():
    global ghicit, litere_ghicite, raspuns_len, raspuns, ascuns, estimat_silabe, gresit_consecutiv
    global tura, incercari, total_incercari, litere, vocale, fortat, litere_ghicite_n

    while not ghicit:      
        if litere_ghicite_n == raspuns_len:     
            print(f"The raspuns is: {raspuns}")
            print('You won!\n')
            ghicit = True
            break

        #Afișează starea actuală a cuvântului
        print(' '.join(ascuns))   

        # Determină litera ghicită
        if fortat and litere[fortat] == 0:  
            att = fortat
            fortat = ''
        else:
            att = bot()

        print(f"\nAttempt #{incercari + 1}\nGuess a letter: {att}")  

        if att is None:    
            print('Error! All letters tried or something went wrong...\n')
            with open('results//erori.txt', 'a', encoding='utf-8-sig') as fisier:
                fisier.write(raspuns + '\n')
            break

        matches = False    
        dcrt_a = False
        for i, ch in enumerate(raspuns):
            if att == ch:
                ascuns[i] = att
                litere_ghicite_n += 1
                if att in vocale: estimat_silabe -= 1
                matches = True
            if 0 < i < raspuns_len - 1 and ascuns[i] == '_': dcrt_a = True

        if matches:     
            print(f"\n{att.upper()} fits!\n")
            litere_ghicite.append(att)
            litere[att] = 2  
            gresit_consecutiv = 0
            if att == 'â': litere['î'] = 1  
            elif att == 'î': litere['â'] = 1
        else:   
            print("\nWrong!\n")
            litere[att] = 1
            gresit_consecutiv += 1

        if not dcrt_a and litere['â'] == 0: litere['â'] = 1 
        if litere['î'] == 0 and (ascuns[0] != '_' or ascuns[1] in vocale or cns_i >= lungime_c // 2): fortat = 'î' 

        incercari += 1  
        total_incercari += 1
        alege_tura()

# --- Reset pentru fiecare tură de joc ---
def resetare(n):
    global vcl_i, lungime_v, cns_i, lungime_c, tura, gresit_consecutiv, dift_gasite
    global ghicit, ascuns, incercari, total_incercari, litere_ghicite, litere_ghicite_n
    global estimat_silabe, litere, vocale, raspuns, raspuns_len

    raspuns = lista_cuvinte[n]               
    ascuns = list(cuvinte[raspuns])          
    raspuns_len = len(raspuns)              
    estimat_silabe = raspuns_len // 3 + 1    

    litere = {chr(ch): 0 for ch in range(97, 123)} 
    for ch in 'ăâîșț': litere[ch] = 0

    dift_gasite = set()
    litere_ghicite = []   
    litere_ghicite_n = 0 
    incercari = 0         
    ghicit = False
    vcl_i = 0           
    cns_i = 0
    gresit_consecutiv = 0 
    tura = 'V'           

    for ch in ascuns:   
        if ch.isalpha() and litere[ch] != 2:  
            litere[ch] = 2  
            litere_ghicite_n += raspuns.count(ch)
            litere_ghicite.append(ch)
            if ch in vocale: estimat_silabe -= raspuns.count(ch)

# --- Cod principal ---
def main():
    lim = len(lista_cuvinte)  
    game_id = 1                
    with open('results//results.txt', 'w', encoding='utf-8-sig') as fisier:         
        fisier.write('game_id, incercari, solution, status, guess_sequence\n\n')
    with open('results//erori.txt', 'w', encoding='utf-8-sig') as fisier: 
        fisier.write('')
    
    for n in range(lim): 
        resetare(n)   
        joc()       
        with open('results//results.txt', 'a', encoding='utf-8-sig') as fisier:  
            fisier.write(f"{game_id}, {incercari}, {''.join(ascuns)}, {'OK' if ghicit else 'FAIL'}, {''.join(litere_ghicite)}\n")
        game_id += 1
    
    with open('results//results.txt', 'a', encoding='utf-8-sig') as fisier: 
        fisier.write(f"\nTotal incercari: {total_incercari}")
    
    print(f"\nTotal attempts: {total_incercari}\nAverage attempts: {total_incercari // lim}\n")  

if __name__ == '__main__':
    main()