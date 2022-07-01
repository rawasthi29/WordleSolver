import random
import requests
from bs4 import BeautifulSoup

class AllWords():
    
    def __init__(self,url,InpId,tag):
        self.words=[]
        self.url = url
        self.InpId = InpId
        self.tag =tag
    
    def rawData(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        self.rawwords = soup.find(id=self.InpId)
        self.rawwords.prettify()

    def getWordsFromWeb(self):
        self.rawData()
        job_elements = self.rawwords.find_all(self.tag)
        for tag in job_elements:
            self.words.append(tag.text)

    def exporCsv(self,filename):
        self.FileName = filename
        with open(self.FileName,'w') as f:
            print (f"Exporting file {filename} with {len(self.words)} letter")
            file_lines = "\n".join(self.words)
            f.write(file_lines)
        f.close()

    def getWordsFromFile(self,filename):
        with open(filename,'r') as f:
            print (f"Reading file {filename} " , end='')
            file_lines = f.read()
            self.words = file_lines.split("\n")
            print(f"..........got {len(self.words)} letter.")
        f.close()

class Wordle():
    
    word_lst = []
    foundExact = {}
    foundPartial = {}
    foundNot = {}
    word_lst_full = []
    feedback=""
    
    def __init__(self):
        self.word = ""
        self.chances = 10
        self.counter = 1
        self.guess = ""

    def generateWord(self):
        self.word = random.choice(self.word_lst_full)
        #print(self.word)
        
    def drawBoxes(self):
        for i in range(len(self.word)):
            if len(self.foundExact)!=0 and len([val for val in self.foundExact if val==i])>0 and [val for val in self.foundExact if val==i][0]==i:
                print(self.foundExact[i],end=' ')
            else:
                print("_",end=' ')
        print("")
        
    def getFeedback(self):
        return self.feedback

    def setFeedback(self,feed):
        self.feedback = feed

    def setgMode(self):
        try:
            self.gmode = int(input("1 for Computer and 2 for Manual "))
        except:
            print("Defaulting to Computer mode")
            self.gmode = 1

    def getgMode(self):
        return self.gmode
    
    def input(self):
        print ("")
        if self.counter == 1 and self.length == 5:
            print("Some good starters words are 'board - unite', 'adieu - story', 'teary - pious', 'slice - tried - crane'. ALL THE BEST")
        print(f"Chance {self.counter} out of {self.chances + self.counter}")
        while True:
            self.guess = input("What word do you guess? ").lower()
            if len(self.guess) < self.length or len(self.guess) > self.length:
                print ("5 digit word only..")
                continue
            elif not self.inDict():
                print ("Word not in dictionary")
                continue
            break
                
        if self.getgMode()!=1:
            print("g - green, y - yellow, w - wrong / grey")
            while True:
                self.setFeedback(input("Feedback ").lower())
                if len(self.getFeedback()) < self.length or len(self.getFeedback()) > self.length:
                    print ("5 digit feedback only..")
                    continue
                elif not all(y in ['g','y','w'] and not y.isdigit() for y in self.getFeedback()):
                    print ("Plesae choose from g, y and w")
                    continue                 
                break

    def setgNumWrds(self):
        try:
            self.length = int(input("How many words Wordle? (5 Default) "))
        except:
            print("Defaulting to 5 Letter Wordle")
            self.length = 5
        
    def inDict(self):

        if self.guess.lower() in (x.lower() for x in self.word_lst_full):
            return True
        else:
            return False
    
    def check(self):
        if self.guess.lower() == self.word.lower() or self.getFeedback() == 'ggggg':
            if self.getFeedback() == 'ggggg':
                print(f"Well Done in {self.counter} tries !..")
                return True
            print ("That's correct!")
            return True
        elif self.chances == 0:
            print ("You have lost! The word was", self.word)
            return True
        else:        
            self.chances -= 1
            self.counter += 1
            return False           


    def Initialize(self):
        self.setgMode()
        self.setgNumWrds()

    def update(self):
        gEnd = False
        self.generateWord()
        self.drawBoxes()
        while not gEnd:
            self.input()
            gEnd = self.check()
            if not gEnd : self.info()
 
    def suggestion(self):    
        if len(self.word_lst) < 1:
            self.word_lst = self.word_lst_full.copy()

        temp_tuple = tuple(self.word_lst)
        for word in temp_tuple:
            for i in range(self.length):
                if self.feedback[i] == "w" and self.guess[i] in word:
                    self.word_lst.remove(word)
                    break
                elif self.feedback[i] == "g" and self.guess[i] != word[i]:
                    self.word_lst.remove(word)
                    break
                elif self.feedback[i] == "y" and self.guess[i] not in word:
                    self.word_lst.remove(word)
                    break
                elif self.feedback[i] == "y" and self.guess[i] == word[i]:
                    self.word_lst.remove(word)
                    break                      
        return self.word_lst

    
    def PrintSuggestion(self,guess_list):
        counter = 0
        if len(guess_list) != 0:
            for word in guess_list:
                print(word,end=", ")
                counter+=1
                if counter == 24:
                    print("")
                    counter = 0
        else:
            print("No suggestions")

 
    def info(self):
        feed = 5*['']
        for i in range(self.length):
            if  self.getgMode() == 1:
                if self.guess[i] in self.word and self.guess[i] == self.word[i]:
                    print (self.guess[i], "is in the correct postion")
                    self.setFeedback('%s%s%s'%(self.getFeedback()[:i],'g',self.getFeedback()[i+1:]))
                elif self.getgMode() == 1 and self.guess[i] in self.word and self.guess[i] != self.word[i]: 
                    print (self.guess[i], "is in the word but position not correct")
                    self.setFeedback('%s%s%s'%(self.getFeedback()[:i],'y',self.getFeedback()[i+1:]))
                elif self.getgMode() == 1 and self.guess[i] not in self.word:
                    print (self.guess[i]," is not in word")
                    self.setFeedback('%s%s%s'%(self.getFeedback()[:i],'w',self.getFeedback()[i+1:]))

            if (self.getFeedback()[i] == 'g'): 
                if(i not in self.foundExact):
                    self.foundExact.update({i:self.guess[i]})
                if self.guess[i] in self.foundPartial.values():
                    self.foundPartial = { k:v for k,v in self.foundPartial.items() if v!=self.guess[i] }                
            elif (self.feedback[i] == 'y'):
                if(i not in self.foundPartial):
                    self.foundPartial.update({i:self.guess[i]})                   
            elif (self.feedback[i] == 'w'):
                if(i not in self.foundNot):
                    self.foundNot.update({i:self.guess[i]})

        print("-----Partial Found   ", self.foundPartial,end = '           ')
        print("-----ExactFound      ", self.foundExact,end = '           ')
        print("-----Incorrect found ", [y for x,y in self.foundNot.items()])
        self.drawBoxes()
        hel=''
        while hel not in ['y','Y','n','N']:
            hel = input("show suggestion (y/n)? ")
        suggest = self.suggestion()
        if hel.lower()== 'y':
            self.PrintSuggestion (suggest)
                
  
w= Wordle()
w.Initialize()

url = "https://wordfind.com/length/"+str(w.length)+"-letter-words/"
InpId = str(w.length)+'-letter-words'
tag = "a"

wrds = AllWords(url,InpId,tag)

try:
    wrds.getWordsFromFile(str(InpId+".txt"))
except IOError:
    print ("Error: File does not appear to exist.")
    print ("Getting from web")
    wrds.getWordsFromWeb()
    wrds.exporCsv(InpId+".txt")

w.word_lst_full = wrds.words
w.update()       
