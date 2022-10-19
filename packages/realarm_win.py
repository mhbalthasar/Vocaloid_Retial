import sys
import os
import EncodeTimeID as tencoder
import datetime

import winreg

def __enum_key(hParent):
    subKeys=[]
    index=0
    while True:
        try:
            cPub=winreg.EnumKey(hParent,index)
            if len(cPub)==16:
                subKeys.append(cPub)
            index=index+1
        except:
            break
    return subKeys

def __search_v5_6():
    ret_tab=[]
    reg_paths=[
            "SOFTWARE\VOCALOID5\Application\Components",
            "SOFTWARE\VOCALOID6\Application\Components",
            "SOFTWARE\VOCALOID5\Voice\Components",
            "SOFTWARE\VOCALOID6\Voice\Components"
            ]
    for rpath in reg_paths:
        try:
            hkey=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rpath,access=winreg.KEY_ALL_ACCESS + winreg.KEY_WOW64_64KEY)
        except:
            continue
        sKey=__enum_key(hkey)
        winreg.CloseKey(hkey)
        for cid in sKey:
            ret_tab.append("{0}\{1}".format(rpath,cid))
    return ret_tab

def __realarm_v5_6(reg_paths,TimeID):
    ret=[]
    for rpath in reg_paths:
        try:
            hkey=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rpath,access=winreg.KEY_ALL_ACCESS + winreg.KEY_WOW64_64KEY)
        except:
            continue
        try:
            winreg.SetValueEx(hkey, 'Date', 0, winreg.REG_SZ, TimeID)
            ret.append(rpath)
        except:
            pass
        winreg.CloseKey(hkey)
    return ret

def __search_v3_4():
    ret_tab=[]
    reg_paths=[
            "SOFTWARE\VOCALOID4\DATABASE",
            "SOFTWARE\VOCALOID4\DATABASE41",
            "SOFTWARE\VOCALOID3\DATABASE\VOICE3"
            ]
    for rpath in reg_paths:
        try:
            hkey=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rpath,access=winreg.KEY_ALL_ACCESS + winreg.KEY_WOW64_32KEY)
        except:
            continue
        sKey=__enum_key(hkey)
        winreg.CloseKey(hkey)
        for cid in sKey:
            ret_tab.append("{0}\{1}".format(rpath,cid))
    return ret_tab

def __realarm_v3_4(reg_paths,TimeID):
    ret=[]
    for rpath in reg_paths:
        try:
            hkey=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rpath,access=winreg.KEY_ALL_ACCESS + winreg.KEY_WOW64_32KEY)
        except:
            continue
        sKey=__enum_key(hkey)
        try:
            winreg.SetValueEx(hkey, 'TIME', 0, winreg.REG_SZ, TimeID)
            ret.append(rpath)
        except:
            pass
        winreg.CloseKey(hkey)
    return ret

def do_alarm():
    print("===1.Generatoe TimeID===")
    TimeID=tencoder.Encode_TimeID(datetime.datetime.now())
    if type(TimeID)!=str or len(TimeID)<16:
        print("generate failure")
        return
    print("generated success:{}".format(TimeID))
    print("===2.Search VOCALOID5/6 Componments===")
    V56C=__search_v5_6()
    print("{} VOCALOID5/6 Componments found".format(len(V56C)))
    print("===3.Realarm VOCALOID5/6 Componments===")
    V56B=__realarm_v5_6(V56C,TimeID)
    print("{} VOCALOID5/6 Componments realarmed".format(len(V56B)))
    print("===4.Search VOCALOID3/4 Voice Banks===")
    V34C=__search_v3_4()
    print("{} VOCALOID3/4 Voice Banks found".format(len(V34C)))
    print("===5.Realarm VOCALOID3/4 Voice Banks===")
    V34B=__realarm_v3_4(V34C,TimeID)
    print("{} VOCALOID3/4 Voice Banks realarmed".format(len(V34B)))
    print("===All Done===")

