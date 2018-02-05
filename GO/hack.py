import re


re_unquoted_string = re.compile(r'[^\n]+')
re_quoted_string = re.compile(r' " ( [^\n"\\]*  (?:"|\\.) )+', re.VERBOSE | re.S )
re_BT = re.compile("(true|false)")

re_id = re.compile('''
  ((?:http|https) : \S+) # URL AS ID
| ( [a-zA-Z][a-zA-Z_]* : \d+) # prefixed canonical
| ( [^ \t:]+ : \S+) # prefixed non canonical
| ( [^ \t:]+ ) # unprefixed
''', re.VERBOSE)


# example
'''" primer \\ za \t string \
sta sve moze"'''

def ID(line, pos):
    match = re_id.match(line, pos=pos)
    return match.group(0), match.end(0)

def Def(line, pos):
    match = re_quoted_string.match(line, pos=pos)
    return match.group(0), match.end(0)


def TVP(line, pos):
    match = re_unquoted_string.match(line, pos=pos)
    return match.group(0), match.end(0)

def BT(line, pos):
    match = re_BT.match(line, pos=pos)
    return match.group(0) == 'true', match.end(0)


term_func = {
    "id" : TVP,
    "is_anonymous" : BT,
    "name" : TVP,
    "namespace" : TVP,
    "alt_id" : TVP,
    "def" : Def,
    "comment" : TVP,

    "is_a" : ID,

    "is_obsolete" :  BT ,
    "replaced_by" : TVP ,
    "consider" : TVP ,
    "created_by" : TVP ,
    "creation_date" : TVP

}



# with open("../data/go_1.obo", "r") as obo_file:
#     for term_description in re.findall(r"\[Term\]\n(.+?)\n\n", obo_file.read(), re.S ):
#
#         for line in term_description.split("\n"):
#             line_match  = re.match('^([A-Za-z_]+):\s*', line)
#             tag, endpos = line_match.group(1), line_match.end()
#
#             parser = term_func.get(tag)
#             if(parser):
#                 value, endpos = parser(line, endpos)
#                 print('%s:'%tag, value, repr(line[endpos:]))
#                 print(line)
#
#         print("-------")





with open("../data/go_1.obo", "r") as obo_file:
    for term_description in re.findall(r"\[Term\]\n(.+?)\n\n", obo_file.read(), re.S ):

        id = None
        for line in term_description.split("\n"):
            line_match  = re.match('^([A-Za-z_]+):\s*', line)
            if not line_match: ## drugi term
                break
            tag, endpos = line_match.group(1), line_match.end()

            parser = term_func.get(tag)
            if(parser):
                value, endpos = parser(line, endpos)
                if tag == 'id':
                    id = value
                print(id, '%s:'%tag, value, repr(line[endpos:]))

        print("-------")
