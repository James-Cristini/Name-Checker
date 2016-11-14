# name_checker

##Introduction
This program is a Python/PyQT GUI application created for and intended to be used by the verbal department at Addison Whitney.
To put it simply, this program allows members of the department to perform faster and more accurate due dilligence on their submitted creative work.

###Due Dilligence
This program allows users to input different types of avoids (letters strings or full word/names) that can be checked against to be sure that no submitted names contain these letter strings or are overly similar to full names/words.
There are also two built in databases (not included here for confidentiality purposes) that can be checked against as well.
After avoids are input and saved, users can paste in their created names. The names are parsed out and checked against selected avoids. Conflicts are highlighted in red for easier reading.

###Domain name availability
In addition to the due diligence, this program allows users to quickly determine the status and availability of the .com associated with each created name through the use of requests with the Dynadot API

###Search Keys
Lastly, this program also offers the opportunity to quicken the search process when screenign names through an online trademark database. It willt ake in a list of names and break each down into the specific query needed for optimal searching


###Main Tab 
Inputting created names, selecting avoids to check, and viewing conflicts
![Picture](http://i.imgur.com/flSMGIy.png?1)

###Adding avoids
Project avoids allows you to check against specific letterstrings;
Internal/Presented checks letter-for-letter against names;
Compettior names checks for conflicting similarities (sharing letter strings such as prefixes, suffixes, infixes, etc.
![Picture](http://i.imgur.com/5y9kHjD.png?1)

###URL Availability
Checking for .com domain name status for each name.
green = available, red=taken
![Picture](http://i.imgur.com/EIQ18Op.png?1)
