# WIS2 topic hierarchy

## Overview

The WIS2 topic hierarchy provides a central classification and categorization scheme used by data
providers and WIS2 Global Services in support of core WIS2 workflows: publish, discover, subscribe
and download.

## Real-time data sharing

WIS 2.0 real-time data sharing is based on a message queuing protocol (MQP) supporting a publication/subscription mechanism. A user can subscribe to an MQP broker to receive real-time notifications that some data can be downloaded. The notification message received from the MQP broker contains a URL to download the data. In addition, the MQP broker offers a range of topics organised in a hierarchy. The users can select their topics of interest and subscribe to them to receive notifications and download data relevant to their work.

## Data discovery

Users can discover datasets from the Global Discovery Catalogue (GDC), obtaining the topic and the MQP broker offering the dataset to subscribe and receive notifications of new data. Datasets in the GDC are made available via the WMO Core Metadata Profile 2.0 (WCMP2) standard for discovery metadata, which supports a categorisation scheme consistent with the topic hierarchy to provide an seamless search experience compatible with the access modality provided by the MQP broker. In other words, the MQP topic and WIS 2.0 discovery metadata have the same vocabulary so that discovery, subscription and download are consistent.

## Structure

The structure of the topic hierarchy underpins the discovery and sharing of data in WIS 2.0 and has to be standardized across all the WIS 2.0 services to provide consistent search and access to the user.

Recalling that WIS 2.0 is designed to support the WMO Unified Data Policy, the topic hierarchy must be aligned with [WMO Res. 1 Cg-EXT-21 - Unified Data Policy](https://ane4bf-datap1.s3-eu-west-1.amazonaws.com/wmocms/s3fs-public/ckeditor/files/Cg-Ext2021-d04-1-WMO-UNIFIED-POLICY-FOR-THE-INTERNATIONAL-approved_en_0.pdf?4pv38FtU6R4fDNtwqOxjBCndLIfntWeR).

The WIS 2.0 topic hierarchy has been developed according to the classification of the Earth System domains in Annex 1 of Resolution 1 Cg-Ext(2021), and is managed in two parts:

1. primary topic levels (levels 1-8): topic structure to be applied by all data and services in WIS 2.0. These levels are managed by the WMO Secretariat
2. domain specific topic subcategory levels (level 9 and beyond): topic structure proposed by domain experts and user communities. Note that the number of levels in this part may vary according to the requirements of various domains


The primary topic levels are described in the following table:

| **Level** | **Name** | **Notes** |
| --- | --- | --- |
| **1** | channel | Location of of where the data originates from (data providers [`origin`] or global services [`cache`]) |
| **2** | version | Alphabetical version of the topic hierarchy |
| **3** | wis2 | Fixed value of `wis2` for WIS 2.0 |
| **4** | country | lower case representation of ISO3166 3-letter code. Includes extensions for partner organizations |
| **5** | center-id | acronym as specified by member and endorsed by the PR of the country and by WMO|
| **6** | resource-type | WIS 2.0 resources types (`data`, `metadata`, `reports` [from monitoring activities]) |
| **7** | data-policy | data policy as defined by the WMO Unified Data Policy. `core` data are available from the Global Caches with open access on a free and unrestricted basis. Notifications for core and recommended data are available by subscription to Global Brokers. `recommended` data are downloaded from original NC/DCPC and may require authentication/authorisation |
| **8** | earth-system-discipline | As per Annex 1 of resolution 1 Cg-Ext-2021 |
| **9** | earth-system-discipline-subcategory | As proposed by domain experts and further approved by INFCOM|
