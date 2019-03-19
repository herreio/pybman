from pybman import data
# from pybman import local
from pybman import query
from pybman import rest
from pybman import inspector
# from pybman import utils


class Client:

    def __init__(self, secret='./conf/secret.json'):

        # load rest api controllers
        self.item_rest = rest.ItemRestController()
        self.ou_rest = rest.OrgUnitRestController()
        self.ctx_rest = rest.ContextRestController()
        self.feed_rest = rest.FeedRestController()

        # load cone controllers
        self.journals_cone = rest.JournalConeController()
        self.persons_cone = rest.PersonConeController()

        # load classes providing search queries
        self.pers_query = query.PersQuery()
        self.ou_query = query.OrgUnitQuery()
        self.ctx_query = query.ContextQuery()

        # inspector class
        self.inspector = None

    def get_data(self,ctx_id=None,ou_id=None,pers_id=None,released=False):
        if ctx_id:
            query = self.ctx_query.get_item_query(ctx_id)
            self.item_rest.search_items(query=query)
            return data.DataSet(ctx_id, raw=self.item_rest.records)
        elif ou_id:
            query = self.ou_query.get_item_query()
            self.item_rest.search_items(query=query)
            return data.DataSet(ou_id, raw=self.item_rest.records)
        elif pers_id:
            query = self.pers_query.get_item_query(pers_id)
            self.item_rest.search_items(query=query)
            return data.DataSet(pers_id, raw=self.item_rest.records)
        else:
            print("please specify data to retrieve!")

    def update_data(self, idx, data, comment):
        updated_data = self.item_rest.update_item(idx, data)
        response = self.item_rest.release_item(idx, updated_data, 'auto-update: title stripped')
        print("successfully updated data with id", response['objectId'])

    def inspect_titles(self, data):
        print("starting title inspection!")
        # create inspector instance
        self.inspector = inspector.Inspector(data.records)
        ### inspect publication titles ###
        clean_data = self.inspector.check_publication_titles(clean=True)
        if clean_data:
            counter = 0
            for k in clean_data:
                self.update_data(k, clean_data[k]['data'], 'auto-update: publication title stripped')
                counter += 1
            print("updated", counter, "publication titles!")
            total += counter
        else:
            print("publication title data is already clean! nothing to do...")
        ### inspect source titles ###
        print("inspecting source titles:")
        clean_data = self.inspector.check_source_titles(clean=True)
        if clean_data:
            counter = 0
            for k in clean_data:
                self.update_data(k, clean_data[k]['data'], 'auto-update: source title stripped')
                counter += 1
            print("updated", counter, "source titles!")
            total += counter
        else:
            print("source title data is already clean! nothing to do...")
        print("updated", total, "items.")
