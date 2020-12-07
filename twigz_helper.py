from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def display_article_count_table(string):
    articleCountDictionary = {}
    listOfSentences = string.split('.')
    for sentence in listOfSentences:
        if sentence.count(' ') >= 5:
            if sentence not in articleCountDictionary:
                articleCountDictionary[sentence] = 1
            else:
                articleCountDictionary[sentence] +=1
    return articleCountDictionary

def display_author_count_table(string):
    authorCountDictionary = {}
    listOfSentences = string.split('.')
    for sentence in listOfSentences:
        author = sentence.split(' ')[0]
        if author.isupper():
            if author not in authorCountDictionary:
                authorCountDictionary[author] = 1
            else:
                authorCountDictionary[author] += 1
    return authorCountDictionary

## WRITE RESEARCH ARTICLES - CITATION TUPLES TO FILE
    
##    researchFILE = open('research_articles.txt','r')
##    articleFrequencyDictionary = {}
##    for line in researchFILE:
##        line = line.strip('\n')
##        articleFrequencyDictionary[line] = text.count(line.lower())
##    articleFrequencyTuples = []
##    for word in articleFrequencyDictionary:
##        articleFrequencyTuples.append((word,articleFrequencyDictionary[word]))
##    from operator import itemgetter, attrgetter
##    output = sorted(articleFrequencyTuples, key = itemgetter(1))
##    output = output[::-1]
##    outputFILE = open('research_articles_frequencies.txt','w')
##    for item in output:
##        outputFILE.write(str(item)+'\n')
##    outputFILE.close()
        



##   WRITE AUTHOR - CITATION TUPLES TO FILE
##    last_namesFILE = open('last_names_all.txt','r')
##    last_names = []
##    for line in last_namesFILE:
##        last_names.append(line.strip('\n'))
##    # text = "Abramo, G., et al.: A comparison of pers two approaches for measuring interdisciplinary research output: the disciplinary diversity of authors vs the disciplinary diversity of the reference list. J. Informetr. 12, 1182–1193 (2018) Anderson, M., et al.: The incompatibility of beneft-cost analysis with sustainability science. Sustain. Sci. 10, 33–41 (2015) Arli, D., Tjiptono, F.: God and green: investigating the impact of religiousness on green marketing. Int JNon-Proft Volun Sectors Market 22, e1578 (2017) Barbarossa, C., et al.: Personal values, green self-identity and electric car adoption. Ecol. Econ. 140, 190– 200 (2018) Baumard, N., Boyer, P.: Explaining moral religions. Trends Cogn Sci 17, 272–280 (2013) Bender, J., et al.: How moral threat shapes laypersons’ engagement with science. Pers. Soc. Psychol. Bull. 42, 1723–1735 (2016)"
##    text = text.split(' ')
##    authorLastNameFrequency = {}
##    for word in text:
##        word = word.strip(',').strip(':').strip('.').lower()
##        if word in last_names:
##            if word in authorLastNameFrequency:
##                authorLastNameFrequency[word] += 1
##            else:
##                authorLastNameFrequency[word] = 1
##    authorLastNameFrequencyTuples = []
##    for word in authorLastNameFrequency:
##        authorLastNameFrequencyTuples.append((word,authorLastNameFrequency[word]))
##    from operator import itemgetter, attrgetter    
##    output = sorted(authorLastNameFrequencyTuples, key=itemgetter(1))
##    output = output[::-1]
##    outputFILE = open('output.txt','w')
##    for item in output:
##        outputFILE.write(item+'\n')
##    outputFILE.close()

## WRITE SURNAME - FREQUENCY TUPLES TO FILE

def find_index_next_space(text,start=0):
    try:
        index = text.index(' ',start)
        return index
    except ValueError:
        return False
def find_index_start_name(text,start):
    notFound = True
    while notFound:
        start -= 1
        if text[start] == " " or text[start]=="\n":
            notFound = False
    return start + 1  # given a text string and starting index, searches for the index of the second blank
                    # space in the reverse direction, returns the index+1 of that space

def constructSetNames(text):
    start = 0
    setNames = set()
    while True:
        indexMiddleSpace = find_index_next_space(text, start)
        start += 1
        if isinstance(indexMiddleSpace,bool) and indexMiddleSpace == False:
            break
        try:
            if text[indexMiddleSpace+1] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if text[indexMiddleSpace+2] == ".":
                    beginningOfNameIndex = find_index_start_name(text,indexMiddleSpace)
                    setNames.add(text[beginningOfNameIndex:indexMiddleSpace+3])
            start = indexMiddleSpace + 1
        except IndexError:
            pass
    return setNames
if __name__=="__main__":
    text = convert_pdf_to_txt('bibliographies_only1.pdf')
    setNames = constructSetNames(text)
    nameFrequencyDict = {}
    for name in setNames:
        nameFrequencyDict[name] = text.count(name)
    print(nameFrequencyDict)
    outputFILE = open('output.txt','w')
    authorFrequencyTuples = []
    for word in nameFrequencyDict:
        authorFrequencyTuples.append((word,nameFrequencyDict[word]))
    from operator import itemgetter, attrgetter
    output = sorted(authorFrequencyTuples, key = itemgetter(1))
    output = output[::-1]
    outputFILE = open('output.txt','w')
    for item in output:
        outputFILE.write(str(item)+'\n')
    outputFILE.close()
