"""
data extraction routines
"""

def value_from_level(field, level):
    """
    extract value from field in level of item
    """
    return level[field] if field in level else ""

def list_from_level(field, level):
    """
    extract list from field in level of item
    """
    return level[field] if field in level else []

def field_in_level(field, level):
    """
    true if field is in level, false otherwise
    """
    return True if field in level else False

def iter_fields(field, level):
    """
    iterate over field of level
    """
    if field_in_level(field,level):
        for field in level[field]:
            yield(field)
    else:
        []

def data(item):
    """
    extract data of item
    """
    return item['data']

def metadata(item):
    """
    extract meta data of item
    """
    return data(item)['metadata']

def idx_from_item(item):
    """
    extract identifier of item
    """
    return data(item)['objectId']

def ctx_from_item(item):
    """
    extract identifier of item
    """
    return data(item)['context']

def ctx_idx_from_item(item):
    """
    extract identifier of item
    """
    return ctx_from_item(item)['objectId']

def title_from_item(item):
    """
    extract title of item
    """
    return metadata(item)['title']

def genre_from_item(item):
    """
    extract genre of item
    """
    return metadata(item)['genre']

def creators_from_item(item):
    """
    extract creators of item
    """
    return metadata(item)['creators']

def type_from_creator(creator):
    """
    extract type of creator
    """
    pass

def field_from_creator(field, creator):
    """
    extract field from creator of item
    """
    return value_from_level(field, creator)

def persons_from_item(item):
    """
    extract persons from item
    """
    return [creator for creator in creators_from_item(item)\
    if value_from_level('person', creator)]

def persons_name_from_creator(creator):
    """
    exract persons’ name from creator of item
    """
    return (value_from_level('givenName',creator['person']),
            value_from_level('familyName',creator['person']))

def persons_identifier_from_creator(creator):
    """
    exract persons’ identifier from creator of item
    """
    return value_from_level('identifier',creator['person'])

def persons_id_from_creator(creator):
    """
    exract persons’ ID and type of ID from creator of item
    """
    pers_id = persons_identifier_from_creator(creator)
    return value_from_level('id',pers_id).split("/")[-1],\
           value_from_level('type',pers_id)

def persons_organizations_from_creator(creator):
    """
    exract persons’ organizations from creator of item
    """
    return list_from_level('organizations',creator['person'])

def persons_affiliation_from_creator(creator):
    """
    exract persons’ affiliations from creator of item
    """
    organizations = persons_organizations_from_creator(creator)
    return [(value_from_level('identifier',organization),\
           value_from_level('identifierPath',organization),\
           value_from_level('name',organization),\
           value_from_level('address',organization)) for organization in organizations]

def role_from_creator(creator):
    """
    extract role from creator of item
    """
    return value_from_level('role',creator)

def organizations_from_item(item):
    """
    extract organizations from item
    """
    return [creator for creator in creators_from_item(item)\
    if field_from_creator('organization', creator)]

def organizations_name_from_creator(creator):
    """
    extract organizations’ names from item
    """
    return value_from_level('name',creator['organization'])

def organizations_identifier_from_creator(creator):
    """
    extract organizations’ identifiers from item
    """
    return value_from_level('identifier',creator['organization'])

def field_from_metadata(field, item, value=True):
    """
    extract field from metadata of item
    """
    if value:
        return value_from_level(field, metadata(item))
    else:
        return list_from_level(field, metadata(item))

def languages_from_items(item):
    """
    extract languages of item
    """
    return field_from_metadata('languages',item,value=False)

def identifers_from_item(item):
    """
    extract values and types of identifiers
    """
    result = []
    if field_in_level('identifiers',metadata(item)):
        for idx in iter_fields('identifiers',metadata(item)):
            result.append((value_from_level('type', idx),
                           value_from_level('id', idx)))
    else:
        result.append(("",""))
    return result

def pubinfo_from_item(item):
    """
    extract publishing info of item
    """
    return field_from_metadata('publishingInfo', item)

def field_from_pubinfo(field, item):
    """
    extract field from publishing info of item
    """
    if field_in_level(field,pubinfo_from_item(item)):
        return pubinfo_from_item(item)[field]
    else:
        ""

def place_from_item(item):
    """
    extract publishing place of item
    """
    return field_from_pubinfo('place', item)

def publisher_from_item(item):
    """
    extract publisher from item
    """
    return field_from_pubinfo('publisher', item)

def date_pubprint_from_item(item):
    """
    extract publication date (print) from item
    """
    return field_from_metadata('datePublishedInPrint', item)

def date_pubonline_from_item(item):
    """
    extract publication date (online) from item
    """
    return field_from_metadata('datePublishedOnline', item)

def date_modified_from_item(item):
    """
    extract date of modification from item
    """
    return field_from_metadata('dateModified', item)

def date_accepted_from_item(item):
    """
    extract date of acceptance from item
    """
    return field_from_metadata('dateAccepted', item)

def date_submitted_from_item(item):
    """
    extract date of submission from item
    """
    return field_from_metadata('dateSubmitted', item)

def date_created_from_item(item):
    """
    extract date of creation from item
    """
    return field_from_metadata('dateCreated', item)

def date_from_item(item):
    """
    extract date from item
    """
    if date_pubprint_from_item(item):
        return date_pubprint_from_item(item)
    elif date_pubonline_from_item(item):
        return date_pubonline_from_item(item)
    elif date_modified_from_item(item):
        return date_modified_from_item(item)
    elif date_accepted_from_item(item):
        return date_accepted_from_item(item)
    elif date_submitted_from_item(item):
        return date_submitted_from_item(item)
    elif date_created_from_item(item):
        return date_created_from_item(item)
    else:
        return ''

def sources(item):
    """
    iterate over sources of item
    """
    if field_in_level('sources',metadata(item)):
        for source in metadata(item)['sources']:
            yield(source)
    else:
        []

def sources_titles_from_item(item):
    """
    extract sources’ titles from item
    """
    return [value_from_level('title',source) for source in sources(item)]

def sources_titles_genres_from_item(item):
    """
    extract sources’ titles and genres from item
    """
    return [(value_from_level('title',source),
             value_from_level('genre',source))
             for source in sources(item)]

def creators_from_source(source):
    """
    extract sources’ titles and genres from item
    """
    return list_from_level('creators',source)

def sources_persons_from_item(item):
    """
    extract sources’ creators from item if person
    """
    result = []
    for source in sources(item):
        source_persons = []
        if field_in_level('creators', source):
            for creator in creators_from_source(source):
                if field_in_level('person',creator):
                    source_persons.append(creator)
        result.append(source_persons)
    return result

def sources_persons_id_from_item(item):
    """
    extract persons ID from source of item
    """
    result = []
    for source in sources_persons_from_item(item):
        s = []
        for person in source:
            pers_name = persons_name_from_creator(person)
            pers_role = role_from_creator(person)
            pers_id, pers_id_type = persons_id_from_creator(person)
            s.append( (pers_id,
                       pers_name[0],
                       pers_name[1],
                       pers_role,
                       pers_id_type) )
            #persons_affiliation_from_creator(person)
        result.append(s)
    return result

def sources_persons_affiliations_from_item(item):
    """
    extract persons affilations from source of item
    """
    result = []
    for source in sources_persons_from_item(item):
        s = []
        for person in source:
            s.append(persons_affiliation_from_creator(person))
        result.append(s)
    return result

def sources_identifiers_from_item(item):
    """
    extract values and types of identifiers from item’s sources
    """
    result = []
    for source in sources(item):
        if field_in_level('identifiers',source):
            result.append([(value_from_level('type', idx), value_from_level('id', idx))\
            for idx in iter_fields('identifiers',source)])
        else:
            result.append([("","")])
    return result

def items(records):
    """
    iterate items
    """
    for record in records:
        yield(record)
    else:
        []

def titles_from_records(records):
    """
    extract titles from records
    """
    return [title_from_item(item) for item in items(records)]

def source_titles(collection):
    """
    extract source titles from records
    """
    result = []
    for item in items(collection):
        for source_title in sources_titles_from_item(item):
            if source_title:
                result.append(source_title)
    return result

def source_titles_genres(collection):
    """
    extract source titles and genres from records
    """
    result = []
    for item in items(collection):
        for source_title_genre in sources_titles_genres_from_item(item):
            result.append(source_title_genre)
    return result
