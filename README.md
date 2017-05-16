# pyRecommender

Get stackoverflow answers automatically based on uncaught exceptions.

# Installation

```
$ git clone git@github.com:rahulnair23/pyRecommender.git
$ cd pyRecommender
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
```

The pyRecommender sessions are active for all interactive and command line python sessions.


# Example use:
```
$python test.py
pyRecommender session enabled (remove sitecustomize.py from PYTHONPATH to disable).
Traceback (most recent call last):
  File "test.py", line 4, in <module>
    print(float('k'))
ValueError: could not convert string to float: 'k'

Have you looked at: 
1.If you want to handle exceptions different depending on their origin, it is best to separate the different code parts that can throw the exceptions. Then you can just put a try/except block around the respective statement that throws the exception, e.g.:

    while True:
        try:
           ...
Source: http://stackoverflow.com/questions/13297748/python-except-valueerror-only-for-strings

2.replace this code

    GAIA_HOST = &#39;www.google.com&#39;
    LOGIN_URI = &#39;/accounts/ServiceLoginAuth&#39;

by this

    GAIA_HOST = &#39;accounts.google.com&#39;
    LOGIN_URI = &#39;/ServiceLoginAuth&#39;...
Source: http://stackoverflow.com/questions/19915335/python-cloud-print-authorization
```

# How does it work?

Python automatically imports the `site` package during initialization which in turn looks for `sitecustomize` which registers the custom hooks to get unhandled exceptions.