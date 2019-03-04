class Inspector:

    def __init__(self, records):
        self.records = records

    def check_publication_titles(self):
        updates = {}
        for record in self.records:
            publication_title = record['data']['metadata']['title']
            if publication_title != publication_title.strip():
                item_id = record['data']['objectId']
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
