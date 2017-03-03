import requests
import re
from BeautifulSoup import BeautifulSoup as bf
pat='[\w+\W+]+cid=([a-z]+)00([0-9]+)'
pat1='[\w+\W+]+cid=[0-9]+([a-z]+)00([0-9]+)'
pat2='[\w+\W+]+cid=[a-z]_[0-9]+([a-zA-Z]+)00([0-9]+)'
pat3='[\w+\W+]+cid=([\w+])/'
s=requests.session()
r=s.get('http://www.dmm.co.jp/digital/videoa/-/list/=/sort=ranking/')
alllist=bf(r.text)
result = alllist.find('ul',{'id':'list'}).findAll('li')
for i in result:
    cid = i.find('p',{'class':'tmb'}).find('a')['href']
    print cid
    if re.match(pat,cid) is not None:
      video_id = re.match(pat,cid).group(1)+'-'+re.match(pat,cid).group(2)
    elif re.match(pat1,cid) is not None:
      video_id = re.match(pat1,cid).group(1)+'-'+re.match(pat1,cid).group(2)
    elif re.match(pat2,cid) is not None:
      video_id = re.match(pat2,cid).group(1)+'-'+re.match(pat2,cid).group(2)
    else:
      print re.match(pat3,cid).group(1)
    print video_id
