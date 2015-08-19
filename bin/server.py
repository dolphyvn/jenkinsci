from bottle import route, run, template,post,request
import base64
import hashlib



@post('/api')

def index():
      key = "RHOx3Pt3kgMQpNldzD7ApFgIxk3KnL3wNzD7ApFgMbHgZX63ONnvigMQpNldzD7ApF__"
      token = request.forms.get('token')
      repo = request.forms.get('repo')
      rev = request.forms.get('rev')
      code = request.forms.get('code')
      
      message = str(repo) + "__" + str(rev) + "__" + str(code)
      
      strs = key + message
      m = hashlib.sha512(b'%s' % strs)
      checksum = m.hexdigest()
      if hashchecksum(token,checksum):
            deploy(repo,rev)
            return { "success" : True, "message" : "sucess to implement"}
      else:
            return { "success" : False, "message" : "Something wrong pls check log files"}
      
def hashchecksum(token,checksum):
      if checksum == token:
            return True
      else:
            return False
def deploy(repo,rev):
      from subprocess import Popen as start
      import subprocess
      
      cmd = "python /opt/auto/svn/bin/svncheck.py %s %s" % (repo, rev) 
      p = start(cmd,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      
      
run(host='127.0.0.1', port=8888,reloader=True)
