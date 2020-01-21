# RePy

The RePy library's purpose is to create SSH connections and execute single 
python/shell commands, or entire python/shell files, as well as handle get/put with SFTP.

This is primarily designed as a backend to my other projects.

Ex:
```python
import Remoter
rem = Remoter.SSH(user='Jeff', host='192.168.240.3', pswd=password)
rem.pyxecute('import randint; for i in range(5): print(randint(1,6))'
rem.pyxecute(open('tortoise.sh').read())

sftp = Remoter.SFTP(user='Jeff', host='192.168.240.3', pswd=password)
sftp.get_file('/etc/hosts', './hosts')
sftp.put_file('./tortoise.sh', '/usr/local/bin')
```

### BUILT ON 
[Paramiko](https://github.com/paramiko/paramiko)
