from pharma_inn_avoids_dict import PHARMA_AVOIDS_DICTIONARY, INN_AVOIDS_DICTIONARY
import sys
import string

reload(sys)
sys.setdefaultencoding('utf-8')


def strip_names(names_text):
    if not names_text.strip(string.whitespace) :
        print "nothing"
        return []

    stripped = []
    #Replace instances of brackets with parenthesis then split each line into a separate item for names_list
    new_text = ""
    for x in range(len(names_text)-1) :
        if names_text[x] == "*" and names_text[x+1] not in string.letters :
            pass
        else :
            new_text += names_text[x]
    new_text += names_text[-1]

    new_text = new_text.replace("[", "(").replace("]", ")").replace("*", "(").split("\n")

    for x in new_text :
        # Break each line up into its major components [Names, pronunciation, rationale, etc.]
        line_components = x.split("(")
        # Break the first component of line_components (should be all names potentially separated by a '/')
        names_on_line = line_components[0].split("/")
        # Add each name to the list of stripped names to be returned
        stripped += [x.strip(string.whitespace) for x in names_on_line if x.strip(string.whitespace)]
        #stripped.sort()
    return stripped


def build_project_avoids(avoid_list):
    # Create a new dictionary that will hold project avoids split up into its proper -fix category
    project_avoids = {
        "prefix" : [],
        "infix" : [],
        "suffix" : []
    }
    # Determine if avoids are prefix/infix/suffix and build the project_avoids dictionary accordingly
    for avoid in avoid_list:

        # Check for Infix first, if it starts and ends with a - or " it is an infix
        if avoid[0] == '"' and avoid[-1] == '"' or avoid[0] == '-' and avoid[-1] == '-':
            project_avoids["infix"].append(avoid.strip("-").strip('"'))

        # If it only ends in with a -, it's a prefix
        elif avoid[-1] == "-":
            project_avoids["prefix"].append(avoid.strip("-").strip('"'))

        # If it starts with a -, it's a suffix
        elif avoid[0] == "-":
            project_avoids["suffix"].append(avoid.strip("-").strip('"'))

        else:
            print "Problem with:", avoid
    # Return the full dictionary
    return project_avoids

def build_avoids_output(avoids):
    avoids_text_list = ["", "", ""]
    prefix_text = ""
    infix_text = ""
    suffix_text = ""

    avoids["prefix"].sort()
    avoids["infix"].sort()
    avoids["suffix"].sort()

    for x in avoids["prefix"] :
        prefix_text += x + "-\t" + avoids["all_avoids"][x + "-"] + "\n"
        avoids_text_list[0] = prefix_text

    for x in avoids["infix"] :
        infix_text += "-" + x + "-\t" + avoids["all_avoids"]["-" + x + "-"] + "\n"
        avoids_text_list[1] = infix_text

    for x in avoids["suffix"] :
        suffix_text += "-" + x + " \t" + avoids["all_avoids"]["-" + x] + "\n"
        avoids_text_list[2] = suffix_text

    return avoids_text_list

def write_avoids(project_avoids, internal_names, competitor_names) :
    with open("avoids.txt", "w") as f:
        line = ""
        for x in project_avoids:
            line = "Project:"
            line += ",".join(project_avoids)
        f.write(line + "\n")

        for x in internal_names:
            line = "Internal:"
            line += ",".join(internal_names)
        f.write(line + "\n")

        for x in competitor_names:
            line = "Competitor:"
            line += ",".join(competitor_names)
        f.write(line + "\n")
