import re
import json
import pathlib
import argparse

from typing import Generator, Optional

repo_dir = pathlib.Path(__file__).resolve().parent / "bilara-data"

def iter_json_files(target_dir, glob_pattern='**/[!_]*.json'):
    yield from sorted(target_dir.glob(f'[!_.]*/{glob_pattern}'), key=lambda f: humansortkey(str(f)))

def numericsortkey(string, _split=re.compile(r'(\d+)').split):
    # if re.fullmatch('\d+', s) then int(s) is valid, and vice-verca.
    return [int(s) if i % 2 else s for i, s in enumerate(_split(str(string)))]


def humansortkey(string, _split=re.compile(r'(\d+(?:[.-]\d+)*)').split):
    """
    >>> humansortkey('1.1') > humansortkey('1.0')
    True

    >>> humansortkey('1.0a') > humansortkey('1.0')
    True

    >>> humansortkey('1.0^a') > humansortkey('1.0')
    True
    """
    # With split, every second element will be the one in the capturing group.
    return [numericsortkey(s) if i % 2 else s
            for i, s in enumerate(_split(str(string)))]

def bilarasortkey(string):
    """
    >>> bilarasortkey('1.1') > bilarasortkey('1.0')
    True

    >>> bilarasortkey('1.0a') > bilarasortkey('1.0')
    True

    >>> bilarasortkey('1.0^a') < bilarasortkey('1.0')
    True
    """
    string = str(string)
    if string[-1].isalpha():
        string = f'{string[:-1]}.{ord(string[-1])}'
    subresult = humansortkey(string)

    result = []
    for i, obj in enumerate(subresult):
        if obj == '':
            obj = 0
        if isinstance(obj, str) and obj and obj[0] == '^':
                result.extend([-1, obj[1:]])
        else:
            result.append(obj)
    
    if isinstance(result[-1], list):
        result.append(0)
    return result


def print_name_if_needed(file, _seen=set()):
    if file not in _seen:
        print(file)
    _seen.add(file)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def json_load(file):
    try:
        with file.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.decoder.JSONDecodeError as e:
        lineno = e.lineno
        colno = e.colno
        with file.open('r') as f:
            lines = f.readlines()
        
        print('{}JSONDecodeError{}: {}'.format(bcolors.FAIL, bcolors.ENDC, file), file=sys.stderr)
        for i in range(lineno-2, lineno):
            if i >= 0:
                print(bcolors.OKGREEN+bcolors.BOLD, str(i).rjust(6), bcolors.ENDC, '  ', lines[i], sep='', end='', file=sys.stderr)
        print(' '*(colno + 7), '^', sep='', file=sys.stderr)
        print(bcolors.FAIL, e.msg, bcolors.ENDC, sep='', file=sys.stderr)


def muid_sort_key(string):
    if string.startswith('root'):
        return (0, string)
    elif string.startswith('translation'):
        return (1, string)
    elif string.startswith('markup'):
        return (2, string)
    else:
        return (3, string)

def print_html(file_uid_mapping):
    for uid, file_mapping in file_uid_mapping.items():
        # Get HTML
        if 'html' in file_mapping:
            html = json_load(file_mapping['html'])
        else:
            print('No HTML')
            exit(1)

        # Get Root
        if 'root-pli-ms' in file_mapping:
            print('Text:')
            root = json_load(file_mapping['root-pli-ms'])
        else:
            print('No Text')
            exit(1)

        # Write the result to the output file
        output_file_path = uid + '.html'
        print('Writing {}'.format(output_file_path))
        with open(output_file_path, 'w') as output_file:
            for segment_id, value in root.items():
                if (html[segment_id]):
                    output_file.write(html[segment_id].format(value) + '\n')
                else:
                    print('No HTML for {}'.format(segment_id))
                    output_file.write(value + '\n')


def yield_rows(muid_strings, file_uid_mapping):
    fields = ['segment_id'] + muid_strings
    yield fields

    field_mapping = {field:i for i, field in enumerate(fields)}
    
    for file_num, (uid, file_mapping) in enumerate(sorted(file_uid_mapping.items(), key=bilarasortkey)):
        data = {}
        segment_ids = set()
        for muid_string in muid_strings:
            if muid_string in file_mapping:
                file = file_mapping[muid_string]
                
                try:
                    file_data = json_load(file)
                except json.decoder.JSONDecodeError:
                    exit(1)
                
                i = field_mapping[muid_string]
                for segment_id, value in file_data.items():
                    if segment_id not in data:
                        data[segment_id] = [segment_id] + [''] * (len(fields) - 1)
                    data[segment_id][i] = value
        
        for segment_id in sorted(data.keys(), key=bilarasortkey):
            yield data[segment_id]
        
        if file_num < len(file_uid_mapping) - 1:
            yield [''] * len(fields)

def get_data(repo_dir: pathlib.Path, uids: set[str], include_filter: Optional[set[set[str]]] = None, exclude_filter: Optional[set[str]] = None) -> Generator[list[str], None, None]:
    """
    repo_dir is a path to the bilara-data repository or structurally equivilant data

    uids is a set of the uids to get the data for, this can be a single text uid such as {dn2}, a single folder uid such as {dn}
    or multiple, such as {dn1,dn2,dn3,dn4,dn5,dn6,dn7,dn8,dn9,dn10}

    include_filter is a set of muids or frozensets of muids {frozenset({'translation','en','sujato'}),'root','reference'}, if None everything is included
    
    exclude_filter is a set of muids, anything matching will be excluded, e.g. {'comment'}. If None nothing is excluded.

    Returns a generator that yields rows of data suitable for feeding to csv_writer. The first result is the fields
    which will always start with the segment_id and be followed by root, translation and markup fields (provided they
    are included by filters), remaining included fields are sorted in simple alphabetical order.
    Subsequent results are rows of data.
    When multiple texts are processed each text is seperated by a list of empty strings.
    """

    file_uid_mapping = {}
    for file in iter_json_files(repo_dir):
        
        try:
            uid, muids_string = file.stem.split('_')
        except:
            print(file)
            raise

        if not (uid in uids or any(part in uids for part in file.parent.parts)):
            continue
            
        print('Reading {}'.format(str(file.relative_to(repo_dir))))

        muids = frozenset(muids_string.split('-'))
        if include_filter:
            for muid in include_filter:
                if isinstance(muid, frozenset):
                    if muids.intersection(muid) == muid:
                        break
                else:
                    if muid in muids:
                        break
            else:
                continue
        
        if exclude_filter and exclude_filter.intersection(muids):
            continue
        
        if uid not in file_uid_mapping:
            file_uid_mapping[uid] = {}
        file_uid_mapping[uid][muids_string] = file
    
    if not file_uid_mapping:
        print('No matches for {}'.format(",".join(args.uid)), file=sys.stderr)
        exit(1)
        
    muid_strings = set()
    for keys in file_uid_mapping.values():
        muid_strings.update(keys)
    
    muid_strings = sorted(muid_strings, key=muid_sort_key)
    
    print(file_uid_mapping)
    
    print_html(file_uid_mapping)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Export Spreadsheet")
    parser.add_argument('uid', nargs='+', help='One or more sutta UID to export')
    parser.add_argument('out', help='Output file')
    parser.add_argument('--include', default='', help='Filter by MUID. Comma seperated, + for and\nexample: "root,translation+en"')
    parser.add_argument('--exclude', default='', help='Filter by MUID. Comma seperated')
    args = parser.parse_args()

    uids = frozenset(args.uid)
    if args.include:
        include_filter = {frozenset(filter.split('+')) if '+' in filter else filter for filter in args.include.split(',')}
    else:
        include_filter = None
    if args.exclude:
        exclude_filter = frozenset(args.exclude.split(','))
    else:
        exclude_filter = None
    
    rows = get_data(repo_dir, uids, include_filter, exclude_filter)
