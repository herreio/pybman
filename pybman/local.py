import os

from datetime import date

from pybman import data
from pybman import utils


class LocalData:

    def __init__(self, base_dir='./data/', create=False):

        self.data_dir = os.path.realpath(base_dir)
        self.data_file = os.path.join(self.data_dir, 'paths.txt')
        self.data_exists = True

        self.ou_dir = os.path.join(self.data_dir, 'ou')
        self.ctx_dir = os.path.join(self.data_dir, 'ctx')
        self.pers_dir = os.path.join(self.data_dir, 'pers')

        self.ou_exists = True
        self.ctx_exists = True
        self.pers_exists = True

        # self.data_dir = self.base_dir + '/pubs/'
        # self.data_paths_txt = self.base_dir + 'pubs.txt'

        self.data_paths = []

        # self.pers_paths = []
        # self.pers_paths_txt = self.base_dir + 'pers.txt'
        # self.pers_exists = True

        if not os.path.exists(self.data_dir):
            self.data_exists = False
            self.ou_exists = False
            self.ctx_exists = False
            self.pers_exists = False
            if create:
                os.mkdir(self.data_dir)
                os.mkdir(self.ou_dir)
                os.mkdir(self.ctx_dir)
                os.mkdir(self.pers_dir)

        if not os.path.exists(self.ou_dir) and self.ou_exists:
            self.ou_exists = False
            if create:
                os.mkdir(self.ou_dir)

        if not os.path.exists(self.ctx_dir) and self.ctx_exists:
            self.ctx_exists = False
            if create:
                os.mkdir(self.ctx_dir)

        if not os.path.exists(self.pers_dir) and self.pers_exists:
            self.pers_exists = False
            if create:
                os.mkdir(self.pers_dir)

        if self.data_exists:
            if os.path.exists(self.data_file):
                self.data_paths = utils.read_plain_clean(self.data_file)
                if self.data_paths:
                    print('local pulication data:')
                    for p in self.data_paths:
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
            json_data = utils.read_json(path)
            return data.DataSet(data_id, data=json_data)
        else:
            print("could not find local data!")
            return {}

    # write local data file
    def store_data(self, idx, dict_data):
        print("store local data of", idx)
        self.change_data_path(idx)
        path = self.generate_data_path(idx)
        utils.write_json(path, dict_data)

    # get data path for given id
    def generate_data_path(self, data_id):
        return self.data_dir + data_id + "--" + date.today().isoformat() + ".json"

    def change_data_path(self, idx):
        """
        update list of paths
        """
        pos = -1
        for i, path in enumerate(self.data_paths):
            if idx in path:
                pos = i
                break
        new = self.generate_data_path(idx)
        if pos < 0:
            self.data_paths.append(new)
            utils.write_list(self.data_file, self.data_paths)
            print("local data file added", new)
        else:
            old = self.data_paths[pos]
            # self.clean_local_data(old)
            self.data_paths[pos] = new
            utils.write_list(self.data_file, self.data_paths)
            print("local data file updated", new)

    # remove old local data
    def clean_local_data(self, idx):
        """
        clean up local data
        """
        path = self.find_data_path(idx)
        if path:
            print("removing file", path)
            os.remove(path)
        else:
            print("failed to remove file from entity", idx)

#    def store_titles_local(self, idx, data):
#        pass
