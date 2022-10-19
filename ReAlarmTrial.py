import os
import sys
scriptDir=os.path.split(os.path.realpath(__file__))[0]
sys.path.append(os.path.join(scriptDir,"packages"))

import platform

plat=platform.system()
if plat == 'Windows':
    print("ReAlarm in Windows")
    import realarm_win as worker
    worker.do_alarm()
elif plat == 'Linux':
    print("==Cannot Run in Linux==")
elif plat == 'Darwin':
    print("ReAlarm in Linux")
    import realarm_mac as worker
    worker.do_alarm()
