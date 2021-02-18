import sys
import nmap #need to install nmap(by apt or yum,dnf)
import time

#simple port scanner (not syn,ping scans)
class SimplePortScanner:

        def get_activeport(self,host='127.0.0.1',portconf_string='1-1024'):
                active_portlist = []
                err = ""
                try:
                        nm = nmap.PortScanner()
                except nmap.PortScannerError:
                        err = "Nmap not found."
                        return False,active_portlist,err
                except:
                        err = "Unknown Error"
                        return False,active_portlist,err

                nm.scan(host,portconf_string)

                ports = nm[host]['tcp'].keys()
                for port in ports:
                        print("{}:{}".format(port,nm[host].tcp(port)))
                        if nm[host].tcp(port)['state'] == "open":
                                active_portlist.append(port)
                return True,active_portlist,err

        def get_activeportlist(self,host,checkport_strlist):
                activeportlist = []
                if not checkport_strlist :
                        err = "check port list is empty"
                        return False,activeportlist,err
                portconf_string = ','.join(checkport_strlist)
                return self.get_activeport(host,portconf_string)

# main routine

# Attention!!
# Must be run with administrator privileges
if __name__ == '__main__':
        scan = SimplePortScanner()
        portlist = ["21","22","80","33501"]

        #few seconds wait until port scan completed.    
        #wait time is depended on port list sizes. this list are elapsed is 0.7sec.(own machine envs) 
        start = time.time()
        ok,active_portlist,err = scan.get_activeportlist("127.0.0.1",portlist)
        elapsed_time = time.time()-start
        print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
        if ok :
                print("active ports:",active_portlist)
        else:
                print(err)
