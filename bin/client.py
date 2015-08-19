#!/usr/bin/env python
import sys
import os
import requests
import random
import string
import base64
import hashlib


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

def run(repo,rev):
      url = "http://127.0.0.1:8888/api"
      key = "RHOx3Pt3kgMQpNldzD7ApFgIxk3KnL3wNzD7ApFgMbHgZX63ONnvigMQpNldzD7ApF__"
      #message = "projectname__environment__scriptname"
      code = id_generator(10)
      message = repo + "__" + rev + "__" + code
      
      strs = key + message
      m = hashlib.sha512(b'%s' % strs)
      token = m.hexdigest()
     

      headers = {'content-type': 'application/json'}
      payload = {'token':token,'repo':repo,'rev':rev,'code':code}
      r = requests.post(url, data=payload,headers=headers)
      print r.text
      
if __name__ == '__main__':
      if len(sys.argv) < 2:
            _usage_and_exit()
      else:
            repo = sys.argv[1]
            rev = sys.argv[2]
            run(repo,rev)

