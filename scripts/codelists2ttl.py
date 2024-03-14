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
import shutil
from string import Template


def gen_skos_subregister(name: str, description: str,
                         source: str = None) -> str:
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
        print(f'    Generating {relative_path}')
    with file_path.open('w') as fh:
        fh.write(ttl)


def process_subdomain_index(relative_path: Path, csv_base_path: Path,
                            ttl_base_path: Path,
                            verbose: bool = False) -> None:
    """
    Processes recursively all index.csv files in csv_base_path/relative_path
    and writes output to ttl_base_path/relative_path/

    :param relative_path: relative path to start with
    :param csv_base_path: base path where to look for CSV files
    :param ttl_base_path: base path where store generated TTL files

    :returns: `None`
    """

    if verbose:
        print(f'  processing {relative_path}')
    current_csv_dir = csv_base_path / relative_path
    current_ttl_dir = ttl_base_path / relative_path
    current_ttl_dir.mkdir()
    index_file_path = current_csv_dir / 'index.csv'
    with index_file_path.open() as fh_index:
        csv_reader = csv.DictReader(fh_index)
        for csv_record in csv_reader:
            file_name = csv_record['Name'] + '.ttl'
            csv_sub_dir = current_csv_dir / csv_record['Name']
            if csv_sub_dir.exists():
                if verbose:
                    print(f'    creating sub-register {file_name}')
                ttl = gen_skos_subregister(csv_record['Name'],
                                           csv_record['Description'])
                write_ttl_file(ttl, ttl_base_path, relative_path / file_name)
                # recursion
                process_subdomain_index(relative_path / csv_record['Name'],
                                        csv_base_path, ttl_base_path, verbose)
            else:
                if verbose:
                    print(f'    no sub-directory {csv_sub_dir}')
                    print(f'    creating concept {file_name}')
                ttl = gen_skos_concept(csv_record['Name'],
                                       csv_record['Description'])
                write_ttl_file(ttl, ttl_base_path, relative_path / file_name)


parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Print more details')
args = parser.parse_args()

ROOT_PATH = Path.cwd()
CSV_FILES_PATH = ROOT_PATH / 'topic-hierarchy'
TTL_FILES_PATH = ROOT_PATH / 'wis/topic-hierarchy'
COLLECTIONS = []

print('Generating WIS2 Topic Hierarchy TTL files')

ttl_files_path = ROOT_PATH / 'wis/topic-hierarchy'
if ttl_files_path.exists():
    print(f'removed {ttl_files_path}')
    shutil.rmtree(ttl_files_path)
ttl_files_path.mkdir(parents=True)

root_table = ROOT_PATH / 'topic-hierarchy.csv'


root_ttl = ROOT_PATH / 'wis' / 'topic-hierarchy.ttl'
with root_ttl.open('w') as fh:
    ttl = gen_skos_subregister('topic-hierarchy', 'WIS2 Topic Hierarchy')
    fh.write(ttl)


with root_table.open() as fh:
    subregisters = []
    reader = csv.DictReader(fh)
    for row in reader:
        ttl_files_path = ROOT_PATH / 'wis/topic-hierarchy'
        subregister_url = 'http://codes.wmo.int/wis/topic-hierarchy'
        subregisters.append(f'<{subregister_url}>')
        register_ttl_dir = ttl_files_path
        register_ttl_file = register_ttl_dir / f'{row["Name"]}.ttl'
        if args.verbose:
            print(f'Generating {register_ttl_file}')

        if row['Name'] != 'earth-system-discipline':
            with register_ttl_file.open('w') as fh2:
                ttl = gen_skos_subregister(row['Name'], row['Description'])
                fh2.write(ttl)

            concept_csv_file = ROOT_PATH / f'topic-hierarchy/{row["Name"]}.csv'

            with concept_csv_file.open() as fh3:
                reader2 = csv.DictReader(fh3)
                for row2 in reader2:
                    concept_ttl_dir = register_ttl_dir / f'{row["Name"]}'
                    if not concept_ttl_dir.exists():
                        concept_ttl_dir.mkdir()
                    concept_ttl_file = concept_ttl_dir / f'{row2["Name"]}.ttl'
                    if args.verbose:
                        print(f'Generating {concept_ttl_file}')
                    with concept_ttl_file.open('w') as fh4:
                        ttl = gen_skos_concept(row2['Name'],
                                               row2['Description'])
                        fh4.write(ttl)
        else:
            with register_ttl_file.open('w') as fh2:
                ttl = gen_skos_subregister(row['Name'], row['Description'])
                fh2.write(ttl)

print('Level 1-7 completed')

print('Generating Level 8+')
process_subdomain_index(Path('earth-system-discipline'), CSV_FILES_PATH,
                        TTL_FILES_PATH, args.verbose)

print('Done')
