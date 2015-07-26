import subprocess
import os


listOfShellCommands = ["python main.py 'AskHelpchat' > helpchat.html","python main.py 'meziapp' > meziapp.html","python main.py '@magic' > magic.html","python main.py '@operator' > operator.html","python main.py 'GoodServiceApp' > GoodserviceApp.html","python main.py 'MagicTigerApp' > magictiger.html","python main.py 'thehellogenie' > hellogenie.html"] 

for shellCommands in listOfShellCommands:
	print shellCommands
	subprocess.check_output(shellCommands,shell=True)
				