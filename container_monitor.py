import docker
import sys
import time 

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
			container_list = self.client.containers.list()	#docker sdk api (all status) 
			#container_list = self.client.containers.list(label=self._container_namelist)	
			self._get_contains(container_list) #update status dictionary
		return self._container_sts_dict	



	#No Uses? docker exec wrapper method	
	def exec_cmd(self,containername,cmd):
		container = self.client.containers.get(containername)
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
			self._container_sts_dict[key] = "False"	 # is it correct?
	
	#status dictionary status reset
	def _contain_sts_reset(self):
		for key in self._container_sts_dict:
			self._container_sts_dict[key] = "False" #is it correct?

	#update status 
	def _get_contains(self,running_container):
		for container in running_container: 
			if container.name in self._container_sts_dict:
				self._container_sts_dict[container.name] = "True" #is it correct?	

	def get_attr(self,container_name):

	    cattrs = self.client.containers.get(container_name).attrs

	    # Build yaml dict structure

	    cfile = {}
	    cfile[cattrs['Name'][1:]] = {}
	    ct = cfile[cattrs['Name'][1:]]

	    values = {
	        'environment': cattrs['Config']['Env'],
	        'image': cattrs['Config']['Image'],
	        'networks': {x: {'aliases': cattrs['NetworkSettings']['Networks'][x]['Aliases']} for x in cattrs['NetworkSettings']['Networks'].keys()},
	        'volumes': cattrs['HostConfig']['Binds'],
	        'volume_driver': cattrs['HostConfig']['VolumeDriver'],
	        'volumes_from': cattrs['HostConfig']['VolumesFrom'],
	        'entrypoint': cattrs['Config']['Entrypoint'],
	        'user': cattrs['Config']['User'],
	        'working_dir': cattrs['Config']['WorkingDir'],
	        'domainname': cattrs['Config']['Domainname'],
	        'hostname': cattrs['Config']['Hostname'],
	        'privileged': cattrs['HostConfig']['Privileged'],
	        'restart': cattrs['HostConfig']['RestartPolicy']['Name'],
	        'read_only': cattrs['HostConfig']['ReadonlyRootfs'],
	        'stdin_open': cattrs['Config']['OpenStdin'],
	        'tty': cattrs['Config']['Tty']
	    }

	    networklist = self.client.networks.list()
	    networks = {}
	    for network in networklist:
	        if network.attrs['Name'] in values['networks'].keys():
	            networks[network.attrs['Name']] = {'external': (not network.attrs['Internal'])}

	    # Check for command and add it if present.
	    if cattrs['Config']['Cmd'] != None:
	        values['command'] = " ".join(cattrs['Config']['Cmd']),

	    # Check for exposed/bound ports and add them if needed.
	    try:
	        expose_value =  list(cattrs['Config']['ExposedPorts'].keys())
	        ports_value = [cattrs['HostConfig']['PortBindings'][key][0]['HostIp']+':'+cattrs['HostConfig']['PortBindings'][key][0]['HostPort']+':'+key for key in cattrs['HostConfig']['PortBindings']]

	        # If bound ports found, don't use the 'expose' value.
	        if (ports_value != None) and (ports_value != "") and (ports_value != []) and (ports_value != 'null') and (ports_value != {}) and (ports_value != "default") and (ports_value != 0) and (ports_value != ",") and (ports_value != "no"):
	            for index, port in enumerate(ports_value):
	                if port[0] == ':':
	                    ports_value[index] = port[1:]

	            values['ports'] = ports_value
	        else:
	            values['expose'] = expose_value

	    except (KeyError, TypeError):
	        # No ports exposed/bound. Continue without them.
	        ports = None

	    # Iterate through values to finish building yaml dict.
	    for key in values:
	        value = values[key]
	        if (value != None) and (value != "") and (value != []) and (value != 'null') and (value != {}) and (value != "default") and (value != 0) and (value != ",") and (value != "no"):
	            ct[key] = value

	    return cfile, network


# main routine (for subprocess call). TODO.other public method implmentaions are remain.
if __name__ == '__main__':
	intf = ContainerMngInterface(None)
	start_time = time.time()
	cfile,network = intf.get_attr("web-container")
	elapse_time = time.time() -start_time
	print(cfile)
	print(network)
	print('elapsetime:{}'.format(elapse_time))
