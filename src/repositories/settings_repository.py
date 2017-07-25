import os
import pickle

from models.setting import Setting


class SettingsRepository:
    def __init__(self, file):
        self.file = file

    def read(self):
        if os.path.isfile(self.file):
            fh = open(self.file, 'rb')
            setting = pickle.load(fh)
            fh.close()
            return setting
        setting = Setting()
        self.write(setting)
        return setting

    def write(self, setting):
        fh = open(self.file, 'wb')
        pickle.dump(setting, fh)
        fh.close()
