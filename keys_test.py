CONSONANTS = \
["b", "c", "d", "f", "g", "j","k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z", ]
VOWELS = ["a", "e", "i", "o", "u", "y"]


""" NEED TO CHECK CODE AND CLEAN UP """

def get_piu_key(name) :
    search_key_text = ""
    names_list = [name]

    # bring in code from work comp and clean up/inspect that



"""
    # For each name in the originall list of stripped names
    for x in names_list :
        x = x.lower()
        line_list = [x]

        # Check if starting letter is an X
        if x[0] == "x" :
            z = list(x)
            z[0] = "z"
            line_list.append("".join(z))

        # Convert the j in "je' and "ji" strings to g
        if "je" in x :
            j = list(x)
            j[x.index("je")] = "g"
            line_list.append("".join(j))
        elif "ji" in x :
            j = list(x)
            j[x.index("ji")] = "g"
            line_list.append("".join(j))


        # Check for q and qu and replace accordingly
        if "qu" in x :
            qu = list(x)
            del qu[x.index("qu") + 1]
            line_list.append("".join(qu))
        elif "q" in x :
            q = list(x)
            q.insert(x.index("q") + 1, "u")

        for x in line_list:
            full_names_list.append(x)

    for x in full_names_list:
        if x[-1] in VOWELS and x[-2] in VOWELS and x[-3].lower() == "q" :
            full_names_list.append(x[0:-1])
        elif x[-1] in VOWELS and x[-2] in VOWELS :
            full_names_list.append(x[0:-2])
        elif x[-1] in VOWELS :
            full_names_list.append(x[0:-1])

        # If the first letter is a vowel, create a new version with the vowel removed
        if x[0] in VOWELS and x[1] in VOWELS :
            full_names_list.append(x[2:])
        elif x[0] in VOWELS :
            full_names_list.append(x[1:])

    return full_names_list

"""

"""
def get_piu_key(name) :

    name = name.lower()

    # If, for whatever reason a non-name got through, return an empty string
    if name.isspace():
        return ""

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
    if name_line not in name_list and len(name_line) > 4:
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
    if name_line not in name_list and len(name_line) > 4:
        name_list.append(name_line)


    # Gets all instances of added vowels
    name_line = ""
    for x in range(len(name)-1) :
        name_line += name[x]
        if name[x] in CONSONANTS and name[x+1] in CONSONANTS  :
            name_line += "a"
    name_line += name[-1]
    if name_line not in name_list and len(name_line) > 4:
        name_list.append(name_line)


    # Add or remove the vowel(s) at the end of each version of the name
    new_list = []
    # print name_list
    for x in name_list :
        if x[-1] in CONSONANTS :
            new = x + "a"
        elif x[-1] in VOWELS and x[-2] in VOWELS:
            new = x[0:-2]
        elif x[-1] in VOWELS :
            new = x[0:-1]

        else :
            pass
        if len(new) > 4 :
            new_list.append(new)

    name_list += new_list
    parse_line = " or ".join(name_list)
    return parse_line
"""

# Get the structural search key for each name
def get_structural_key(name) :

    #If the name is very short (4 letters or less) return a simplified key
    if len(name) < 5 :
        return name + "* or *" + name

    search_line = ""
    name = name.lower()

    # Add prefix + * to search line output
    search_line += name[0:4] + "* or "

    # If the last letter in the prefix is a vowl, we'll need to check with a '?' and the 5th letter
    if name[3] in VOWELS :
        search_line += name[0:3] + "?" + name[4] + " or "

    # Add the combo and suffix keys
    search_line += name[0] + "*" + name[-3:] + " or *" + name[-4:]

    return search_line
