# WMO Codes Registry management

## Overview

The scripts in this directory are used to manage the WIS2 Topic Hierarchy (WTH)
publication to the WMO Codes Registry.

## The WMO Codes Registry

The [WMO Codes Registry](https://codes.wmo.int) is an authoritative service that
provides a number of registers defining controlled vocabularies used in various
WMO standards and systems.

The service provides an API in support of automated workflow to manage codelist
registers. The API is available as follows:

- https://ci.codes.wmo.int: testing
- https://codes.wmo.int: production

API usage requires an account and credentials. Contact WMO Secretariat to be
provided access to the WMO Codes Registry API (a GitHub user id is required).

Once you receive access, an API Key is required to manage resources on the registry.
To create an API Key, once logged into the registry, select _Admin / Create a temporary password (API Key)_,
and click _Create password_ to generate an API key.

## Mapping from WTH to the WMO Code Registry

The overall setup of WTH publication to the WMO Codes Registry works as follows:

`wis` / CSV filename (without file extension) / CSV row `Name`

where:

- `wis` is the root `reg:Register`
- `topic-hierarchy` is attached to the `wis` register as a sub-register
  - each WTH CSV file is a `reg:Register` itself, attached to the `topic-hierarchy` register as a sub-register
  - each row in a WTH CSV file is a `skos:Concept` tied to its sub-register
- `topic-hierarchy/earth-system-discipline` is attached to the `wis/topic-hierarchy` register as a sub-register
  - each WTH CSV `index.csv` file is a `reg:Register` itself, attached to the relevant `topic-hierarchy` directory / register as a sub-register
  - each row in a WTH CSV file is a `skos:Concept` tied to its sub-register

## Publication workflows

Managing WTH publication to the WMO Codes Registry involves the following steps:

- creating the `wis` register - needed only once, mentioned only for completeness
- generating TTL files from CSV
- publishing TTL files to the WMO Codes Registry

### Creating the `wis` register

Use the action/button "Create register" in the web UI of the WMO Codes Registry and fill following attributes:
- Notation
- Label
- Description

### Generating TTLs

To generate TTL files, from the root of the repository, run the following command:

```bash
python3 scripts/codeslists2ttl.py
```

This will create all TTL files in a directory called `wis`.

### Publishing TTLs

To upload TTL files, from the root of the repository, run the following command:

```bash
python3 scripts/upload_changes.py https://api.github.com/users/{user_id} <password> <environment> <output-directory> <status>
```

where:

- `user_id` is your GitHub userid
- `password` is the API Key (see the [#overview](Overview) with instructions on how to generate an API Key
- `environment` is whether to upload change to the testing or production environment
- `output-directory` is the resulting directly where TTL outputs should published from, that is `wis`
- `status` is either `experimental` or `stable`, please note that this value cannot be changed on existing entries

The script has a few more options, notably `-h` that displays help.

Examples:

```bash
# publish to test environment on https://ci.codes.wmo.int with experimental status
python3 scripts/upload_changes.py https://api.github.com/users/tomkralidis API_KEY test wis experimental

# publish to test environment on https://ci.codes.wmo.int with stable status
python3 scripts/upload_changes.py https://api.github.com/users/tomkralidis API_KEY test wis stable

# publish to production environment on https://codes.wmo.int with experimental status
python3 scripts/upload_changes.py https://api.github.com/users/tomkralidis API_KEY prod wis experimental

# publish to production environment on https://codes.wmo.int with stable status
python3 scripts/upload_changes.py https://api.github.com/users/tomkralidis API_KEY prod wis stable
```

This will create/update all resources on the WMO Codes Registry.
