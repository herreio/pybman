from pybman import data
from pybman import query
from pybman import rest


class Client:

    def __init__(self, secret=''):

        # load rest api controllers
        self.item_rest = rest.ItemRestController(secret)
        self.ou_rest = rest.OrgUnitRestController()
        self.ctx_rest = rest.ContextRestController()
        self.feed_rest = rest.FeedRestController()

        # load cone controllers
        self.journals_cone = rest.JournalConeController()
        self.persons_cone = rest.PersonConeController()
        self.lang_cone = rest.LanguageConeController()

        # load classes providing search queries
        self.pers_query = query.PersQuery()
        self.ou_query = query.OrgUnitQuery()
        self.ctx_query = query.ContextQuery()
        self.lang_query = query.LangQuery()
        self.jour_query = query.JournalQuery()
        self.all_query = query.AllQuery()

        # inspector class
        self.inspector = None

    def get_data(self, ctx_id=None, ou_id=None, pers_id=None, lang_id=None, jour_name=None, misc_query=None):
        if ctx_id:
            ctx_query = self.ctx_query.get_item_query(ctx_id)
            self.item_rest.search_items(query=ctx_query)
            return data.DataSet(ctx_id, raw=self.item_rest.records)
        elif ou_id:
            ou_query = self.ou_query.get_item_query(ou_id)
            self.item_rest.search_items(query=ou_query)
            return data.DataSet(ou_id, raw=self.item_rest.records)
        elif pers_id:
            pers_query = self.pers_query.get_item_query(pers_id)
            self.item_rest.search_items(query=pers_query)
            return data.DataSet(pers_id, raw=self.item_rest.records)
        elif lang_id:
            lang_query = self.lang_query.get_item_query(lang_id)
            self.item_rest.search_items(query=lang_query)
            return data.DataSet(lang_id, raw=self.item_rest.records)
        elif jour_name:
            jour_query = self.jour_query.get_item_query(jour_name)
            self.item_rest.search_items(query=jour_query)
            return data.DataSet(jour_name, raw=self.item_rest.records)
        elif misc_query:
            self.item_rest.search_items(query=misc_query)
            return data.DataSet("query_data", raw=self.item_rest.records)
        else:
            print("please specify data to retrieve!")

    def update_data(self, idx, item_data, comment):
        updated_data = self.item_rest.update_item(idx, item_data)
        if updated_data:
            response = self.item_rest.release_item(idx, updated_data, comment)
            if response:
                print("successfully updated data with id", response['objectId'])
                return response
            else:
                print("something went wrong while releasing item with id", idx)
                return None
        else:
            print("something went wrong while updating item with id", idx)
            return None
