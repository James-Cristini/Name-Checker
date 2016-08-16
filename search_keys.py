import string
CONSONANTS = \
["b", "c", "d", "f", "g", "j","k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z", ]
VOWELS = ["a", "e", "i", "o", "u", "y"]


def get_piu_key(name) :
    # Replace instances of ce or ci (where c is pronounced as s) with an s
    if "ce" in name  :
        c = list(name)
        c[name.index("ce")] = "s"
        name = "".join(c)
    if "ci" in name  :
        c = list(name)
        c[name.index("ci")] = "s"
        name = "".join(c)

    # Build a list that will contain the different version of the name that need to br screened, starting with the actual name itself
    name_list = [name]

    # Gets the first instance of added vowel only
    name_line = ""
    done = False
    for x in range(len(name)-1) :
        name_line += name[x]
        if name[x] in CONSONANTS and name[x+1] in CONSONANTS and not done:
            name_line += "a"
            done = True
    name_line += name[-1]
    if name_line not in name_list and len(name_line) >= 5:
        name_list.append(name_line)


    # Gets the last instance of added vowel only
    name_line = ""
    done = False
    for x in range(len(name)-1, 0, -1) :
        name_line = name[x] + name_line
        if name[x] in CONSONANTS and name[x-1] in CONSONANTS and not done :
            name_line = "a" + name_line
            done = True
    name_line = name[0] + name_line
    if name_line not in name_list and len(name_line) >= 5:
        name_list.append(name_line)


    # Gets all instances of added vowels
    name_line = ""
    for x in range(len(name)-1) :
        name_line += name[x]
        if name[x] in CONSONANTS and name[x+1] in CONSONANTS  :
            name_line += "a"
    name_line += name[-1]
    if name_line not in name_list and len(name_line) >= 5:
        name_list.append(name_line)


    # Add or remove the vowel(s) at the end of each version of the name
    new_list = []
    for x in name_list :
        if x[-1] not in VOWELS or x[-2:] == "qu":
            new = x + "a"
        elif x[-1] in VOWELS and x[-3:-1] == "qu" :
            new = x[:-1]
        elif x[-1] in VOWELS and x[-2] in VOWELS:
            new = x[0:-2]
        elif x[-1] in VOWELS :
            new = x[0:-1]
        else :
            print "something strange happened with", x
            pass

        if len(new) >= 5 :
            new_list.append(new)

    name_list += new_list
    search_key_line = " or ".join(name_list)
    return search_key_line


def check_x (x) :
    search_key = ""
    # If the name starts with x, we'll need to add search keys for a name starting with Z instead
    if x[0] == "x" :
        x = "z" + x[1:]
        search_key += get_piu_key(x) + "\n"
        # Check also for q/qu and ji/je with the names
        search_key += check_j(x)
        search_key += check_q(x)

    # If there are search keys, then return it, otherwise return an empty string
    if search_key :
        return search_key
    else :
        return ""


def check_j (x) :
    search_key = ""
    # Convert the j in "je' and "ji" strings to g
    if "je" in x :
        j = list(x)
        j[x.index("je")] = "g"
        x = "".join(j)
        if x[0] in VOWELS[0:5] :
            search_key += get_piu_key(x) + " or " + get_piu_key(x[1:]) + "\n"
        else:
            search_key += get_piu_key(x) + "\n"
    elif "ji" in x :
        j = list(x)
        j[x.index("ji")] = "g"
        x = "".join(j)
        if x[0] in VOWELS[0:5] :
            search_key += get_piu_key(x) + " or " + get_piu_key(x[1:]) + "\n"
        else:
            search_key += get_piu_key(x) + "\n"

    if search_key :
        return search_key
    else :
        return ""

def check_q(x) :
    # Check for a qu in the name and replace the q with a k
    search_key = ""

    # If there is a qu present in the name, change the q to a k
    if "qu" in x :
        qu_to_k = list(x)
        try:
            if x[x.index("qu")+2] not in VOWELS:
                qu_vowel_insert = list(x)
                qu_vowel_insert.insert(x.index("qu")+2, "a")
                y = "".join(qu_vowel_insert)

                if y[0] in VOWELS[0:5] :
                    search_key += get_piu_key(y) + " or " + get_piu_key(y[1:]) + "\n"
                else:
                    search_key += get_piu_key(y) + "\n"
        except IndexError:
            pass

        qu_to_k[x.index("qu")] = "k"
        x = "".join(qu_to_k)

        if x[0] in VOWELS[0:5] :
            search_key += get_piu_key(x) + " or " + get_piu_key(x[1:]) + "\n"
        else:
            search_key += get_piu_key(x) + "\n"


    # If there is a lone Q in the name, add a U so the screening also catches "Qu"/"Kw" hits
    elif "q" in x :
        q_to_qu = list(x)
        q_to_qu.insert(x.index("q") + 1, "u")
        x = "".join(q_to_qu)
        if x[0] in VOWELS[0:5] :
            search_key += get_piu_key(x) + " or " + get_piu_key(x[1:]) + "\n"
        else:
            search_key += get_piu_key(x) + "\n"


    if search_key :
        return search_key
    else :
        return ""

# Get the structural search key for each name
def get_structural_key(name) :

    #If the name is very short (4 letters or less) return a simplified key
    if len(name) < 5 :
        return name + "* or *" + name

    search_line = ""
    name = name

    # Add prefix + * to search line output
    search_line += name[0:4] + "* or "

    # If the last letter in the prefix is a vowl, we'll need to check with a '?' and the 5th letter
    if name[3] in VOWELS :
        search_line += name[0:3] + "?" + name[4] + "* or "

    # Add the combo and suffix keys
    search_line += name[0] + "*" + name[-3:] + " or *" + name[-4:]

    return search_line
