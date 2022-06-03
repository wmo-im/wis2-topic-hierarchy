# WIS2 Topic Hierarchy

WIS 2.0 real-time data sharing is based on a message queuing protocol (MQP) supporting a publication/subscription mechanism. A user can subscribe to an MQP broker to receive real-time notifications that some data can be downloaded. The notification message received from the MQP broker contains a URL to download the data. In addition, the MQP broker offers a range of topics organised in a hierarchy. The users can select their topics of interest and subscribe to them to receive notifications and download data relevant to their work.

The users can also discover datasets from the Global Discovery Catalogue (GDC), obtaining the topic and the MQP broker offering the dataset to subscribe and receive notifications of new data. The GDC&#39;s new WIS Core Metadata Profile 2.0 has a categorisation scheme consistent with the topic hierarchy to provide an adequate search experience compatible with the access modality provided by the MQP broker. In other words, the MQP topic and WIS 2.0 metadata have the same vocabulary so that search and access are consistent.

The structure of the topic hierarchy underpins the discovery and sharing of data in WIS 2.0 and has to be standardised across all the WIS 2.0 services to provide consistent search and access to the user.

Recalling that WIS 2.0 is designed to support the WMO Unified Data Policy, the topic hierarchy must be aligned with [WMO Res. 1 Cg-EXT-21 - Unified Data Policy](https://ane4bf-datap1.s3-eu-west-1.amazonaws.com/wmocms/s3fs-public/ckeditor/files/Cg-Ext2021-d04-1-WMO-UNIFIED-POLICY-FOR-THE-INTERNATIONAL-approved_en_0.pdf?4pv38FtU6R4fDNtwqOxjBCndLIfntWeR).

The following WIS 2.0 topic hierarchy has been developed according to the classification of the Earth System domains in Annex 1 of Resolution 1 Cg-Ext(2021).

The topic hierarchy is represented in the following table

| **Level** | **Name** | **Values** | **Notes** |
| --- | --- | --- | --- |
| **1** | channel | origin|cache | origin -\&gt; data downloaded from original NC/DCPFcache -\&gt; data downloaded from a Global Cache |
| **2** | version | a,b,c,… | Alphabetic version of the topic hierarchy |
| **3** | wis2 | wis2 | Fixed for WIS 2.0 |
| **4** | country | ISO3166 3-letter code | Exception for Partner Organizations |
| **5** | center\_id | acronym decided by Member | List of NC/DCPC is the starting point. Acronym required |
| **6** | resource\_type | data|metadata|report | In WIS 2.0 different resources will be shared, including data, metadata and reports (from monitoring activities) |
| **7** | data-policy | core|recommended | Core are available from the Global Caches with open access on a free and unrestricted basis. Notifications for core and recommended are available by subscription to Global Brokers. Recommended are downloaded from original NC/DCPC and may require authentication/authorisation |
| **8** | Earth-system-domain | weather|climate|hydrology|atmospheric-composition|cryosphere|ocean|space-weather | Annex 1 of resolution 1 Cg-Ext-2021 |
| **9** | Earth-system-domain-subcategory | In table 2 | From this level it is entirely to be defined by the domain experts |

| **earth-system-domain** | **earth-system-domain-subcategory** |
| --- | --- |
| **weather** |
|| surface-based-observations |
|| satellite-nwp |
|| satellite-nowcasting |
|| global-analysis-prediction |
|| limited-area-analysis-prediction |
|| watches-advisories-guidance |
| **climate** |
|| gcos-upper-air-and-surface |
|| climate-data |
|| ecv |
|| climate-reanalysis |
| **hydrology** |
|| reference-stations |
|| satellite |
|| global-regional-models |
| **Atmospheric composition** |
|| observations |
|| watches-advisories-warnings |
| **cryosphere** |
|| observations |
|| analysis-prediction-reanalysis |
|| watches-advisories-warnings |
| **ocean** |
|| observations |
|| eov-and-ocean-ecv |
|| analysis-prediction |
|| reanalysis |
|| watches-advisories-warnings |
