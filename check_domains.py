import sys
import requests


DYNADOT_API_KEY = '9Tm6Tg7r808t74F9N9B6S7ukS7V7OY6r7B8X7H719C'


def check_domain(names) :
    try:
        # Start a new empty dictionary that will contain the name and URL availabilty
        domains = {}
        count = 0
        html_text = "<p style =\" white-space: pre-wrap;\" >"
        # Base URL with api key included
        url = "https://api.dynadot.com/api2.html?key=" + DYNADOT_API_KEY + "&command=search"

        # Add each name + .com to the url
        for x in names :
            url += "&domain" + str(count) + "=" + x.lower() + ".com"
            count += 1
        print "Accessing Dynadot API"

        # Store the requestedresults
        r = requests.get(url)
        text = ""
        # Strip the results text on all new lines (sometimes dynadot's API returns results with missing /n so it is not a good idae to split on the \n...)
        for x in r :
            text += x.strip("\n")
        print text

        #split each result on "domain" because that part will always occur in returned results
        for x in text :
            new_ls = (text.strip("\n")).split("domain")

        for x in new_ls :
            # Each line should look like: ##, name.com,,yes/no,
            # Split each line on the commas
            line_ls = x.split(",")

            if len(line_ls) > 1 :
                # If the first character of the first item in each line's list is a number, then we have a domain result (there are a few times when a line is not related to domain results)
                if line_ls[0][0] in "0123456789" :
                    print line_ls[1] + " : " + line_ls[3]

                    # Parse the results and store them in a dictionary
                    if line_ls[3] == "yes" :
                        name = (line_ls[1][0:-4]).lower()
                        domains[name] = "avl"
                    else :
                        name = (line_ls[1][0:-4]).lower()
                        domains[name] = "XX"

        # Quick double check for any names that may not have made it into the dictionary
        # this shouldn't happen, but the dynadot API is a bit... strange sometimes
        for x in names :
            if x.lower() not in domains.keys() :
                print x + ".com not found in dictionary"
                domains[x] = "XX"

        # Adds results to the html_text that will be returned and shown to the user
        for x in names :
            if domains[x.lower()] == "XX" :
                html_text += "<span style=\" color:#ff0000;\" >XX : %s</span>\n" % (x)
            elif domains[x.lower()] == "avl" :
                html_text += "<span style=\" color:#348017;\" >avl : %s</span>\n" % (x)
            else :
                print "Something strange happened with", x

        print "Returning domain information"
        return html_text


    except Exception as e:
        return "<p>Whoops!</p>\n\n<p>%s</p?" %(str(e))
