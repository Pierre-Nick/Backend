import sys
import threading
from packages.Listen import accept
from packages.Log import kwlog
from packages.Job.manager import monitor_jobs
from packages.Database import MySQL
#from packages.Login.createAccount import add_new_user
kwlog.debug = True
threading.Thread(target=monitor_jobs).start()
kwlog.init()
MySQL.init()
accept.listen()
kwlog.close
MySQL.close()
#add_new_user("test01", "THISISA", "Test", "mrandal4@students.kennesaw.edu", "AA11223344556677".encode("utf-8"))
