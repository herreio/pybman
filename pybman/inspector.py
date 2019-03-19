# from pybman import rest

class Inspector:

    def __init__(self, records):
        self.records = records

    def check_publication_titles(self, clean=False):
        updates = {}
        for record in self.records:
            item_id = record['data']['objectId']
            publication_title = record['data']['metadata']['title']
            if publication_title != publication_title.strip():
                if clean:
                    record['data']['metadata']['title'] = publication_title.strip()
                updates[item_id] = record
        return updates

    def check_source_titles(self, clean=False):
        updates = {}
        for record in self.records:
            item_id = record['data']['objectId']
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['title'] != source['title'].strip():
                        if clean:
                            source['title'] = source['title'].strip()
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
