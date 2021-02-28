import time
import subprocess
from subprocess import PIPE
import docker


def docker_restart(container_name,image_name,fwdports) :

	client = docker.from_env()
	container = client.containers.get(container_name)
	container.stop()
	container.remove()
	client.containers.run(image_name,name=container_name,ports=fwdports,detach=True)


if __name__ == '__main__':

	starttime = time.time()
	ports={"80":805}
	docker_restart("web-container","nginx:stable-alpine",ports)	
	elapse_time = time.time() - starttime
	print('elapsetime:{}'.format(elapse_time))
