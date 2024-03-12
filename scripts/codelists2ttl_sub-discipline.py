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

import csv
from pathlib import Path
import shutil
from string import Template
import os


def gen_skos_register(subregisters: list) -> str:
    """
    Generate SKOS Register TTL

    :param name: identifier of collection
    :param description: label of collection

    :returns: `str` of SKOS Register TTL
    """

    REGISTER = '''
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix ldp: <http://www.w3.org/ns/ldp#> .
@prefix reg: <http://purl.org/linked-data/registry#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<wis> a reg:Register , ldp:Container ;
        rdfs:label "WIS" ;
        reg:notation "wis" ;
        dct:description "WIS2 Topic Hierarchy"@en ;
        reg:subregister '''

    REGISTER += ' , '.join(subregisters) + ' ; \n'

    REGISTER += 'rdfs:member' + ' , '.join(subregisters)

    REGISTER += ' .'

    return REGISTER.strip()


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


def read_subdomain_index(index_file):
    with open(index_file, "r") as fh_index:
        reader_index = csv.DictReader(fh_index)
    for row_index in reader_index:
        concept_ttl_file = register_ttl_dir / f"{row_index['Name']}.ttl"
        print(f'Generating {concept_ttl_file}')
        with concept_ttl_file.open('w') as fh2_index:
            ttl = gen_skos_concept(row_index['Name'],
                                   row_index['Description'])
            fh2_index.write(ttl)
        concept_csv_dir = os.path.abspath(index_file)
        concept_csv_file = f"{concept_csv_dir}/{row_index['Name']}/index.csv"
        if concept_csv_file.exists():
            read_subdomain_index(concept_csv_file)


REGISTER = 'http://codes.wmo.int/wis'

ROOTPATH = Path.cwd()
CSV_FILES_PATH = ROOTPATH / 'topic-hierarchy' / 'earth-system-discipline'
TTL_FILES_PATH = ROOTPATH / 'wis' / 'topic-hierarchy' / 'sub-discipline'
COLLECTIONS = []

print('Generating WIS2 Topic Hierarchy earth-system-disciplines TTL files')

ttl_files_path = ROOTPATH / 'wis' / 'topic-hierarchy' / 'sub-discipline'
if ttl_files_path.exists():
    shutil.rmtree(ttl_files_path)
ttl_files_path.mkdir()

root_table = ROOTPATH / 'topic-hierarchy/earth-system-discipline/index.csv'
ttl_files_path_base = ROOTPATH / 'wis' / 'topic-hierarchy' / 'sub-discipline'

with root_table.open() as fh:
    subregisters = []
    reader = csv.DictReader(fh)
    subreg_baseurl = "http://codes.wmo.int/wis/topic-hierarchy/sub-discipline"
    for row in reader:
        ttl_files_path = f"{ttl_files_path_base}" / f"{row['Name']}"
        subdirectories = True
        subregister_url = f"{subreg_baseurl}" / f"{row['Name']}"
        subregisters.append(f"<{subregister_url}>")
        register_ttl_dir = ttl_files_path
        register_ttl_file = ttl_files_path / f"{row['Name']}.ttl"
        print(f'Generating {register_ttl_file}')
        register_ttl_dir.mkdir()

        with register_ttl_file.open('w') as fh2:
            ttl = gen_skos_subregister(row['Name'],
                                       row['Description'])
            fh2.write(ttl)

        concept_csv_dir = ROOTPATH / 'topic-hierarchy/earth-system-discipline'
        concept_csv_file = f"{concept_csv_dir}" / f"{row['Name']}" / "index.csv"
        concept_ttl_file = register_ttl_dir / f"{row['Name']}.ttl"

        read_subdomain_index(concept_csv_file)

print('Done')
