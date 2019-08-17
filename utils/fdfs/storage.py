# -*- coding:UTF-8 -*-
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):

    def __init__(self, client_conf=None, base_url=None):

        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):

        pass

    def _save(self, name, content):

        client = Fdfs_client(self.client_conf)

        # 上传文件到fast dfs系统中
        res = client.upload_by_buffer(content.read())

        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') != 'Upload successed.':

            raise Exception('fail to upload file to fast dfs')


        filename = res.get('Remote file_id')

        return filename

    def exists(self, name):

        return False

    def url(self, name):
        print(self.base_url+name)
        return self.base_url+name



