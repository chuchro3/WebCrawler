from urllib.request import Request, urlopen, HTTPError
import os
import json

def extract_key(elem, key):
    '''
    Attempts to extract the object at the given key from the nested json document
    Assuming nesting is done by dict/list objects
    
    Input:
        elem: start of nested json document
        key: target key to find
    Returns:
        elem[key] if found
        None if key does not exist
    '''
    if isinstance(elem, dict):
        if key in elem:
            return elem[key]
        for k in elem:
            item = extract_key(elem[k], key)
            if item is not None:
                return item
    elif isinstance(elem, list):
        for k in elem:
            item = extract_key(k, key)
            if item is not None:
                return item
    return None


def extract_all_keys(elem, key):
    '''
    Same as extract_key(), but creates a generator using yield to extract multiple occurences of key
    
    Input:
        elem: start of nested json document
        key: target key to find
    Returns:
        Generator representing all occurences of elem[key]
    '''
    if hasattr(elem,'items'):
        for k, v in elem.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in extract_all_keys(v, key):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in extract_all_keys(d, key):
                        yield result


def get_request_to_dic(link, verbose=False):
    '''
    Input: 
        link: URL as string

    Returns: 
        dictionary of json response
    '''
    req = Request(link)

    #get json info from url
    req.add_header("Accept", "application/json,application/xml")

    if verbose:
        print(link)
    try:
        raw_page = urlopen(req).read().decode()
        page_dic = json.loads(raw_page)
    except HTTPError as err:
        if verbose:
            print("HTTPError", err.code)
            page_dic = {}
    return page_dic


def write_to_file(name, content, dest_dir):
    json_str = json.dumps(content)
    file_name = dest_dir+"/"+name+".json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    f = open(file_name, "w")
    f.write(json_str)
    f.close()
