###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

import argparse
import csv
from pathlib import Path
import re
import shutil
from string import Template

description_suffix = '-description'


def gen_skos_subregister(
    name: str, description: str, source: str = None
) -> str:
    """
    Generate SKOS Sub-register TTL

    :param name: identifier of collection
    :param description: label of collection

    :returns: `str` of SKOS Sub-register TTL
    """

    SUBREGISTER = '''
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ldp: <http://www.w3.org/ns/ldp#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<$name> a reg:Register , skos:Collection , ldp:Container ;
        ldp:hasMemberRelation skos:member ;
        rdfs:label "$name" ;
        dct:description "$description"'''

    template_vars = {
        'name': name,
        'description': description
    }

    if source != '':
        SUBREGISTER += ' ;\n        rdfs:isDefinedBy "$source" .'
        template_vars['source'] = source
    else:
        SUBREGISTER += ' .'

    return Template(SUBREGISTER).substitute(template_vars).strip()


def gen_skos_concept(name: str, description: str, source: str = None) -> str:
    """
    Generate SKOS Concept TTL

    :param name: identifier of collection
    :param description: label of collection

    :returns: `str` of SKOS Concept TTL
    """

    CONCEPT = '''
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix dct: <http://purl.org/dc/terms/> .

<$name> a skos:Concept ;
        rdfs:label "$name" ;
        skos:notation "$name" ;
        dct:description "$description"@en'''

    template_vars = {
        'name': name,
        'description': description
    }

    if source != '':
        CONCEPT += ' ;\n        rdfs:isDefinedBy "$source" .'
        template_vars['source'] = source
    else:
        CONCEPT += ' .'

    return Template(CONCEPT).substitute(template_vars).strip()


def write_ttl_file(ttl: str, ttl_base_path: Path, relative_path: Path,
                   verbose: bool = False) -> None:
    """
    Write TTL to file

    :param ttl: `str` the TTL to be written to the file
    :param ttl_base_path: the base path/directory for TTL files
    :param relative_path: the relative path of this TTL file

    :returns: `None`
    """

    file_path = ttl_base_path / relative_path
    if verbose:
        indent = len(relative_path.parents)
        print_with_indent(indent, f'writing {relative_path}')
    with file_path.open('w') as fh:
        fh.write(ttl)


def print_with_indent(indent: int, message: str) -> None:
    """
    Print message with indent

    :param indent: indentation level
    :param message: the message to be printed

    :returns: `None`
    """

    indent_str = ''.ljust(indent * 2)
    print(f'{indent_str}{message}')


def process_subdomain_index(relative_path: Path, csv_base_path: Path,
                            ttl_base_path: Path,
                            verbose: bool = False,) -> None:
    """
    Processes recursively all index.csv files in csv_base_path/relative_path
    and writes output to ttl_base_path/relative_path/

    :param relative_path: relative path to start with
    :param csv_base_path: base path where to look for CSV files
    :param ttl_base_path: base path where store generated TTL files

    :returns: `None`
    """
    indent = len(relative_path.parents) - 1
    if indent == 1:
        print_with_indent(indent, f'generating subtree in {relative_path}')
        indent += 1

    current_csv_dir = csv_base_path / relative_path
    current_ttl_dir = ttl_base_path / relative_path
    current_ttl_dir.mkdir()
    index_file_path = current_csv_dir / 'index.csv'
    flat_index_file_path = current_csv_dir / 'index-flat.csv'
    if index_file_path.exists():
        if verbose:
            print_with_indent(
                indent,
                f'processing {index_file_path.relative_to(csv_base_path)}',
            )
            indent += 1
        with index_file_path.open() as index_file:
            csv_reader = csv.DictReader(index_file)
            for csv_record in csv_reader:
                file_name = csv_record['Name'] + '.ttl'
                csv_sub_dir = current_csv_dir / csv_record['Name']
                if csv_sub_dir.exists():
                    if verbose:
                        print_with_indent(
                            indent, f'creating sub-register {file_name}'
                        )
                    ttl = gen_skos_subregister(
                        csv_record['Name'],
                        csv_record['Description'],
                        csv_record['Source'],
                    )
                    write_ttl_file(
                        ttl, ttl_base_path, relative_path / file_name, verbose
                    )
                    # recursion
                    process_subdomain_index(
                        relative_path / csv_record['Name'],
                        csv_base_path,
                        ttl_base_path,
                        verbose,
                    )
                else:
                    if verbose:
                        print_with_indent(
                            indent,
                            f'{relative_path/csv_record["Name"]} is a leaf',
                        )
                        print_with_indent(
                            indent + 1, f'creating concept {file_name}'
                        )
                    ttl = gen_skos_concept(
                        csv_record['Name'],
                        csv_record['Description'],
                        csv_record['Source'],
                    )
                    write_ttl_file(
                        ttl, ttl_base_path, relative_path / file_name, verbose
                    )
    elif flat_index_file_path.exists():
        if verbose:
            rel_file_path = flat_index_file_path.relative_to(csv_base_path)
            print_with_indent(
                indent,
                f'processing {rel_file_path}',
            )
        else:
            print_with_indent(
                indent, f'converting flat CSV to subtree in {relative_path}'
            )
        with flat_index_file_path.open() as flat_index_file:
            csv_records = list(csv.reader(flat_index_file))
            (name_keys, description_keys) = read_flat_index_keys(
                csv_records[0]
            )
            name_column = 0
            process_flat_subdomain_index(
                csv_records,
                1,
                name_column,
                name_keys,
                description_keys,
                relative_path,
                csv_base_path,
                ttl_base_path,
                name_column + 1 == len(name_keys),
                verbose,
            )


def read_flat_index_keys(keys: list[str]) -> list[str]:
    if len(keys) % 2 != 0 or len(keys) == 0:
        raise RuntimeError(f'Unexpected number of columns {len(keys)}')
    description_regex = re.compile(r'\w+' + description_suffix)
    description_keys = [k for k in keys if description_regex.match(k)]
    name_keys = [k for k in keys if not description_regex.match(k)]
    if len(description_keys) != len(name_keys):
        raise RuntimeError(
            f'Unexpected number of description columns {len(description_keys)}'
        )
    return (name_keys, description_keys)


def process_flat_subdomain_index(csv_records: list[str], current_row: int,
                                 name_column: int, name_keys: list[str],
                                 description_keys: list[str],
                                 relative_path: Path,
                                 csv_base_path: Path,
                                 ttl_base_path: Path, is_leaf: bool,
                                 verbose: bool = False,) -> None:
    """
    Processes index-flat.csv file as if it was a sub-tree in
    "csv_base_path/relative_path" where each level is described by two columns
    in the CSV file, "X" containing domain name and "X-description" containing
    the description. Columns/levels are processed from left to right, but
    the order of description columns is not important.
    The output (sub-tree of TTLs) is written into "ttl_base_path/relative_path"

    :param csv_records: list of CSV records read from the flat file
    :param current_row: current row in the CSV file
    :param name_column: index of the (sub-domain) name column in the record
    :param name_keys: list of (sub-domain) name keys (not descriptions)
    :param description_keys: list of (sub-domain) description keys
    :param relative_path: relative path to start with
    :param csv_base_path: base path where to look for CSV files
    :param ttl_base_path: base path where store generated TTL files
    :param is_leaf: `True` if this is the last level of the hierarchy
    :param verbose: `True` if more details should be printed out

    :returns: `None`
    """

    indent = len(relative_path.parents) + name_column
    current_ttl_dir = ttl_base_path / relative_path
    if not current_ttl_dir.exists():
        current_ttl_dir.mkdir()

    name_key = name_keys[name_column]
    description_key = name_key + description_suffix
    column_names = csv_records[0]
    name_value_previous = ''
    parent_value_previous = (
        '' if name_column == 0 else csv_records[current_row][name_column - 1]
    )

    while current_row < len(csv_records) and (
        name_column == 0
        or csv_records[current_row][name_column - 1] == parent_value_previous
    ):
        csv_record = csv_records[current_row]
        name_value = csv_record[column_names.index(name_key)]
        description_value = csv_record[column_names.index(description_key)]

        if name_value != name_value_previous:
            name_value_previous = name_value
            file_name = name_value + '.ttl'
            if not is_leaf:
                if verbose:
                    print_with_indent(
                        indent,
                        f'creating sub-register/{name_key} "{name_value}"',
                    )
                ttl = gen_skos_subregister(name_value, description_value, '')
                write_ttl_file(
                    ttl, ttl_base_path, relative_path / file_name, verbose
                )
                # recursion
                next_level_name_column = name_column + 1
                process_flat_subdomain_index(
                    csv_records,
                    current_row,
                    next_level_name_column,
                    name_keys,
                    description_keys,
                    relative_path / name_value,
                    csv_base_path,
                    ttl_base_path,
                    next_level_name_column + 1 == len(name_keys),
                    verbose
                )
            else:  # is leaf
                if verbose:
                    print_with_indent(
                        indent, f'creating concept/{name_key} "{name_value}"'
                    )
                # TODO: source?
                ttl = gen_skos_concept(name_value, description_value, '')
                write_ttl_file(
                    ttl, ttl_base_path, relative_path / file_name, verbose
                )
        current_row += 1


parser = argparse.ArgumentParser()
parser.add_argument(
    '-v', '--verbose', action='store_true', help='Print more details'
)
args = parser.parse_args()

ROOT_PATH = Path.cwd()
CSV_FILES_PATH = ROOT_PATH / 'topic-hierarchy'
COLLECTIONS = []

print('Re-generating WIS2 Topic Hierarchy TTL files')

topic_hierarchy_ttl_dir = ROOT_PATH / 'wis/topic-hierarchy'
if topic_hierarchy_ttl_dir.exists():
    print_with_indent(1, f'removed {topic_hierarchy_ttl_dir}')
    shutil.rmtree(topic_hierarchy_ttl_dir)
topic_hierarchy_ttl_dir.mkdir(parents=True)

topic_hierarchy_csv_path = ROOT_PATH / 'topic-hierarchy.csv'

topic_hierarchy_ttl_path = ROOT_PATH / 'wis' / 'topic-hierarchy.ttl'
with topic_hierarchy_ttl_path.open('w') as topic_hierarchy_ttl_file:
    ttl = gen_skos_subregister('topic-hierarchy', 'WIS2 Topic Hierarchy')
    topic_hierarchy_ttl_file.write(ttl)


with topic_hierarchy_csv_path.open() as root_table_file:
    subregisters = []
    reader = csv.DictReader(root_table_file)
    for row in reader:
        subregister_url = 'http://codes.wmo.int/wis/topic-hierarchy'
        subregisters.append(f'<{subregister_url}>')
        register_ttl_file_name = Path(f'{row["Name"]}.ttl')

        ttl = gen_skos_subregister(row['Name'], row['Description'])
        write_ttl_file(
            ttl, topic_hierarchy_ttl_dir, register_ttl_file_name, True
        )

        if row['Name'] != 'earth-system-discipline':
            concept_csv_file = ROOT_PATH / f'topic-hierarchy/{row["Name"]}.csv'

            with concept_csv_file.open() as concept_csv_file:
                reader2 = csv.DictReader(concept_csv_file)
                for row2 in reader2:
                    concept_ttl_dir = (
                        topic_hierarchy_ttl_dir / f'{row["Name"]}'
                    )
                    if not concept_ttl_dir.exists():
                        concept_ttl_dir.mkdir()
                    concept_ttl_file = concept_ttl_dir / f'{row2["Name"]}.ttl'
                    relative_concept_ttl_path = concept_ttl_file.relative_to(
                        topic_hierarchy_ttl_dir
                    )
                    ttl = gen_skos_concept(
                        row2['Name'], row2['Description'], row2['Source']
                    )
                    write_ttl_file(
                        ttl,
                        topic_hierarchy_ttl_dir,
                        relative_concept_ttl_path,
                        args.verbose
                    )


print('Level 1-7 completed')

print('Generating Level 8+')
process_subdomain_index(
    Path('earth-system-discipline'),
    CSV_FILES_PATH,
    topic_hierarchy_ttl_dir,
    args.verbose
)

print('Done')
