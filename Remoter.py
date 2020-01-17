from paramiko import SSHClient, AutoAddPolicy
from paramiko.hostkeys import HostKeys
from getpass import getpass
from typing import List


class _RePyError(Exception):
    pass


class _RePyClient(object):
    def __init__(self, user, host, pswd, port, sudo):
        self.user: str = user
        self.host: str = host
        self.pswd: str = pswd
        self.sudo: bool = sudo
        self.port: int = port

    def __repr__(self):
        return {'user': self.user, 'host': self.host, 'pswd': self.pswd, 'port': self.port, 'sudo': self.sudo}

    def __str__(self):
        return f'Client(user:{self.user}, host:{self.host}, pswd:{self.pswd}, port:{self.port}, sudo:{self.sudo})'


class SSH(_RePyClient, _RePyError):
    def __init__(self, user, host, pswd='', port=22, sudo=False):
        super().__init__(user, host, pswd, port, sudo)
        self._ssh = SSHClient()
        self._ssh.set_missing_host_key_policy(AutoAddPolicy)
        self._ssh.load_system_host_keys()

        if not HostKeys().lookup(self.host):
            if not self.pswd:
                getpass(f'No key found for {self.user}@{self.host}, please enter password: [WILL NOT ECHO]')
            self.ssh_client = self._ssh.connect(hostname=self.host, username=self.user, password=self.pswd,
                                                port=self.port)
        else:
            self.ssh_client = self._ssh.connect(hostname=self.host, username=self.user, port=self.port)

    def pyxecute(self, commands: List[str] or str) -> str:
        if isinstance(commands, list):
            for file in commands:
                command = self.sudoer(f'python <<EOF\n \n{open(file).read()} \nEOF')
                stdin, stdout, stderr = self._ssh.exec_command(command=command, get_pty=True)
                stdin.close()
                return stdout.read()
        elif isinstance(commands, str):
            command = self.sudoer(f'python <<EOF\n \n{commands} \nEOF')
            stdin, stdout, stderr = self._ssh.exec_command(command=command, get_pty=True)
            stdin.close()
            return stdout.read()
        else:
            raise _RePyError('SSH.pyxecute only accepts a list of files to read and execute or a single python '
                             'command string.')

    def execute(self, files: List[str] or str) -> str:
        if isinstance(files, list):
            for file in files:
                command = self.sudoer(f'{open(file).read()}')
                stdin, stdout, stderr = self._ssh.exec_command(command=command, get_pty=True)
                stdin.close()
                return stdout.read()
        elif isinstance(files, str):
            command = self.sudoer(files)
            stdin, stdout, stderr = self._ssh.exec_command(command=command, get_pty=True)
            stdin.close()
            return stdout.read()
        else:
            raise _RePyError('SSH.execute only accepts a list of files to read and execute ore a single shell command '
                             'string')

    def sudoer(self, text: str) -> str:
        if self.sudo:
            return f'sudo {text}'
        else:
            return text
