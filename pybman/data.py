from pybman import extract

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
            self.collection = {}
            self.num = 0
            self.records = []
            self.persons = {}

    def get_creators(self):
        """
        extract data of creators from records
        """
        creators = []
        for record in self.records:
            if 'creators' in record['data']['metadata']:
                creators_list = record['data']['metadata']['creators']
                for creator in creators_list:
                    creators.append(creator)
        return creators

    def get_creators_from_records(self):
        """
        extract creators lists from records
        """
        creators = []
        for record in self.records:
            if 'creators' in record['data']['metadata']:
                creators.append(record['data']['metadata']['creators'])
        return creators

    def get_creators_data(self):
        """
        extract persons’ CoNE IDs and associated records
        """
        creators = {}
        for record in self.records:
            if 'creators' in record['data']['metadata']:
                creators_list = record['data']['metadata']['creators']
                found = False
                for creator in creators_list:
                    if 'person' in creator:
                        found = True
                        if 'identifier' in creator['person']:
                            idx = creator['person']['identifier']['id'].split("/")[-1]
                            if idx in creators:
                                creators[idx].append(record)
                            else:
                                creators[idx] = [record]
                        else:
                            continue
                if not found:
                    print("no person found for", record['data']['objectId'])
        return creators

    def get_cone_persons(self):
        """
        extract persons’ CoNE IDs and associated names
        """
        persons = {}
        for creator in self.get_creators():
            if creator['type'] == 'PERSON':
                if 'identifier' in creator['person']:
                    if creator['person']['identifier']['type'] == 'CONE':
                        if creator['person']['identifier']['id'] not in persons:
                            cone_id = creator['person']['identifier']['id'].split("/")[-1]
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

    def get_organizations(self):
        """
        extract organizations of creators and associated IDs of records
        """
        organizations = {}
        for record in self.records:
            if 'creators' in record['data']['metadata']:
                creators_list = record['data']['metadata']['creators']
                for creator in creators_list:
                    if creator['type'] == 'PERSON':
                        person = creator['person']
                        if 'organizations' in person:
                            for organization in person['organizations']:
                                if organization['name'] in organizations:
                                    organizations[organization['name']].append(record['data']['objectId'])
                                else:
                                    organizations[organization['name']] = [record['data']['objectId']]
                    elif creator['type'] == 'ORGANIZATION':
                        organization = creator['organization']
                        if organization['name'] in organizations:
                            organizations[organization['name']].append(record['data']['objectId'])
                        else:
                            organizations[organization['name']] = [record['data']['objectId']]
                    else:
                        print("unknown creator type", creator['type'])
            else:
                print(record['data']['objectId'], "has no creator!")
        return organizations

    def get_titles(self):
        """
        extract titles and associated IDs of records
        """
        titles = {}
        for record in self.records:
            title = record['data']['metadata']['title']
            if title in titles:
                titles[title].append(record['data']['objectId'])
            else:
                titles[title] = [record['data']['objectId']]
        return titles

    def get_titles_from_source(self):
        """
        extract titles of sources and associated IDs of records
        """
        source_titles = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['title'] in source_titles:
                        source_titles[source['title']].append(record['data']['objectId'])
                    else:
                        source_titles[source['title']] = [record['data']['objectId']]
        return source_titles

    def get_genres(self):
        """
        extract genres and associated IDs of records
        """
        genres = {}
        for record in self.records:
            if record['data']['metadata']['genre'] in genres:
                genres[record['data']['metadata']['genre']].append(record['data']['objectId'])
            else:
                genres[record['data']['metadata']['genre']] = [record['data']['objectId']]
        return genres

    def get_genre_data(self):
        """
        extract genres and associated records
        """
        genres = {}
        for record in self.records:
            if record['data']['metadata']['genre'] in genres:
                genres[record['data']['metadata']['genre']].append(record)
            else:
                genres[record['data']['metadata']['genre']] = [record]
        return genres

    def get_genre_relationships(self):
        """
        extract genres and associated source genres
        """
        genres = {}
        for record in self.records:
            genre = record['data']['metadata']['genre']
            if genre not in genres:
                genres[genre] = {}
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['genre'] not in genres[genre]:
                        genres[genre][source['genre']] = []
                    genres[genre][source['genre']].append(record['data']['objectId'])
            else:
                if 'NONE' not in genres[genre]:
                    genres[genre]['NONE'] = []
                genres[genre]['NONE'].append(record['data']['objectId'])
        return genres

    def get_places(self):
        """
        extract publication places and associated IDs of records
        """
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

    def get_contexts(self):
        """
        extract IDs of records an associated IDs of collection
        """
        contexts = {}
        for record in self.records:
            item_idx = record['data']['objectId']
            ctx_idx = record['data']['context']['objectId']
            contexts[item_idx] = ctx_idx
        return contexts

    def get_publishers(self):
        """
        extract publishers and associated IDs of records
        """
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

    def get_journals(self):
        """
        extract publication sources from records with JOURNAL as source genre
        """
        journals = {}
        items = self.get_source_from_items_with_source_genre("JOURNAL")
        for k in items:
            if items[k]['title'] in journals:
                journals[items[k]['title']].append(k)
            else:
                journals[items[k]['title']] = [k]
        return journals

    def get_journals_data(self):
        """
        extract records with JOURNAL as source genre
        """
        journals = {}
        items = self.get_source_from_items_with_source_genre("JOURNAL")
        for k in items:
            if items[k]['title'] in journals:
                journals[items[k]['title']].append(self.get_item(k))
            else:
                journals[items[k]['title']] = [self.get_item(k)]
        return journals

    def get_series(self):
        """
        extract publication source from records with SERIES as source genre
        """
        series = {}
        items = self.get_source_from_items_with_source_genre("SERIES")
        for k in items:
            if items[k]['title'] in series:
                series[items[k]['title']].append(k)
            else:
                series[items[k]['title']] = [k]
        return series

    def get_years(self):
        """
        extract publication years and associated record IDs
        """
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
            elif 'dateModified' in record['data']['metadata']:
                year = record['data']['metadata']['dateModified'].split("-")[0]
                if year in years:
                    years[year].append(record['data']['objectId'])
                else:
                    years[year] = [record['data']['objectId']]
            elif 'dateAccepted' in record['data']['metadata']:
                year = record['data']['metadata']['dateAccepted'].split("-")[0]
                if year in years:
                    years[year].append(record['data']['objectId'])
                else:
                    years[year] = [record['data']['objectId']]
            elif 'dateSubmitted' in record['data']['metadata']:
                year = record['data']['metadata']['dateSubmitted'].split("-")[0]
                if year in years:
                    years[year].append(record['data']['objectId'])
                else:
                    years[year] = [record['data']['objectId']]
            elif 'dateCreated' in record['data']['metadata']:
                year = record['data']['metadata']['dateCreated'].split("-")[0]
                if year in years:
                    years[year].append(record['data']['objectId'])
                else:
                    years[year] = [record['data']['objectId']]
            else:
                print("no publication date found for", record['data']['objectId']+"!")
        return years

    def get_years_data(self):
        """
        extract publication years and associated records
        """
        years = {}
        for record in self.records:
            if 'datePublishedInPrint' in record['data']['metadata']:
                year = record['data']['metadata']['datePublishedInPrint'].split("-")[0]
                if year in years:
                    years[year].append(record)
                else:
                    years[year] = [record]
            elif 'datePublishedOnline' in record['data']['metadata']:
                year = record['data']['metadata']['datePublishedOnline'].split("-")[0]
                if year in years:
                    years[year].append(record)
                else:
                    years[year] = [record]
            elif 'dateModified' in record['data']['metadata']:
                year = record['data']['metadata']['dateModified'].split("-")[0]
                if year in years:
                    years[year].append(record)
                else:
                    years[year] = [record]
            elif 'dateAccepted' in record['data']['metadata']:
                year = record['data']['metadata']['dateAccepted'].split("-")[0]
                if year in years:
                    years[year].append(record)
                else:
                    years[year] = [record]
            elif 'dateSubmitted' in record['data']['metadata']:
                year = record['data']['metadata']['dateSubmitted'].split("-")[0]
                if year in years:
                    years[year].append(record)
                else:
                    years[year] = [record]
            elif 'dateCreated' in record['data']['metadata']:
                year = record['data']['metadata']['dateCreated'].split("-")[0]
                if year in years:
                    years[year].append(record)
                else:
                    years[year] = [record]
            else:
                print("no publication date found for", record['data']['objectId']+"!")
        return years

    def get_languages(self):
        """
        extract publication languages and associated record IDs
        """
        languages = {}
        for record in self.records:
            item_idx = extract.idx_from_item(record)
            if 'languages' in extract.metadata(record):
                langs = extract.languages_from_item(record)
                for lang in langs:
                    if lang in languages:
                        languages[lang].append(item_idx)
                    else:
                        languages[lang] = [item_idx]
            else:
                print(record['data']['objectId'], "has no language!")
                if 'NONE' in languages:
                    languages['NONE'].append(item_idx)
                else:
                    languages['NONE'] = [item_idx]
        return languages

    def get_languages_data(self):
        """
        extract publication languages and associated records
        """
        languages = {}
        for record in self.records:
            item_idx = extract.idx_from_item(record)
            if 'languages' in extract.metadata(record):
                langs = extract.languages_from_item(record)
                for lang in langs:
                    if lang in languages:
                        languages[lang].append(record)
                    else:
                        languages[lang] = [record]
            else:
                print(item_idx, "has no language!")
                if 'NONE' in languages:
                    languages['NONE'].append(item_idx)
                else:
                    languages['NONE'] = [item_idx]
        return languages

    def get_source_genres(self):
        """
        extract genres of publication sources and associated record IDs
        """
        genres = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['genre'] in genres:
                        genres[source['genre']].append(record['data']['objectId'])
                    else:
                        genres[source['genre']] = [record['data']['objectId']]
        return genres

    def get_source_genres_data(self):
        """
        extract genres of publication sources and associated records
        """
        genres = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source['genre'] in genres:
                        genres[source['genre']].append(record)
                    else:
                        genres[source['genre']] = [record]
        return genres

    def get_sources_identifiers(self):
        """
        extract identifers of publication sources and associated record IDs
        """
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

    def get_sources_titles(self):
        """
        extract titles of publication sources and associated record IDs
        """
        source_titles = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    title = source['title']
                    if title in source_titles:
                        source_titles[title].append(record['data']['objectId'])
                    else:
                        source_titles[title] = [record['data']['objectId']]
        return source_titles

    def get_item(self, item_id):
        """
        extract record with given record ID
        """
        item = {}
        for record in self.records:
            if item_id == record['data']['objectId']:
                item = record
                break
        return item

    # get items from collection with given genre
    def get_items_with_genre(self, genre):
        """
        extract IDs of records with state 'released' and associated records
        """
        records = {}
        for record in self.records:
            if genre == record['data']['metadata']['genre']:
                records[record['data']['objectId']] = record
        return records

    def get_items_released(self):
        """
        extract IDs of records with state 'released' and associated records
        """
        released = []
        for record in self.records:
            if record['data']['publicState'] == 'RELEASED':
                if record['data']['versionState'] == 'RELEASED':
                    released.append(record)
        return released

    # get items with state 'submitted'
    def get_items_submitted(self):
        """
        extract records with state 'submitted' and associated IDs
        """
        submitted = {}
        for record in self.records:
            if record['data']['publicState'] == 'SUBMITTED':
                if record['data']['versionState'] == 'SUBMITTED':
                    submitted[record['persistenceId']] = record['data']
        return submitted

    def get_items_from_year(self, year):
        """
        extract IDs of records with given publication year
        """
        years = self.get_years()
        if year in years:
            return years[year]
        else:
            return []

    def get_items_from_year_data(self, year):
        """
        extract records with given publication year
        """
        years = self.get_years_data()
        if year in years:
            return years[year]
        else:
            return []

    def get_items_with_external_url(self):
        """
        extract records with external url
        """
        records = {}
        for record in self.records:
            if 'files' in record['data']:
                for f in record['data']['files']:
                    if f['storage'] == 'EXTERNAL_URL':
                        records[record['data']['objectId']] = record
        return records

    def get_items_with_identifier_uri(self):
        """
        extract records with identifier uri
        """
        records = {}
        for record in self.records:
            if 'identifiers' in record['data']['metadata']:
                identifiers = record['data']['metadata']['identifiers']
                for idx in identifiers:
                    if idx['type'] == 'URI':
                        records[record['data']['objectId']] = record
        return records

    def get_items_with_source_genre(self, source_genre):
        """
        extract records with given source genre
        """
        records = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source_genre == source['genre']:
                        records[record['data']['objectId']] = record
        return records

    def get_source_from_items_with_source_genre(self, source_genre):
        """
        extract data of record’s source with given source genre
        """
        records = {}
        for record in self.records:
            if 'sources' in record['data']['metadata']:
                for source in record['data']['metadata']['sources']:
                    if source_genre == source['genre']:
                        records[record['data']['objectId']] = source
        return records
