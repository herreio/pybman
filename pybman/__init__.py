name = 'pybman'

from pybman import data
from pybman import local
from pybman import export

class Pybman:

    def __init__( self, ou_id='', ctx_id='', data_dir='./data/', load=False):

        self.ou_id = ou_id
        self.ctx_id = ctx_id

        self.ou_data = None
        self.ctx_data = None
        self.pers_data = None
        self.loc_data = None

        if load:
            self.loc_data = local.LocalData(base_dir=data_dir)

        if ou_id:
            if type(ou_id) == str:
                if load:
                    ou_data = self.loc_data.get_data( self.ou_id )
                    self.ou_data = data.DataSet( self.ou_id, data=ou_data )
                else:
                    ou_data = export.get_ou( self.ou_id )
                    self.ou_data = data.DataSet( self.ou_id, data=ou_data )
            elif type(ou_id) == list:
                self.ou_data = []
                if load:
                    for idx in ou_id:
                        ou_data = self.loc_data.get_data(idx)
                        self.ou_data.append(data.DataSet(idx,data=ou_data))
                else:
                    for idx in ou_id:
                        ou_data = export.get_ou(idx)
                        self.ou_data.append(data.DataSet(idx,data=ou_data))

        if ctx_id:
            if type(ctx_id) == str:
                if load:
                    ctx_data = self.loc_data.get_data( self.ctx_id )
                    self.ctx_data = data.DataSet( self.ctx_id, data=ctx_data )
                else:
                    ctx_data = export.get_ctx( self.ctx_id )
                    self.ctx_data = data.DataSet( self.ctx_id, data=ctx_data )
            elif type(ctx_id) == list:
                self.ctx_data = []
                if load:
                    for idx in ctx_id:
                        ctx_data = self.loc_data.get_data(idx)
                        self.ctx_data.append(data.DataSet(idx,data=ctx_data))
                else:
                    for idx in ctx_id:
                        ctx_data = export.get_ctx(idx)
                        self.ctx_data.append(data.DataSet(idx,data=ctx_data))

        # self.ou_creators = self.ou_data.get_creators()

    def save_data(self, data_set):
        self.loc_data.store_data_local(data_set.idx, data_set.collection)
        # self.data_set.store_data()
