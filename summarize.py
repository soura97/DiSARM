from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
import sys
import cx_Oracle

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = defaultdict(int)
    mylist1=list(freq.keys())
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fitering
    m = float(max(freq.values()))
    for w in mylist1:
      freq[w] = freq[w]/m
      if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
        del freq[w]
    return freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)#When it encounters an assert statement, Python evaluates the accompanying expression, which is hopefully true. If the expression is false, Python raises an AssertionError exception.
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = defaultdict(int)
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)    
    return [sents[j] for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)

'''
filelist=['res1.txt','res2.txt','res3.txt']
for names in filelist:
  text=open(names, 'r').read()#read the file into a string
#print(fs.summarize(text,5))
  mylist=fs.summarize(text,5)
  print(mylist)
  thefile=open('e:/resout11.txt','a')
#thefile.write("hi there")
'''
def dbupload(outputfile,i):

	
	def printf (format,*args):
		sys.stdout.write (format % args)

	def printException (exception):
		error, = exception.args
		printf ("Error code = %s\n",error.code);
		printf ("Error message = %s\n",error.message);

	username = 'u1'
	password = 'pwd1'
	databaseName = "DISARM"
	
	try:
		connection = cx_Oracle.connect (username,password,databaseName)
	except cx_Oracle.DatabaseError, exception:
		printf ('Failed to connect to %s\n',databaseName)
		printException (exception)
		exit (1)
	
	cursor = connection.cursor ()
	cursor.execute("DROP TABLE IF EXISTS DISARM")
	
	sql = """CREATE TABLE DISARM (				
	         CATEGORY INT,
	         LOCATION CHAR(10),
	         SUMMARY CHAR(50) )"""
	#DISARM TABLE
	#CATEGORY	LOCATION	SUMMARY
	#   1		JOKA	        Yes ,local market has sufficient food.....
	cursor.execute(sql)
	with open(outputfile, "r") as output:
		lines=output.readlines()
	
	cursor.execute ("""INSERT INTO DISARM (CATEGORY,LOCATION,SUMMARY) VALUES(%d, ?, ?)""",(i,"JOKA",lines))
	connection.commit()
	cursor.close()
	connection.close()
	
	
fs = FrequencySummarizer()	
for i in range (1,4):
	inname="res"+str(i)+".txt"
    	#print(inname)
	text=open(inname, 'r').read()
	mylist=fs.summarize(text,3)
	 #print(mylist)
	outname="resout"+str(i)+".txt"
	#print(outname)
	thefile=open(outname,'w')
	#print("Hello")
	for item in mylist:
		thefile.write("%s\n" % item)
	dbupload(thefile,str(i),outname)
#thefile.write("\n".join(mylist))
#thefile.write(mylist)
thefile.close()
