from pybman import data
# from pybman import local
from pybman import query
from pybman import rest
from pybman import inspector
# from pybman import utils


class Client:

    def __init__(self, secret='./conf/secret.json'):

        # load rest api controllers
        self.item_rest = rest.ItemRestController(secret)
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
        self.lang_query = query.LangQuery()

        # inspector class
        self.inspector = None

    def get_data(self, ctx_id=None, ou_id=None, pers_id=None, lang_id=None):
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

    def clean_init(self, data_set):
        self.inspector = inspector.Inspector(data_set.records)

    def clean_titles(self, data_set=None):

        print("start cleaning title data!")

        # create new inspector instance
        if data_set:
            self.clean_init(data_set)
        else:
            print("failed to initialize inspector!")
            print("please pass data to be cleaned.")
            return 0

        # cleaning of publication titles
        clean_data = self.inspector.check_publication_titles(clean=True)
        total = 0
        if clean_data:
            for k in clean_data:
                updated = self.update_data(k, clean_data[k]['data'], 'auto-update: publication title stripped')
                if updated:
                    total += 1
            print("updated", total, "publication titles!")
        else:
            print("publication title data is already clean!")
            print("nothing to do...")

        return total

    def clean_source_titles(self, data_set=None):

        print("start cleaning source title data!")

        # create new inspector instance
        if data_set:
            self.clean_init(data_set)
        else:
            print("failed to initialize inspector!")
            print("please pass data to be cleaned.")
            return 0

        # cleaning of source title data
        clean_data = self.inspector.check_source_titles(clean=True)
        total = 0
        if clean_data:
            for k in clean_data:
                updated = self.update_data(k, clean_data[k]['data'], 'auto-update: source title stripped')
                if updated:
                    total += 1
            print("updated", total, "source titles!")
        else:
            print("source title data is already clean!")
            print("nothing to do...")

        return total

    def clean_publishers(self, data_set=None):

        print("start cleaning publisher data!")

        # create new inspector instance
        if data_set:
            self.clean_init(data_set)
        else:
            print("failed to initialize inspector!")
            print("please pass data to be cleaned.")
            return 0

        # cleaning of publisher data
        clean_data = self.inspector.check_publishers(clean=True)
        total = 0
        if clean_data:
            for k in clean_data:
                updated = self.update_data(k, clean_data[k]['data'], 'auto-update: publisher stripped')
                if updated:
                    total += 1
        else:
            print("publisher data is already clean!")
            print("nothing to do...")

        print("updated", total, "items!")
        return total

    def clean_publishing_places(self, data_set=None):

        print("start cleaning publishing place data!")

        # create new inspector instance
        if data_set:
            self.clean_init(data_set)
        else:
            print("failed to initialize inspector!")
            print("please pass data to be cleaned.")
            return 0

        # start cleaning of publishing place data
        clean_data = self.inspector.check_publishing_places(clean=True)
        total = 0
        if clean_data:
            for k in clean_data:
                updated = self.update_data(k, clean_data[k]['data'], 'auto-update: publishing place stripped')
                if updated:
                    total += 1
        else:
            print("publishing place data is already clean!")
            print("nothing to do...")

        print("updated", total, "items!")
        return total
