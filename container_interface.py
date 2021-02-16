import docker
import sys

#docker container management interface
#docker sdk api wrapper class


class ContainerMngInterface:
        _client = 'None'  #docker.client instance
        _container_namelist = {}  #management containers name list
        _container_sts_dict = {}  #containers status(run or stale(any))
                                  #TODO composing containers list are included ?
        #Constructor Code
        def __init__(self,baseurl):
                if baseurl is not None:
                        self.client = docker.from_env(baseurl)
                else:
                        self.client = docker.from_env()

        #Set Management Contaniner List
        def set_container_list(self,container_namelist):
                if container_namelist is not None:
                        self._container_namelist = container_namelist
                        self._make_container_dict() # make status dictionary 

        #Get Management Container List  
        def get_container_list(self):
                return self._container_namelist

        #Get Container Run or Not Status
        def get_status(self):
                self._contain_sts_reset() #Status Reset (Not Runnning)
                if self._container_namelist is not None:
                        container_list = self.client.containers.list()  #docker sdk api (all status) 
                        #container_list = self.client.containers.list(label=self._container_namelist)   
                        self._get_contains(container_list) #update status dictionary
                return self._container_sts_dict

        #No Uses? docker exec wrapper method    
        def exec_cmd(self,containername,cmd):
                container = self.containers.get(containername)
                if container is not None:
                        try :
                                res = container.exec_run(cmd)
                        except docker.errors.APIError:
                                return False
                        return True
                        #res is tuple(output,exit_code)                 
        #def copydata(self,srcpath,dstcontainer,dstpath):

        #internal method        

        #initialze container status dictionary
        def _make_container_dict(self):
                for key in self._container_namelist:
                        self._container_sts_dict[key] = "False"  # is it correct?

        #status dictionary status reset
        def _contain_sts_reset(self):
                for key in self._container_sts_dict:
                        self._container_sts_dict[key] = "False" #is it correct?

        #update status 
        def _get_contains(self,running_container):
                for container in running_container:
                        if container.name in self._container_sts_dict:
                                self._container_sts_dict[container.name] = "True" #is it correct?       

# main routine (for subprocess call). TODO.other public method implmentaions are remain.
if __name__ == '__main__':
        intf = ContainerMngInterface(None)
        getlist = ["pedantic_panini","test_container_name"]
        intf.set_container_list(getlist)
        print(intf.get_status())
