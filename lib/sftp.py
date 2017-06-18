import os.path
import paramiko

class SSHConnection(object):

    def __init__(self, host, username, password, port=22):
        self.sftp = None
        self.sftp_open = False
        self.transport = paramiko.Transport((host, port))
        self.transport.connect(username=username, password=password)

    def _openSFTPConnection(self):
        if not self.sftp_open:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp_open = True

    def put(self, local_path, remote_path, key):
        self._openSFTPConnection()
        self.mkdir_recursive(remote_path+'/'+os.path.dirname(key))
        self.sftp.put(local_path, remote_path+'/'+key)
        print('Uploaded file '+key)

    def close(self):
        if self.sftp_open:
            self.sftp.close()
            self.sftp_open = False
            self.transport.close()

    def mkdir_recursive(self, remote_directory):
        self._openSFTPConnection()
        if remote_directory == '/':
            self.sftp.chdir('/')
            return
        if remote_directory == '':
            return
        try:
            self.sftp.chdir(remote_directory)
        except IOError:
            dirname, basename = os.path.split(remote_directory.rstrip('/'))
            self.mkdir_recursive(dirname)
            self.sftp.mkdir(basename)
            self.sftp.chdir(basename)
            return True

    def rmdir_recursive(self, remote_path):
        self._openSFTPConnection()
        remote_directory = os.path.dirname(remote_path)
        if remote_directory == '/':
            self.sftp.chdir('/')
            return
        if remote_directory == '':
            return
        if remote_directory == remote_path:
            return
        try:
            print('Removing dir.. '+remote_path)
            self.sftp.rmdir(remote_path)
            dirname, basename = os.path.split(remote_path.rstrip('/'))
            if self.sftp.listdir(dirname) == []:
                self.rmdir_recursive(dirname)
        except IOError, e:
            if 'No such file' in str(e):
                return False
            raise

    def remove(self, remote_path, key):
        self._openSFTPConnection()
        try:
            list_file = self.sftp.stat(remote_path+'/'+key)
        except IOError, e:
            if 'No such file' in str(e):
                return False
            raise
        try:
            self.sftp.remove(remote_path+'/'+key)
            print('Removed file '+key)
            try:
                if self.sftp.listdir(os.path.dirname(remote_path+'/'+key)) == []:
                    self.rmdir_recursive(os.path.dirname(remote_path+'/'+key))
            except IOError, e:
                if 'No such file' in str(e):
                    return False
                raise
        except IOError, e:
            if 'No such file' in str(e):
                return False
            raise