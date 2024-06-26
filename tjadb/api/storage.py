# -*- coding: utf-8 -*-
import os

from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return super().get_available_name(name, max_length)
