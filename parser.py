# -*- coding: iso-8859-15 -*-

# header registration = [ <class>, <email>, <name> ]

strClass = "Classe code"
strName = "Nom et prénom responsable"
strEmail = "Email Famille"

def parse_sites(filename, delim = ';'):
    sites = {}
    with open(filename, 'r', encoding="ISO-8859-15") as f:
        for line in f:
            splitLine = line.strip().split(sep=delim)
            codeClass = splitLine[0]

            for field in splitLine[1:]:
                if len(field) == 0:
                    continue
                field = " " + field
                if not field in sites.keys():
                    sites[field] = []
                sites[field].append(splitLine[0])

        return sites


def parse_charlemagne(filename, delim = ';'):
    parents = {}
    categories = {}

    with open(filename, 'r', encoding="ISO-8859-15") as f:
        header = f.readline()
        reg = header_registration(header, delim)
        if not reg:
            return False

        try:
            for line in f:
                splitLine = line.strip().split(sep=delim)
                codeClass = splitLine[reg[0]]
                emailParent = splitLine[reg[1]]
                nameParent = splitLine[reg[2]]

                parents[emailParent] = [nameParent, [], []]

                for i in range(len(codeClass)):
                    code = codeClass[:i+1]
                    parents[emailParent][1].append(code)
                    if not code in categories.keys():
                        categories[code] = []
                    categories[code].append(emailParent)

            categories[" All Parents"] = parents.keys()
            return parents, categories

        except: # if any error detected
            return {}, {}


def header_registration(header_string, delim=';'):
    regHeader = [None, None, None]
    headerList = header_string.split(sep=delim)
    counter = 0
    for field in headerList:
        field = field.strip()
        if field == strClass:
            if not regHeader[0] == None:
                return False
            regHeader[0] = counter

        if field == strEmail:
            if not regHeader[1] == None:
                return False
            regHeader[1] = counter

        if field == strName:
            if not regHeader[2] == None:
                return False
            regHeader[2] = counter
        counter += 1

    if None in regHeader:
        return False

    return regHeader

