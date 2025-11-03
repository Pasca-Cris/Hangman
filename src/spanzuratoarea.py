# --- Citire și prelucrare cuvinte ---
cuvinte = {}                 # Creează un dicționar gol pentru a stoca cuvintele valide
linii_invalide = 0           # Creează un contor care ține evidența liniilor greșite din fișier                                                       
with open('data//words.txt', 'r', encoding='utf-8-sig') as fisier:                 #Deschide fișierul words.txt din folderul data pentru citire, folosind codarea utf-8-sig
    for linie in fisier:                      #Parcurge fiecare linie din fișier, una câte una                                    
        thing = linie.strip('\n')             #Elimină caracterul de „enter” de la sfârșitul liniei
        if linie.count(';') == 2:             #Verifică dacă linia are exact 2 puncte și virgulă ;, adică are 3 părți corecte
            thing = thing.split(';')          #Desparte linia în cele 3 părți separate de ;
            if len(thing[0]) < 1 and len(thing[1]) < 1 and len(thing[2]) < 1:     #Verifică dacă vreuna dintre cele 3 părți e goală (nu conține text)
                print('\nEmpty member(s)!!!\n')   #Afișează un mesaj de eroare, crește numărul liniilor invalide și sare peste acea linie
                linii_invalide += 1                  
                continue
            if len(thing[1]) == len(thing[2]):    #Dacă cele două părți (modelul și răspunsul) au aceeași lungime
                cuvinte[thing[2].lower()] = thing[1].lower().replace('*', '_')
        else:                                
            print('\nline formatted wrongly!!!\n')
            linii_invalide += 1

# --- Variabile globale ---
lista_cuvinte = list(cuvinte.keys())
raspuns = ''            #Inițializează un șir gol care va conține cuvântul curent ce trebuie ghicit
ascuns = []             #Creează o listă goală unde vor fi puse caracterele afișate
raspuns_len = 0         #Va stoca lungimea cuvântului curent
estimat_silabe = 0      #Ține o estimare a câte vocale (sau silabe) mai sunt necunoscute — e folosită ca strategie pentru alternarea între vocale și consoane.
ghicit = False          #Indică dacă jocul a fost câștigat (adevărat) sau nu (fals).
litere_ghicite = []     #Ține o listă cu toate literele deja ghicite, pentru a nu le repeta.
litere_ghicite_n = 0    #Contorizează câte litere au fost deja ghicite corect.
incercari = 0           #Numărul de încercări pentru cuvântul curent.
total_incercari = 0     #Numărul total de încercări pentru toate cuvintele din fișier

litere = {chr(ch): 0 for ch in range(97, 123)}
for ch in 'ăâîșț':
    litere[ch] = 0

consoane = 'rntlscmbpdgfvșțhzjkxywq'   
vocale = 'aieuoăâî'                    
lungime_c = len(consoane)              #Salvează numărul total de consoane, util pentru indexare în bucle.
lungime_v = len(vocale)                #Salvează numărul total de vocale, util pentru indexare în bucle.
diftong = ('ea', 'oa', 'ia')           #Tuplu cu diftongi
hiat = ('ou', 'uu', 'ii', 'ao')        #Tuplu cu hiaturi
dift_gasite = set()                    #Set gol unde se vor salva pozițiile diftongilor găsiți în cuvânt. Folosit pentru a nu re-verifica aceleași combinații.
cns_i = 0                              #Index curent pentru lista de consoane, pentru a ști ce literă urmează să fie ghicită.
vcl_i = 0                              #Index curent pentru lista de vocale, pentru a ști ce literă urmează să fie ghicită.
tura = 'V'                             #Variabila care indică ce tur este acum
fortat = ''                            #Variabilă folosită pentru a forța ghicirea unei litere specifice în cazuri speciale

# --- Alege tura pentru consoane sau vocale---
def alege_tura():
    global estimat_silabe, vocale, raspuns_len, fortat, gresit_consecutiv
    global vcl_i, lungime_v, cns_i, lungime_c, tura

    cuv_ascuns = ''.join(ascuns)                #Verifică fiecare pereche de litere din cuvântul (parțial) descoperit caută două vocale consecutive
    for i in range(raspuns_len - 1):
        v1, v2 = cuv_ascuns[i], cuv_ascuns[i + 1]
        if (i, i + 1) in dift_gasite:
            continue
        elif v1 + v2 not in hiat and v1 in vocale and v2 in vocale:
            if v1 == v2: continue
            elif v1 + v2 in diftong or (v1 not in 'ăâî' and v2 in 'iu'):
                estimat_silabe += 1             #Dacă acea combinație nu este deja marcată ca diftong o adaugă și crește estimarea silabelor
                dift_gasite.add((i, i + 1))
 
    if gresit_consecutiv >= 3:            #Dacă botul a greșit de 3 ori la rând, își schimbă strategia dacă încerca consoane trece la vocale si invers
        gresit_consecutiv = 0
        if tura == 'C' and vcl_i < lungime_v: tura = 'V'
        elif tura == 'V' and cns_i < lungime_c: tura = 'C'
        return

    if estimat_silabe < 1: tura = 'C'          #Dacă toate vocalele posibile par descoperite botul trece la consoane

    for i in range(1, raspuns_len - 1):                 #Parcurge fiecare poziție „_” din cuvântul ascuns Se uită la vecinii din stânga și din dreapta Dacă ambele vecine sunt litere (nu sunt _)
        l1, l2 = cuv_ascuns[i - 1], cuv_ascuns[i + 1]
        if cuv_ascuns[i] == '_' and '_' not in l1 + l2:
            if l1 in 'cg' and l2 in 'ei': fortat = 'h'     #Dacă avem combinația „c_e” sau „g_i” → setează fortat = 'h'
            elif l1 in vocale and l2 in vocale: tura = 'C'   #Dacă am vocale de ambele părți → probabil e o consoană în mijloc
            elif l1 in consoane and l2 in consoane: tura = 'V'  #Dacă am consoane de ambele părți → probabil e o vocală în mijloc
            else: tura = 'V'

    if ascuns[-1] == '_' and ascuns[-2] in consoane: tura = 'V'  #Dacă ultima literă e încă ascunsă și înaintea ei e o consoană probabil urmează o vocală
    if vcl_i >= lungime_v: tura = 'C'  #Dacă botul a încercat toate vocalele, trece la consoane
    if cns_i >= lungime_c: tura = 'V'  #Dacă a încercat toate consoanele, trece la vocale

# --- Bot alege următoarea literă ---
def bot():
    global litere, vocale, vcl_i, lungime_v, cns_i, lungime_c, tura

    if vcl_i >= lungime_v and cns_i >= lungime_c: return None  #Dacă nu mai există nici vocale, nici consoane disponibile, funcția se oprește și returnează None

    if tura == 'V':
        while vcl_i < lungime_v and litere[vocale[vcl_i]] != 0: vcl_i += 1  #Se caută prima vocală disponibilă
        if vcl_i < lungime_v: return vocale[vcl_i]    #Dacă s-a găsit o vocală liberă, funcția o returnează
        tura = 'C'   #Dacă nu mai sunt vocale disponibile, schimbă tura la consoane
        return bot()
    else:            #Caută prima consoană liberă, o returnează dacă o găsește si dacă nu mai sunt consoane, schimbă tura la vocale
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