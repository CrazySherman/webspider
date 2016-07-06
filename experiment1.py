
# coding: utf-8

# In[1]:

import urllib2


# In[2]:

response = urllib2.urlopen('http://weixin.sogou.com/weixin?type=2&query=%E5%8D%97%E4%BA%AC&ie=utf8')


# In[3]:

print response


# In[4]:

print response.info()



# In[5]:

data= response.read()


# In[6]:

print data


# In[11]:

from HTMLParser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag is 'h4':
            print "Encountered a h4 start tag:", tag
    def handle_endtag(self, tag):
        if tag is 'h4':
            print "Encountered an h4 end tag :", tag


# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed(data)


# In[8]:

parser 


# In[9]:

parser = MyHTMLParser()
parser.feed(data)


# In[12]:

del MyHTMLParser


# In[13]:

del parser


# In[30]:

from HTMLParser import HTMLParser
newUrls = []
# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    flag = False
    def handle_starttag(self, tag, attrs):
        if tag == 'h4':
            self.flag = True
            print "Encountered a h4 start tag:", tag
        if self.flag and tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    newUrls.append(attr[1])
             
    def handle_endtag(self, tag):
        if tag == 'h4':
            self.flag = False
            print "Encountered an h4 end tag :", tag
    def handle_data(self,data):
        if self.flag == True:
            print data


# In[31]:

parser = MyHTMLParser()
parser.feed(data)


# In[32]:

newUrls


# In[33]:

type(newUrls[0])


# In[37]:

for i in range(0,len(newUrls)):
    newUrls[i] = 'weixin.sogou.com' + newUrls[i]


# In[38]:

newUrls


# In[36]:

'shit' + newUrls[0]


# In[42]:

res2 = urllib2.urlopen(newUrls[0])


# In[40]:

for i in range(0,len(newUrls)):
    newUrls[i] = 'http://' + newUrls[i]


# In[41]:

newUrls


# In[43]:

res2.info()


# In[44]:

res2.header


# In[45]:

h2 = res2.info()


# In[46]:

print h2


# In[48]:

data2 = res2.read()
print data2


# In[49]:

data2


# In[50]:

res2.info


# In[51]:

res2.info()


# In[52]:

print h2


# In[ ]:



