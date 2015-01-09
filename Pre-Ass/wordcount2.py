import sys
import operator

def sort_helper(filename):
  words = []
  f = open(filename, 'rU')
  
  for line in f:
    words += line.split()
  
  f.close()
  words = map(lambda e:e.lower(), words)
  wordCountDictionary = dict((w,words.count(w)) for w in words)
  return wordCountDictionary

def print_words(filename):
  wordCountDictionary = sort_helper(filename)
  
  sortedByWord = sorted(wordCountDictionary.items(), key = operator.itemgetter(0))
  for x in sortedByWord:
    print x[0] + ' : ' + str(x[1]) 
  return 
  
def print_top(filename):
  wordCountDictionary = sort_helper(filename)
  
  sortedByOccurence = sorted(wordCountDictionary.items(), key = operator.itemgetter(1))
  sortedByOccurence.reverse()
  del sortedByOccurence[20:]
  for x in sortedByOccurence:
    print x[0] + ' : ' + str(x[1]) 
  return

###

# This basic command line argument parsing code is provided and
# calls the print_words() and print_top() functions which you must define.
def main():
  if len(sys.argv) != 3:
    print 'usage: ./wordcount.py {--count | --topcount} file'
    sys.exit(1)

  option = sys.argv[1]
  filename = sys.argv[2]
  if option == '--count':
    print_words(filename)
  elif option == '--topcount':
    print_top(filename)
  else:
    print 'unknown option: ' + option
    sys.exit(1)

if __name__ == '__main__':
  main()
