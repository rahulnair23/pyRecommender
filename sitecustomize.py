import sys
import atexit
import pickle
import io
from os.path import expanduser, isfile, join
import requests
import traceback

# sitecustomize is loaded by the site package at each invocation of the 
# interpreter. It just needs to be on PYTHONPATH


ANSWER_CACHE = join(expanduser('~'), 'so.pickle')
STACKOVERFLOW_API = "https://api.stackexchange.com/2.2/search/advanced"
STACKOVERFLOW_ANS = "https://api.stackexchange.com/2.2/answers/"
MAX_ANSWERS = 4
MAX_LENGTH = 300
SO_ANS_FILTER = "!--pn9sqW9y)i"


class pyRecommender(object):
    """ Stackoverflow query mechanism based on tracebacks """

    cache = {}

    @classmethod
    def key_generation(cls, e, v):
        """ Standardize query terms based on error class and message """
        return type(e).__name__ + " " + str(v)

    @classmethod
    def query(cls, k):
        """ Query stackoverflow for remedies to the malady """

        payload = {'q': k, 
                   'accepted': 'True', 
                   'tagged':'Python', 
                   'sort': 'relevance',
                   'order': 'desc', 
                   'site': 'stackoverflow'}

        r = requests.get(STACKOVERFLOW_API, payload)
        
        try:
            data = []
            questions = r.json()

            for i, c in enumerate(questions['items']):
                
                rq = requests.get(STACKOVERFLOW_ANS+str(c['accepted_answer_id']), 
                        data={'filter': SO_ANS_FILTER, 'site': 'stackoverflow'})
                
                answers = rq.json()
                
                for a in answers['items']:
                    data.append((a['body_markdown'], c['link']))
                
                if i+1>=MAX_ANSWERS:
                    break

            return data

        except ValueError:
            # Silently fails if error getting SO responses
            return None
    
    @classmethod
    def load_cache(cls):
        """ Loads a cached dictionary of previous remedies """
        if isfile(ANSWER_CACHE):
            pyRecommender.cache = pickle.load(io.open(ANSWER_CACHE, 'rb'))
        #print("Cache items: %u"%len(pyRecommender.cache))


    @classmethod
    def save_cache(cls, k, v):
        """ Save current answer to cache """
        pyRecommender.cache[k] = v
        with io.open(ANSWER_CACHE, 'wb') as pickle_file:
            pickle.dump(pyRecommender.cache, pickle_file, protocol=2)


def custom_exception_hook(exctype, value, tb):
    """ Custom hook to grab information on unhandled exceptions """
    
    # Print the stack trace again
    traceback.print_exception(exctype, value, tb)

    pyRecommender.load_cache()
    key = pyRecommender.key_generation(exctype, value)
    
    if key in pyRecommender.cache:
        # Get it from the cache
        value = pyRecommender.cache[key]
        
    else:
        # Query the api and store
        value = pyRecommender.query(key)
    
        if value is not None:
            pyRecommender.save_cache(key, value)

    # output the values
    if value is not None: 
        try:
            print("\nHave you looked at: ")
            for i, (a, l) in enumerate(value):
                print("%d.%s...\nSource: %s\n" % (i+1, a[0:MAX_LENGTH], l))
            
            print("\n")
        except KeyError:
            pass
    
def main():
    print("pyRecommender session enabled (remove sitecustomize.py from PYTHONPATH to disable).")
    sys.excepthook = custom_exception_hook


def before_exit():
    """ executed after program terminates """
    pass


atexit.register(before_exit)
main()
