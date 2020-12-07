import docx2txt


def extractKeywordCount_from_Word_Doc(filename, outputFILE):
    text = docx2txt.process(filename)
    list_of_keywords = text.split(', ')
    outputDict = {}
    for string in list_of_keywords:
        string = string.lower()
        if string not in outputDict:
            outputDict[string] = 1
        else:
            outputDict[string] += 1
    outputList = []        
    for keyword in outputDict:
        
        outputList.append((keyword, outputDict[keyword]))
    outputList.sort()
    outputList.reverse()
    outputFile = open(outputFILE, 'w')
    for e in outputList:
        outputFile.write(str(e[0])+': ' + str(e[1]) + ' ')
    outputFile.close()
    

filename = "BVE Keyword and SUBJECT COMBINED.docx"



extractKeywordCount_from_Word_Doc(filename, 'Twigz_(keywords and subjects).txt')
extractKeywordCount_from_Word_Doc("BVE KEYWORDS.docx", "Twigz_(keywords only).txt")
extractKeywordCount_from_Word_Doc("BVE SUBJECTS (not keywords) 1-17-20.docx", "Twigz_(subjects_only).txt")
