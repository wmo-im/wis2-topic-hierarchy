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
        index_file_path = os.path.abspath(index_file)
        sub_dir_part = index_file_path.split('/earth-system-discipline/')[1]
        sub_dir = sub_dir_part.replace("/index.csv", "")
        for row3 in reader_index:
            if sub_dir != "":
                concept_ttl_dir = f"{register_ttl_dir}/{sub_dir}"
                concept_ttl_file = f"{concept_ttl_dir}/{row3['Name']}.ttl"
            else:
                concept_ttl_file = f"{register_ttl_dir}/{row3['Name']}.ttl"
            print(f'Generating {concept_ttl_file}')
            with open(concept_ttl_file, 'w') as fh2_index:
                ttl = gen_skos_concept(row3['Name'],
                                       row3['Description'])
                fh2_index.write(ttl)
            concept_csv_dir = os.path.abspath(index_file)
            concept_csv_file = f"{concept_csv_dir}/{row3['Name']}/index.csv"
            if os.path.exists(concept_csv_file):
                read_subdomain_index(concept_csv_file)


REGISTER = 'http://codes.wmo.int/wis'

ROOTPATH = Path.cwd()
CSV_FILES_PATH = ROOTPATH / 'topic-hierarchy'
TTL_FILES_PATH = ROOTPATH / 'wis/topic-hierarchy'
COLLECTIONS = []

print('Generating WIS2 Topic Hierarchy TTL files')

ttl_files_path = ROOTPATH / 'wis/topic-hierarchy'
if ttl_files_path.exists():
    print(f'removed {ttl_files_path}')
    shutil.rmtree(ttl_files_path)
ttl_files_path.mkdir(parents=True)

root_table = ROOTPATH / 'topic-hierarchy.csv'

with root_table.open() as fh:
    subregisters = []
    reader = csv.DictReader(fh)
    for row in reader:
        ttl_files_path = ROOTPATH / 'wis/topic-hierarchy'
        subregister_url = "http://codes.wmo.int/wis/topic-hierarchy"
        subregisters.append(f"<{subregister_url}>")
        register_ttl_dir = ttl_files_path
        register_ttl_file = f"{register_ttl_dir}/{row['Name']}.ttl"
        print(f'Generating {register_ttl_file}')

        if "earth-system-discipline" not in str(row['Name']):
            with open(register_ttl_file, 'w') as fh2:
                ttl = gen_skos_subregister(row['Name'],
                                           row['Description'])
                fh2.write(ttl)

            concept_csv_file = ROOTPATH / f"topic-hierarchy/{row['Name']}.csv"

            with concept_csv_file.open() as fh3:
                reader2 = csv.DictReader(fh3)
                for row2 in reader2:
                    concept_ttl_dir = register_ttl_dir / f"{row['Name']}"
                    if not os.path.exists(concept_ttl_dir):
                        concept_ttl_dir.mkdir()
                    concept_ttl_file = concept_ttl_dir / f"{row2['Name']}.ttl"
                    print(f'Generating {concept_ttl_file}')
                    with concept_ttl_file.open('w') as fh4:
                        ttl = gen_skos_concept(row2['Name'],
                                               row2['Description'])
                        fh4.write(ttl)

print("Level 1-7 READY")
root_table_sub = ROOTPATH / 'topic-hierarchy/earth-system-discipline/index.csv'
ttl_root_dir = ROOTPATH / 'wis/topic-hierarchy/earth-system-discipline'
if not os.path.exists(ttl_root_dir):
    ttl_root_dir.mkdir()

with open(root_table_sub, "r") as fh5:
    subregisters = []
    reader = csv.DictReader(fh5)
    subreg_baseurl = "http://codes.wmo.int/wis/topic-hierarchy/earth-system-discipline"
    for row in reader:
        ttl_files_path = ROOTPATH / f"wis/topic-hierarchy/earth-system-discipline"
        subregister_url = f"{subreg_baseurl}/{row['Name']}"
        subregisters.append(f"<{subregister_url}>")
        register_ttl_dir = ttl_files_path
        register_ttl_file = f"{register_ttl_dir}/{row['Name']}.ttl"
        print(f'Generating {register_ttl_file}')
        if not os.path.exists(register_ttl_dir):
            register_ttl_dir.mkdir()

        with open(register_ttl_file, 'w') as fh6:
            ttl = gen_skos_subregister(row['Name'],
                                       row['Description'])
            fh6.write(ttl)

        concept_csv_dir = ROOTPATH / f"topic-hierarchy/earth-system-discipline/{row['Name']}"
        concept_csv_file = f"{concept_csv_dir}/index.csv"
        concept_ttl_path = Path(f"{ttl_files_path}/{row['Name']}")
        if not os.path.exists(concept_ttl_path):
            concept_ttl_path.mkdir()
        concept_ttl_file = f"{ttl_files_path}/{row['Name']}.ttl"
        concept_rel_path = ""

        read_subdomain_index(concept_csv_file)

print('Done')
