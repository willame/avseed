# -*- coding: UTF-8 -*-
import requests
import re
from BeautifulSoup import BeautifulSoup as bf
import sys
import os
import sqlite3
conn=sqlite3.connect('id.db')
reload(sys)
sys.setdefaultencoding('utf8')

def get_avlist():
  avlist=[]
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
      if re.match(pat,cid) is not None:
        video_id = re.match(pat,cid).group(1)+'-'+re.match(pat,cid).group(2)
      elif re.match(pat1,cid) is not None:
        video_id = re.match(pat1,cid).group(1)+'-'+re.match(pat1,cid).group(2)
      elif re.match(pat2,cid) is not None:
        video_id = re.match(pat2,cid).group(1)+'-'+re.match(pat2,cid).group(2)
      else:
        print re.match(pat3,cid).group(1)
        #print 'error'
      avlist.append(video_id)
  return avlist
def javbooks(avlist):
  s=requests.session()
  j=0
  f = open('url.txt','w')
  for i in avlist:
    a=conn.execute("select * from name where id=?",(i,))
    if a.fetchone() != None:
      url = 'http://javbooks.com/serch_censored/'+ i +'/serialall_1.htm'
      r = s.get(url)
      get_bt_url = bf(r.text)
      try:
        bt_url = get_bt_url.find('div',{'class':'Po_topic_title'}).find('a')['href']
        r = s.get(bt_url)
        result = bf(r.text)
        #f.write(result.find('div',{'class':'dht_dl_title_content'}).find('a')['href']+str('\n'))
        conn.execute("insert into name (id) values(?)",(i,))
        os.system("start "+result.find('div',{'class':'dht_dl_title_content'}).find('a')['href'])
        print "------------------------"
        sleep(5)
      except:
        j = j+1
        print i
  print j
  f.close()

def sukebei(avlist):
  s=requests.session()
  j=0
  for i in avlist:
    url = 'https://sukebei.nyaa.se/?page=search&cats=8_0&filter=0&term=' + i
    r = s.get(url)
    get_bt_url = bf(r.text)
    try:
      print get_bt_url.find('tr',{'class':'tlistrow trusted'}).find('td',{'class':'tlistname'}).find('a')['href']
    except:
      j = j+1
      print i
  print j

#sukebei(get_avlist())
#print("--------")
javbooks(get_avlist())
conn.commit()
conn.close()