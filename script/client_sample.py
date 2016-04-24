# coding: utf-8

import urllib
import urllib2

import cPickle as pickle


url = 'http://localhost:8888'
values = {'positive': 'イチロー'}
req = urllib2.Request(url, urllib.urlencode(values))
response = urllib2.urlopen(req)
#print response.read()

vector = pickle.loads(response.read())
print type(vector)
print vector
