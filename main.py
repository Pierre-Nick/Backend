import sys
import threading
from packages.Listen import accept
from packages.Log import kwlog
from packages.Job.manager import monitor_jobs
kwlog.debug = True
threading.Thread(target=monitor_jobs).start()
kwlog.init()
accept.listen()
kwlog.close
