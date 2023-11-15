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
import os

topics = []

for root, dirs, files in os.walk('earth-system-discipline'):
    for file_ in files:
        if file_.endswith('.csv'):
            root2 = root.replace('earth-system-discipline', '')
            if root2.startswith('/'):
                root2 = root2.replace('/', '', 1)
            filename = os.path.join(root, file_)
            with open(filename) as fh2:
                reader = csv.reader(fh2)
                next(reader)
                for row in reader:
                    topic_to_add = f'{root2}/{row[0]}'
                    if topic_to_add.startswith('/'):
                        topic_to_add = topic_to_add.lstrip('/')

                    topics.append(topic_to_add)

with open('earth-system-discipline.csv', 'w') as fh:
    fieldnames = ['Name']
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()

    for topic in sorted(topics):
        writer.writerow({'Name': topic})
