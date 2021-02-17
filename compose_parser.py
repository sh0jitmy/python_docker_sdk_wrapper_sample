import yaml
import os
import sys

#exception code
#sorry, this definitions are go-lang like exception codes.
PYDOCKPE_FILE_NOTEXIST =  "file is not exist."
PYDOCKPE_TAG_NOTEXIST =   "[services] tag is not exist."
PYDOCKPE_KEYWORD_NOTEXIST =   "keyword  is not match in dictionary."


class DockerComposeParser:
        def __init__ (self):
                self.opened = False
                self._docker = None
                self._servicelist = []
                self._networks = {}

        def open_compose(self,filepath='./docker-compose.yml'):
                self._reset_state() #initialize attribute
                err = ""
                if not os.path.exists(filepath):
                        err = PYDOCKPE_FILE_NOTEXIST
                        return self.opened,err

                with open(filepath, 'r') as ymlfile:
                        self._docker = yaml.safe_load(ymlfile)
                        if 'services' in self._docker:
                                for service in self._docker['services']:
                                        self._servicelist.append(service)
                                self.opened = True
                        else:
                                err = PYDOCKPE_TAG_NOTEXIST
                return self.opened,err

        def getvalue_from_service(self,keyword):
                found = False
                valuelist = []
                err = ""
                if not self._servicelist:
                        err = PYDOCKPE_TAG_NOTEXIST
                        return found,valuelist,err

                for servicename in self._servicelist:
                        if keyword in self._docker['services'][servicename]:
                                valuelist.append(self._docker['services'][servicename][keyword])
                                found = True
                if not found:
                        err = PYDOCKPE_KEYWORD_NOTEXIST + " your keyword is: " + keyword
                return found,valuelist,err
                
        def _reset_state(self):
                self.opened = False
                self._docker = None
                self._servicelist = []
                self._networks = {}


        ''' TODO GET NETWORK PARAMTER
                
        def getvalue_from_networks(keyword):
                found = False
                        
                valuelist.append(docker['services'][servicename][keyword])
                        found = True
                return found,valuelist  
        '''

# main routine 
if __name__ == '__main__':

        parser = DockerComposeParser()
        opened,err = parser.open_compose()

        if not opened:
                print(err)
                sys.exit(1)

        #print("getvalue")      
        exist,valuelist,err = parser.getvalue_from_service('container_name')
        if exist:
                print(valuelist)
        else:
                print(err)
