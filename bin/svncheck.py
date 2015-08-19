#!/usr/bin/env python
# abc repo svn check project initial
from ConfigParser import ConfigParser
import sys
import os
import os.path
import subprocess
import errno
import datetime,time


#from svn import repos, fs, delta, core
env = set(["production","staging","sandbox","dev"])


class LogDebugger():
      def __init__(self):
            self.now = time.strftime("%Y-%m-%d %H:%M:%S")
            self.log_file = time.strftime("%Y-%m-%d")
            self.log_path = "/abc/auto/svn/logs"
            
      def writetolog(self,logdata,project):
            f = open('%s/%s.log' % (self.log_path,self.log_file), 'a+') 
            content = self.now + " : [" + project + "]" + " [ " + logdata.rstrip() + " ] " + "\n"
            f.write(content)
            f.close()




class CaseConfigParser(ConfigParser):
    def __init__(self):
        ConfigParser.__init__(self)
        self.optionxform = str

class ProjectDeploy():
    log = LogDebugger()
       
    def __init__(self):
          self.data_root_path = "/abc/auto/svn"
          self.script_root_path = "/abc/auto/svn/scripts"
          
    def create_empty_script(self,filename):
          try:
                f = open(filename,'w')
                content = "#!/bin/bash"
                f.write(content)
                f.close()
                return True
          except:
                return False
          
    def svn_sync_script_check(self,path):
           if os.path.isfile(path):
                 return True
           else:
                 self.create_empty_script(path)
                 return True
           
    def svn_external_php(self,project,enviroment):
           self.project_sync_svn(project, enviroment)
                
    def directory_check(self,project,enviroment):
           #log = LogDebugger()
           path = os.path.join(self.data_root_path,"data",project,enviroment)
           try:
                os.makedirs(path)
                self.log.writetolog("Folder not exist, created folder success", project)
                return 1
           except OSError as exception:
                if exception.errno != errno.EEXIST:
                    #raise
                    return False
                else:
                    self.log.writetolog("Project already exist", project)
                    return 2
              
    def project_sync_svn(self,project,enviroment):
            project = project.replace("/", "_")
            sync_svn_script = self.script_root_path + "/" + enviroment + "_" + project + "_sync.sh"
            if self.svn_sync_script_check(sync_svn_script):
                  self.log.writetolog("Found script %s to execute" % sync_svn_script, project)
                  
                  chmod = subprocess.Popen("%s/chmod.sh %s" 
                  % (self.script_root_path,sync_svn_script), shell=True, stdout=subprocess.PIPE, 
                  stderr=subprocess.STDOUT)
                  
                  for chmodlogs in chmod.stdout.readlines():
                        self.log.writetolog(chmodlogs, project)
                  self.log.writetolog("Start sync process from %s " % sync_svn_script, project)                        
                  p = subprocess.Popen("sudo %s" 
                  % (sync_svn_script), shell=True, stdout=subprocess.PIPE, 
                  stderr=subprocess.STDOUT)
                  logdata = p.stdout.readlines()
                  for logs in logdata:
                        self.log.writetolog(logs, project)
                  
                              
            
            
    def project_checkout(self,project,enviroment):
            finder = ProjectsFinder()
            project_url = finder.get_project_details(project) + enviroment
            p = subprocess.Popen("sudo /abc/auto/svn/bin/project.sh %s %s %s " 
            % (project, enviroment, project_url), shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
            op = p.stdout.readlines()
            lens = len(op) - 1
            result = op[lens]
            self.log.writetolog(result, project)
            return result
    def project_update(self,project,enviroment):
            
            p = subprocess.Popen("sudo /abc/auto/svn/bin/update.sh %s %s %s " 
            % (project, enviroment, "update"), shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
            op = p.stdout.readlines()                  
            lens = len(op) - 1
            result = op[lens]
            for log in op:
                  self.log.writetolog(log, project)
            return result
    
    def project_build(self,project,enviroment):
            self.log.writetolog("Project is java, start building process", project)
#            if project == "DonationService":
#                  self.log.writetolog("Call jenkins hook", project)
#                  try:
#                        p = subprocess.Popen("sudo /abc/auto/svn/bin/jenkins_build.sh %s %s" 
#                        % (project, enviroment), shell=True, stdout=subprocess.PIPE, 
#                        stderr=subprocess.STDOUT)
#                        op = p.stdout.readlines()                  
#                        lens = len(op) - 2
#                        result = op[lens]
#                        self.log.writetolog(result, project)
#                        return result
#                  except:
#                        return False    
#                  
#            else:
            try:
                  p = subprocess.Popen("sudo /abc/auto/svn/bin/java_build.sh %s %s" 
                  % (project, enviroment), shell=True, stdout=subprocess.PIPE, 
                  stderr=subprocess.STDOUT)
                  op = p.stdout.readlines()                  
                  lens = len(op) - 2
                  result = op[lens]
                  self.log.writetolog(result, project)
                  return result
            except:
                  return False            
    

                  
    def start(self,project,enviroment):
            finder = ProjectsFinder()
            
            
            path = os.path.join(self.data_root_path,"data",project,enviroment)
            path_check = self.directory_check(project, enviroment)
            
            project_url = finder.get_project_details(project) + enviroment
            if path_check == 1:
                  result = self.project_checkout(project, enviroment)
                  if "Checked out revision" in result:
                        self.log.writetolog("Success %s to %s" % ( result,path ) , project)
                        if finder.checkprojecttype(project) == "java":
                              if self.project_build(project, enviroment):
                                    self.project_sync_svn(project, enviroment)
                        else:
                              self.project_sync_svn(project, enviroment)
                              
                  else:
                        
                        self.log.writetolog("Something error, contact admin for error %s" % result, project)
            if path_check == 2:
                  result = self.project_update(project, enviroment)
                  #print result
                  if "Updated to revision" in result:
                        if finder.checkprojecttype(project) == "external_php":
                              self.svn_external_php(project, enviroment)
                        if finder.checkprojecttype(project) == "java":
                              result = self.project_build(project, enviroment)
                              if "BUILD SUCCESSFUL" in result:
                                    self.log.writetolog("BUILD SUCCESSFUL on project %s " % project, project)
                                    self.project_sync_svn(project, enviroment)
                              else:
                                    self.log.writetolog("BUILD ERRORs %s" % result, project)
                        if finder.checkprojecttype(project) == "php":
                              self.project_sync_svn(project, enviroment)
                                    
                                             
                  elif finder.checkprojecttype(project) == "java":
                        if self.project_build(project, enviroment):
                              self.project_sync_svn(project, enviroment)
                  

            
                        
                      

class ProjectsFinder():
      log = LogDebugger()
      parser = CaseConfigParser()
      
      def __init__(self):
            self.repo = sys.argv[1]
            self.rev = sys.argv[2]
            self.log_no_matched = "No project matched"
            self.config_file = "/abc/auto/svn/config/config.cfg"

      def _get_project_details(self,project):
            self.parser.read(self.config_file)
            try:
                  if self.parser.get("java", project):
                        return self.parser.get("java", project)
            except:
                  try:
                        if self.parser.get("php", project):
                              return self.parser.get("php", project)
                  except:
                        if self.parser.get("external_php", project):
                              return self.parser.get("external_php", project)
                        
                        
                                         
      def get_project_details(self,project):
            self.parser.read(self.config_file)
            types = self.parser.sections()
            for type in types:
                  try:
                        project_type = self.parser.get(type, project)
                  except:
                        pass
            return project_type
            
      
      def checkprojecttype(self,project):
            proj_type = self._get_project_list_()
            result = proj_type.get(project)
            return result
      
            
      def get_project_list(self):
            self.parser.read(self.config_file)
            data = dict(parser.items('java'))
            keylist = []
            for key in data.keys():
                  keylist.append(key)
            return keylist
                  
      def _get_project_list_(self):
            self.parser.read(self.config_file)
            project_type = self.get_project_type_list()
            projects_dict = {}
            for type in project_type:
                  data = dict(self.parser.items(type))                  
                  for key in data.keys():
                        projects_dict.update({key:type})
            
            return projects_dict
      
      def get_project_type_list(self):
            self.parser.read(self.config_file)
            result = self.parser.sections()            
            return result
                        
      def get_env(self,path_list):
            try:
                  paths = set(path_list)
                  matched = paths.intersection(env)
                  matches = list(matched)
                  return matches
            except:
                  return False
      def _get_matched_project_(self,path_list):
            paths = set(path_list)
            projects_dict = self._get_project_list_()
            projects = []
            matched_projects = []
            for proj in projects_dict.keys():
                  n_proj = proj.split("/")
                  projects.append(n_proj)
            for i in range(len(projects)):
                  project = set(projects[i])
                  if len(list(paths.intersection(project))) > 0:
                        if len(matched_projects) == 0:
                              matched_projects.append(projects[i])
                        if len(matched_projects) > 0:
                              if len(list(paths.intersection(project))) > len(matched_projects[0]):
                                    matched_projects[0] = projects[i]
            
            
            return matched_projects
      
      def _get_project_(self,path_list):
            paths = set(path_list)
            projects_dict = self._get_project_list_()
            projects = []
            for proj in projects_dict.keys():
                  projects.append(proj)
                  
            projects = set(projects)
            
            matched = paths.intersection(projects)
            matches = list(matched)
            return matches
                
      def get_project(self,path_list):
            paths = set(path_list)
            projects = self._get_project_list_()
            projects = set(projects)
            
            matched = paths.intersection(projects)
            matches = list(matched)
            return matches
    
    
      def main(self):
            deploy = ProjectDeploy()
            svn_url = "https://svn.abc.vn/svn/"
            p =  subprocess.Popen("/abc/csvn/bin/svnlook dirs-changed  %s -r %s" % (self.repo, self.rev), 
                                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
            output = p.stdout.readlines()[0]
            path = output 
            path_list = path.split(os.sep)
            #project_matched = self._get_project_(path_list)
            project_matched = self._get_matched_project_(path_list)
            if len(project_matched) > 0:
                  #project = project_matched[0]
                  project = os.path.join(*project_matched[0])
                  if len(self.get_env(path_list)) > 0:
                        env =  self.get_env(path_list)
                        enviroment  = env[0]
                        self.log.writetolog("Found matched project %s update on environment %s" %  ( project, env[0] ) ,  project )
                        deploy.start(project, enviroment)
                          
                   
            else:
                  self.log.writetolog(self.log_no_matched,"NULL" )



def _usage_and_exit():
      sys.stderr.write("USAGE: %s REPOS-DIR\n" % (sys.argv[0]))

if __name__ == '__main__':
      if len(sys.argv) < 2:
            _usage_and_exit()
      else:

            job = ProjectsFinder()
            job.main()
