from pybman import local
from pybman import export

class DataSet:

    def __init__(self, data_id, data=None, raw=None):

        self.idx = data_id

        if raw:
            self.collection = {"numberOfRecords": len(raw), "records": raw}
            self.num = len(raw)
            self.records = raw
            self.persons = self.get_cone_persons()

        elif data:
            self.collection = data
            self.num = len(data['records'])
            self.records = data['records']
            self.persons = self.get_cone_persons()

        else:
            print("please pass (raw) data for initialization!")
            self.collection = None
            self.num = 0
            self.records = []
            self.persons = {}
            # self.creators = []

    # get creators of items
    def get_creators(self):
        creators = []
        for record in self.records:
            if 'creators' in record['data']['metadata']:
                creators_list = record['data']['metadata']['creators']
                for creator in creators_list:
                    creators.append(creator)
        return creators

    def get_cone_persons(self):
        persons = {}
        for creator in self.get_creators():
            if creator['type'] == 'PERSON':
                if 'identifier' in creator['person']:
                    if creator['person']['identifier']['type'] == 'CONE':
                        if creator['person']['identifier']['id'] not in persons:
                            cone_id = creator['person']['identifier']['id']
                            if 'givenName' in creator['person']:
                                name = creator['person']['givenName']
                                if 'familyName' in creator['person']:
                                    name += ' ' + creator['person']['familyName']
                            else:
                                if 'familyName' in creator['person']:
                                    name = creator['person']['familyName']
                                else:
                                    print('no name found for', cone_id)
                                    name = ''
                            persons[cone_id] = name
        return persons

    def init_pers_data(self):
        pers_data = []
        for p in self.persons:
            p_data = export.get_pers(p)
            p_idx = p.split('/')[-1]
            pers_data.append(DataSet(p_idx,data=p_data))
        return pers_data

    # get titles of items
    def get_titles(self):
        titles = []
        for record in self.records:
            titles.append(record['data']['metadata']['title'])
        return titles

    # get titles from source of items
    def get_titles_from_source(self):
        source_titles = []
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    source_titles.append(source['title'])
        return source_titles

    # get list of genres from collection
    def get_genres(self):
        genres = []
        for record in self.records:
            if record['data']['metadata']['genre'] not in genres:
                genres.append(record['data']['metadata']['genre'])
        return genres

    # get publication places of items
    def get_places(self):
        places = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'place' in record['data']['metadata']['publishingInfo']:
                    place = record['data']['metadata']['publishingInfo']['place']
                    if place in places:
                        places[place].append(record['data']['objectId'])
                    else:
                        places[place] = [record['data']['objectId']]
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'place' in source['publishingInfo']:
                            place = source['publishingInfo']['place']
                            if place in places:
                                places[place].append(record['data']['objectId'])
                            else:
                                places[place] = [record['data']['objectId']]
        return places

    # get publishers of items
    def get_publishers(self):
        publishers = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'publisher' in record['data']['metadata']['publishingInfo']:
                    publisher = record['data']['metadata']['publishingInfo']['publisher']
                    if publisher in publishers:
                        publishers[publisher].append(record['data']['objectId'])
                    else:
                        publishers[publisher] = [record['data']['objectId']]
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'publisher' in source['publishingInfo']:
                            publisher = source['publishingInfo']['publisher']
                            if publisher in publishers:
                                publishers[publisher].append(record['data']['objectId'])
                            else:
                                publishers[publisher] = [record['data']['objectId']]
        return publishers

    def get_years(self):
        years = {}
        for record in self.records:
            if 'datePublishedInPrint' in record['data']['metadata']:
                year = record['data']['metadata']['datePublishedInPrint'].split("-")[0]
                if year in years:
                    years[year].append(record['data']['objectId'])
                else:
                    years[year] = [record['data']['objectId']]
            elif 'datePublishedOnline' in record['data']['metadata']:
                year = record['data']['metadata']['datePublishedOnline'].split("-")[0]
                if year in years:
                    years[year].append(record['data']['objectId'])
                else:
                    years[year] = [record['data']['objectId']]
            else:
                print("no publicatiion date found for", record['data']['objectId'])
        return years

    def get_years_data(self):
        years = {}
        for record in self.records:
            if 'datePublishedInPrint' in record['data']['metadata']:
                year = record['data']['metadata']['datePublishedInPrint'].split("-")[0]
                if year in years:
                    years[year].append(record['data'])
                else:
                    years[year] = [record['data']]
            elif 'datePublishedOnline' in record['data']['metadata']:
                year = record['data']['metadata']['datePublishedOnline'].split("-")[0]
                if year in years:
                    years[year].append(record['data'])
                else:
                    years[year] = [record['data']]
            else:
                print("no publication date found for", record['data']['objectId'])
        return years

    def get_languages(self):
        pass

    # get identifiers from sources of items
    def get_sources_identifiers(self):
        source_idx = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'identifiers' in source:
                        for identifier in source['identifiers']:
                            identifier_type = identifier['type']
                            if identifier_type in source_idx:
                                source_idx[identifier_type].append(record['data']['objectId'])
                            else:
                                source_idx[identifier_type] = [record['data']['objectId']]
        return source_idx

    # get items with state 'submitted'
    def get_items_submitted(self):
        submitted = {}
        for record in self.records:
            if record['data']['publicState'] == 'SUBMITTED':
                if record['data']['versionState'] == 'SUBMITTED':
                    submitted[record['persistenceId']] = record['data']
        return submitted

    # get item from collection by given id
    def get_item(self, item_id):
        item = {}
        for record in self.records:
            if item_id == record['data']['objectId']:
                item = record
                break
        return item

    # get items from collection with given genre
    def get_items_with_genre(self, genre):
        records = {}
        for record in self.records:
            if genre == record['data']['metadata']['genre']:
                records[record['data']['objectId']] = record['data']['metadata']
        return records

    def get_items_with_publication_year(self, year):
        # dateAccepted
        # dateCreated
        # dateModified
        # datePublishedInPrint
        # datePublishedOnline
        # dateSubmitted
        pass

    # get items from collection with given source genre
    def get_items_with_source_genre(self, source_genre):
        records = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source_genre == source['genre']:
                        records[record['data']['objectId']] = source
        return records

    def save_titles(self):
        # titles = self.get_titles()
        pass
