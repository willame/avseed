import requests
import re
from BeautifulSoup import BeautifulSoup as bf
pat='[\w+\W+]+cid=(([a-z]+)00([0-9]+)|[0-9]+([a-z]+)00([0-9]+))'
s=requests.session()
r=s.get('http://www.dmm.co.jp/digital/videoa/-/list/=/sort=ranking/')
alllist=bf(r.text)
result = alllist.find('ul',{'id':'list'}).findAll('li')
for i in result:
    cid = i.find('p',{'class':'tmb'}).find('a')['href']
    print cid
    '''
    if re.match(pat,cid).group(2) is not None:
      video_id = re.match(pat,cid).group(2)+'-'+re.match(pat,cid).group(3)
    else:
      video_id = re.match(pat,cid).group(4)+'-'+re.match(pat,cid).group(5)
    print video_id
    '''