import sys
import string

def check_avoids(names, avoids, avoid_type, ignore="") :

    html_text = "<p style =\" white-space:pre-wrap;\">\n"
    hits = 0
    for name in names :

        for prefix in avoids["prefix"] :
            if prefix in ignore :
                pass
            elif name[:len(prefix)].lower() == prefix.lower() :
                html_text += "<span>"
                pos = 0
                hits += 1
                for x in range(len(name)) :
                    if x == pos :
                        html_text += "<span style=\"color:#ff0000;\">" + name[x]
                        if len(prefix) == 1 :
                            html_text += "</span>"
                    elif x == pos + len(prefix)-1 :
                        html_text += name[x] + "</span>"
                    else :
                        html_text += name[x]

                html_text += "\t<span style=\"color:#ff0000;\">%s</span></span>\n" % (prefix+"-")


        for infix in avoids["infix"] :
            if infix in ignore :
                pass
            elif (infix.lower() in name.lower()):# or (len(infix) == 1 and infix.lower() in name.lower()) or avoid_type == "project" and infix.lower() in name.lower():
                line = "<span>"
                pos = (name.lower()).index(infix.lower())
                hits += 1
                for x in range(len(name)) :
                    if x == pos :
                        line += "<span style=\"color:#ff0000;\">" + name[x]
                        #html_text += "<span style=\"color:#ff0000;\">" + name[x]
                        if len(infix) == 1 :
                            #html_text += "</span>"
                            line += "</span>"
                    elif x == pos + len(infix)-1 :
                        line += name[x] + "</span>"
                        #html_text += name[x] + "</span>"
                    else :
                        line += name[x]
                        #html_text += name[x]
                if line not in html_text:
                    html_text += line +"\t<span style=\"color:#ff0000;\">%s</span></span>\n" % ("-"+infix+"-")


        for suffix in avoids["suffix"]:
            if suffix in ignore :
                pass
            elif name[-len(suffix):].lower() == suffix.lower():
                html_text += "<span>"
                pos = (name.lower()).index(suffix)
                hits += 1
                for x in range(len(name)):
                    if x == pos :
                        html_text += "<span style=\"color:#ff0000;\">" + name[x]
                        if len(suffix) == 1 :
                            html_text += "</span>"
                    elif x == pos + len(suffix)-1:
                        html_text += name[x] + "</span>"
                    else:
                        html_text += name[x]

                html_text += "\t<span style=\"color:#ff0000;\">%s</span></span>\n" % ("-"+suffix)

    if hits == 0 :
        html_text += "None"
    return html_text + "</p>"



def check_internal_names(names, internal_names):
    html_text = "<p style =\" white-space: pre-wrap;\">"
    hits = 0
    for n in names:
        for i in internal_names :
            if n.lower() in i.lower() or i.lower() in n.lower():
                hits += 1
                line = n + " : <span style=\"color:#ff0000;\">"  + i + "</span>\n"
                html_text += line

    if hits == 0 :
        html_text += "None"
    return html_text + "</p>"



def check_competitor_names(names, competitor_names):
    html_text = "<p style =\" white-space: pre-wrap;\">"
    hits = 0
    for name in names :

        html_text += "<span>"
        for c in competitor_names :
            # Check for similar prefixes
            if c[0:3].lower() == name[0:3].lower() :
                prefix_hit = c[0:3]
                pos = 0
                hits += 1
                for x in range(len(name)) :
                    if x == pos :
                        html_text += "<span style=\"color:#ff0000;\">" + name[x]
                        if len(prefix_hit) == 1 :
                            html_text += "</span>"
                    elif x == pos + len(prefix_hit)-1 :
                        html_text += name[x] + "</span>"
                    else :
                        html_text += name[x]

                html_text += " : <span style=\"color:#ff0000;\">" + c + "</span></span>\n"

            # Check for similar 4-letter word parts
            infix_conflict = False
            for l in range (0, len(c)-3) :
                if c[l:l+4].lower() in name.lower() :
                    infix_conflict = c[l:l+4]
                    pos = l
            if infix_conflict :
                html_text += "<span>"
                pos = (name.lower()).index(infix_conflict.lower())
                hits += 1
                for x in range(len(name)) :
                    if x == pos :
                        html_text += "<span style=\"color:#ff0000;\">" + name[x]
                        if len(infix_conflict) == 1 :
                            html_text += "</span>"
                    elif x == pos + len(infix_conflict)-1 :
                        html_text += name[x] + "</span>"
                    else :
                        html_text += name[x]

                html_text +=  " : <span style=\"color:#ff0000;\">" + c + "</span></span>\n"


            # Checks for similar combo hits (first and last 3 letters)
            if (c[0] + c[-3:]).lower() == (name[0] + name[-3:]).lower() :
                conflict_part1 = c[0]
                conflict_part2 = c[-3:]
                pos = 0
                pos2 = name.lower().index(conflict_part2.lower())
                hits += 1
                for x in range(len(name)) :
                    if x == pos :
                        html_text += "<span style=\"color:#ff0000;\">" + name[x] + "</span>"
                    elif x == pos2 :
                        html_text += "<span style=\"color:#ff0000;\">" + name[x]
                    elif x == pos2 + len(conflict_part2)-1 :
                        html_text += name[x] + "</span>"
                    else :
                        html_text += name[x]


                html_text += " : <span style=\"color:#ff0000;\">" + c + "</span></span>\n"
    if hits == 0 :
        html_text += "None"
    return html_text + "</p>"
