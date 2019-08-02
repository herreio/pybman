import re

from pybman import utils


class Inspector:

    def __init__(self, client, records):
        self.records = records
        self.client = client

    def check_publication_titles(self, clean=False):
        updates = {}
        for record in self.records:
            publication_title = record['data']['metadata']['title']
            if publication_title != utils.clean_string(publication_title):
                item_id = record['data']['objectId']
                if clean:
                    record['data']['metadata']['title'] = utils.clean_string(publication_title)
                updates[item_id] = record
        return updates

    def check_source_titles(self, clean=False):
        updates = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['title'] != utils.clean_string(source['title']):
                        item_id = record['data']['objectId']
                        if clean:
                            source['title'] = utils.clean_string(source['title'])
                        updates[item_id] = record
        return updates

    def check_publishers(self, clean=False):
        updates = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'publisher' in record['data']['metadata']['publishingInfo']:
                    publisher = record['data']['metadata']['publishingInfo']['publisher']
                    if publisher != utils.clean_string(publisher):
                        item_id = record['data']['objectId']
                        if clean:
                            record['data']['metadata']['publishingInfo']['publisher'] = utils.clean_string(publisher)
                        updates[item_id] = record
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'publisher' in source['publishingInfo']:
                            publisher = source['publishingInfo']['publisher']
                            if publisher != utils.clean_string(publisher):
                                item_id = record['data']['objectId']
                                if clean:
                                    source['publishingInfo']['publisher'] = utils.clean_string(publisher)
                                updates[item_id] = record
        return updates

    def check_publishers_omission(self, clean=False):
        et_al = re.compile(r"\s\[et\.? ?al\.?\]|\s\[u\.?\s?a\.?\]|\s\[etc\.?\]")
        updates = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'publisher' in record['data']['metadata']['publishingInfo']:
                    publisher = record['data']['metadata']['publishingInfo']['publisher']
                    if publisher != et_al.sub("", publisher):
                        item_id = record['data']['objectId']
                        if clean:
                            record['data']['metadata']['publishingInfo']['publisher'] = et_al.sub("", publisher)
                        updates[item_id] = record
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'publisher' in source['publishingInfo']:
                            publisher = source['publishingInfo']['publisher']
                            if publisher != et_al.sub("", publisher):
                                item_id = record['data']['objectId']
                                if clean:
                                    source['publishingInfo']['publisher'] = et_al.sub("", publisher)
                                updates[item_id] = record
        return updates

    def check_publishing_places(self, clean=False):
        updates = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'place' in record['data']['metadata']['publishingInfo']:
                    place = record['data']['metadata']['publishingInfo']['place']
                    if place != utils.clean_string(place):
                        item_id = record['data']['objectId']
                        if clean:
                            record['data']['metadata']['publishingInfo']['place'] = utils.clean_string(place)
                        updates[item_id] = record
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'place' in source['publishingInfo']:
                            place = source['publishingInfo']['place']
                            if place != utils.clean_string(place):
                                item_id = record['data']['objectId']
                                if clean:
                                    source['publishingInfo']['place'] = utils.clean_string(place)
                                updates[item_id] = record
        return updates

    def check_publishing_places_omission(self, clean=False):
        et_al = re.compile(r"\s\[et\.? ?al\.?\]|\s\[u\.?\s?a\.?\]|\s\[etc\.?\]")
        updates = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'place' in record['data']['metadata']['publishingInfo']:
                    place = record['data']['metadata']['publishingInfo']['place']
                    if place != et_al.sub("", place):
                        item_id = record['data']['objectId']
                        if clean:
                            record['data']['metadata']['publishingInfo']['place'] = et_al.sub("", place)
                        updates[item_id] = record
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'place' in source['publishingInfo']:
                            place = source['publishingInfo']['place']
                            if place != et_al.sub("", place):
                                item_id = record['data']['objectId']
                                if clean:
                                    source['publishingInfo']['place'] = et_al.sub("", place)
                                updates[item_id] = record
        return updates

    def check_publication_date(self):
        # dateAccepted
        # dateCreated
        # dateModified
        # datePublishedInPrint
        # datePublishedOnline
        # dateSubmitted
        pass

    def check_publication_uri(self):
        # was ist wenn zwei uri's auftauchen? eine geht, eine nicht, beide gehen?
        updates = {}
        for record in self.records:
            if 'identifiers' in record['data']['metadata']:
                identifiers = record['data']['metadata']['identifiers']
                for idx in identifiers:
                    if idx['type'] == 'URI':
                        url = idx['id']
                        if not utils.url_exists(url):
                            item_id = record['data']['objectId']
                            updates[item_id] = url
        return updates

    def check_publication_url(self):
        updates = {}
        for record in self.records:
            if 'files' in record['data']:
                for f in record['data']['files']:
                    if f['storage'] == 'EXTERNAL_URL':
                        url = f['content']
                        # check = utils.check_url(url)
                        # if url != check:
                        #    item_id = record['data']['objectId']
                        #    updates[item_id] = check
                        if not utils.url_exists(url):
                            item_id = record['data']['objectId']
                            updates[item_id] = url
                        # if 'name' in f:
                        #    url = f['name']
                        #    if not utils.url_exists(url):
                        #        item_id = record['data']['objectId']
                        #        updates[item_id] = url
                        # else:
                        #    print("")
                        #    print("no name given for", record['data']['objectId'])
                        #    print(record['data']['files'])
                        #    print("")
        return updates

    def change_genre(self, new_genre, old_genre):
        updates = {}
        for record in self.records:
            if old_genre == record['data']['metadata']['genre']:
                record['data']['metadata']['genre'] = new_genre
                updates[record['data']['objectId']] = record
            else:
                print("skipping item", record['data']['objectId'])
        return updates

    def change_source_genre(self, new_genre, old_genre):
        updates = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                sources = record['data']['metadata']['sources']
                found = False
                for source in sources:
                    if source['genre'] == old_genre:
                        source['genre'] = new_genre
                        updates[record['data']['objectId']] = record
                        found = True
                        break
                if not found:
                    print("skipping item", record['data']['objectId'])
            else:
                print("skipping item", record['data']['objectId'], "without sources!")
        return updates

    def change_pers_name(self, old_family_name=None, new_family_name=None, old_given_name=None, new_given_name=None):
        updates = {}
        if old_family_name and new_family_name:
            for record in self.records:
                creators = record['data']['metadata']['creators']
                for creator in creators:
                    if creator['type'] == 'PERSON':
                        if creator['person']['familyName'] == old_family_name:
                            creator['person']['familyName'] = new_family_name
                            updates[record['data']['objectId']] = record
            return updates

        elif old_given_name and new_given_name:
            for record in self.records:
                creators = record['data']['metadata']['creators']
                for creator in creators:
                    if creator['type'] == 'PERSON':
                        if creator['person']['givenName'] == old_given_name:
                            creator['person']['givenName'] = new_given_name
                            updates[record['data']['objectId']] = record
            return updates

        else:
            print("please pass either new and old family name or given name!")
            return updates

    def update_genre(self, new_genre, old_genre):

        print("start changing genre from", old_genre, "to", new_genre)

        clean_data = self.change_genre(new_genre, old_genre)
        total = 0
        if clean_data:
            comment = 'auto-update: change genre of item from ' + old_genre + " to " + new_genre
            for k in clean_data:
                updated = self.client.update_data(k, clean_data[k]['data'], comment)
                if updated:
                    total += 1
            print("updated genre of", total, "items!")
        else:
            print("genre is correctly chosen already!")
            print("nothing to do...")
            return 0

    def update_source_genre(self, new_genre, old_genre):

        print("start changing source genre from", old_genre, "to", new_genre)

        clean_data = self.change_source_genre(new_genre, old_genre)
        total = 0
        if clean_data:
            comment = 'auto-update: change source genre of item from ' + old_genre + " to " + new_genre
            for k in clean_data:
                updated = self.client.update_data(k, clean_data[k]['data'], comment)
                if updated:
                    total += 1
            print("updated genre of", total, "items!")
        else:
            print("source genre is correctly chosen already!")
            print("nothing to do...")
            return 0

    def clean_titles(self):

        print("start cleaning title data!")

        clean_data = self.check_publication_titles(clean=True)
        total = 0
        if clean_data:
            comment = 'auto-update: publication title stripped'
            for k in clean_data:
                updated = self.client.update_data(k, clean_data[k]['data'], comment)
                if updated:
                    total += 1
            print("updated", total, "publication titles!")
        else:
            print("publication title data is already clean!")
            print("nothing to do...")

        return total

    def clean_source_titles(self):

        print("start cleaning source titles!")

        clean_data = self.check_source_titles(clean=True)
        total = 0
        if clean_data:
            comment = 'auto-update: source title stripped'
            for k in clean_data:
                updated = self.client.update_data(k, clean_data[k]['data'], comment)
                if updated:
                    total += 1
            print("updated", total, "source titles!")
        else:
            print("source title data is already clean!")
            print("nothing to do...")

        return total

    def clean_publishers(self):

        print("start cleaning publisher data!")

        clean_data = self.check_publishers(clean=True)
        total = 0
        if clean_data:
            comment = 'auto-update: remove control characters from publisher value'
            for k in clean_data:
                updated = self.client.update_data(k, clean_data[k]['data'], comment)
                if updated:
                    total += 1
        else:
            print("publisher data is already clean!")
            print("nothing to do...")

        print("updated", total, "items!")
        return total

    def clean_publishing_places(self):

        print("start cleaning publishing place data!")

        clean_data = self.check_publishing_places(clean=True)
        total = 0
        if clean_data:
            comment = 'auto-update: remove control characters from publishing place value'
            for k in clean_data:
                updated = self.client.update_data(k, clean_data[k]['data'], comment)
                if updated:
                    total += 1
        else:
            print("publishing place data is already clean!")
            print("nothing to do...")

        print("updated", total, "items!")
        return total
