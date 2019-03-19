# from pybman import rest

class Inspector:

    def __init__(self, records):
        self.records = records

    def check_publication_titles(self, clean=False):
        updates = {}
        for record in self.records:
            publication_title = record['data']['metadata']['title']
            if publication_title != publication_title.strip():
                item_id = record['data']['objectId']
                if clean:
                    record['data']['metadata']['title'] = publication_title.strip()
                updates[item_id] = record
        return updates

    def check_source_titles(self, clean=False):
        updates = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['title'] != source['title'].strip():
                        item_id = record['data']['objectId']
                        if clean:
                            source['title'] = source['title'].strip()
                        updates[item_id] = record
        return updates

    def check_publishers(self, clean=False):
        updates = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'publisher' in record['data']['metadata']['publishingInfo']:
                    publisher = record['data']['metadata']['publishingInfo']['publisher']
                    if publisher != publisher.strip():
                        item_id = record['data']['objectId']
                        if clean:
                            record['data']['metadata']['publishingInfo']['publisher'] = publisher.strip()
                        updates[item_id] = record
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'publisher' in source['publishingInfo']:
                            publisher = source['publishingInfo']['publisher']
                            if publisher != publisher.strip():
                                item_id = record['data']['objectId']
                                if clean:
                                    source['publishingInfo']['publisher'] = publisher.strip()
                                updates[item_id] = record
        return updates

    def check_publishing_places(self, clean=False):
        updates = {}
        for record in self.records:
            if 'publishingInfo' in record['data']['metadata']:
                if 'place' in record['data']['metadata']['publishingInfo']:
                    place = record['data']['metadata']['publishingInfo']['place']
                    if place != place.strip():
                        item_id = record['data']['objectId']
                        if clean:
                            record['data']['metadata']['publishingInfo']['place'] = place.strip()
                        updates[item_id] = record
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if 'publishingInfo' in source:
                        if 'place' in source['publishingInfo']:
                            place = source['publishingInfo']['place']
                            if place != place.strip():
                                item_id = record['data']['objectId']
                                if clean:
                                    source['publishingInfo']['place'] = place.strip()
                                updates[item_id] = record
        return updates

    # @staticmethod
    # def clean_publication_titles(records):
    #    for k in records:
    #        publication = records[k]
    #        dirty_title = publication['data']['metadata']['title']
    #        publication['data']['metadata']['title'] = dirty_title.strip()
    #    return records

    def check_publication_date(self):
        # dateAccepted
        # dateCreated
        # dateModified
        # datePublishedInPrint
        # datePublishedOnline
        # dateSubmitted
        pass

    def check_publication_link(self):
        updates = {}
        for record in self.records:
            if 'identifiers' in record['data']['metadata']:
                identifiers = record['data']['metadata']['identifiers']
                for idx in identifiers:
                    if idx['type'] == URI:
                        item_id = record['data']['objectId']
                        updates[item_id] = record
        return updates
