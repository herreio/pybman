import os
import pkg_resources

from datetime import date

from pybman.utils import read_plain_clean
from pybman.utils import write_list
from pybman.utils import read_json, write_json

class LocalData:

    def __init__(self, base_dir='data/'):

        self.base_dir = base_dir

        self.data_dir = self.base_dir + 'pubs/'
        self.data_paths = []
        self.data_paths_txt = self.base_dir + 'pubs.txt'
        self.data_exists = True

        self.pers_dir = self.base_dir + 'pers/'
        self.pers_paths = []
        self.pers_paths_txt = self.base_dir + 'pers.txt'
        self.pers_exists = True

        if not os.path.exists(self.base_dir):
            self.data_exists = False
            self.pers_exists = False
            os.mkdir(self.base_dir)
            os.mkdir(self.data_dir)
            os.mkdir(self.pers_dir)

        if not os.path.exists(self.data_dir):
            os.mkdir(self.data_dir)
            self.data_exists = False

        if not os.path.exists(self.pers_dir):
            os.mkdir(self.pers_dir)
            self.pers_exists = False

        if self.data_exists:
            if os.path.exists(self.data_paths_txt):
                self.data_paths = read_plain_clean(self.data_paths_txt)
                if self.data_paths:
                    print('local pulication data:')
                    for p in self.data_paths:
                        print(p)

        if self.pers_exists:
            if os.path.exists(self.pers_paths_txt):
                self.pers_paths = read_plain_clean(self.pers_paths_txt)
                if self.pers_paths:
                    print('local person data:')
                    for p in self.pers_paths:
                        print(p)

    # find path by given entity (id)
    def find_data_path(self, entity):
        if self.data_paths:
            for p in self.data_paths:
                if entity in p:
                    return p
            print("could not find path containing", entity)
        else:
            print('no local data!')
        return ''

    # get local data
    def get_data(self, data_id):
        path = self.find_data_path(data_id)
        if path:
            return read_json(path)
        else:
            print("could not find local data!")
            return {}

    # get data path for given id
    def generate_data_path(self, data_id):
        return self.data_dir + data_id + "--" + date.today().isoformat() + ".json"

    # remove old local data
    def clean_local_data(self, idx):
        path = self.find_data_path(idx)
        if path:
            print("removing file", path)
            os.remove(path)
        else:
            print("failed to remove file from entity", idx)

    # update list of paths
    def change_data_path(self, idx):
        pos = -1
        for i, path in enumerate(self.data_paths):
            if idx in path:
                pos = i
                break
        new = self.generate_data_path(idx)
        if pos < 0:
            self.data_paths.append(new)
            write_list(self.data_paths_txt, self.data_paths)
            print("local data file added", new)
        else:
            old = self.data_paths[pos]
            # self.clean_local_data(old)
            self.data_paths[pos] = new
            write_list(self.data_paths_txt, self.data_paths)
            print("local data file updated", new)

    # write local data file
    def store_data_local(self, idx, data):
        print("store local data of", idx)
        self.change_data_path(idx)
        path = self.generate_data_path(idx)
        write_json(path, data)

    def store_titles_local(self, idx, data):
        pass

def resolve_path(path):
    return pkg_resources.resource_filename('pybman', path)
