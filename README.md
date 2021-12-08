# USAS Clean
Take a USA Swimming NCAA Top Times Report (CSV) and clean data


## Overview
USA Swimming allows for their times database to be queried for NCAA times utilizing the *Top Times Report* feature. Division I can be found [here](https://www.usaswimming.org/times/ncaa/ncaa-division-i/top-times-report). This data can be exported in several different formats, including PDF, HTML, CSV, Excel, and RTF. The only format sufficient for data analysis is *CSV* (An Excel export is formatted like a PDF), but the format of CSV still has several issues. The purpose of this code and repoo is to provide an adequate tool for cleaning this data. 

## functions.py
Creates two functions to aid with formatting exported data.

**toSeconds:** Converts string times to seconds.

```
toSeconds('1:41.39')
  101.39
```

**CleanUSAS:** Puts the "dirty" CSV file through several different processes to clean it.

Parameters:
* DATA: Dataframe already read in via Pandas
* Description: Description of data set, used to name export file.

Process Description
1. Rename all columns to better descriptions
2. Remove `=` and `"` in all records
3. Split athlete name into `First` and `Last`
4. Replace long stroke names with short stroke names (i.e., *Individual Medley* becomes *IM*)
5. Split out race information into `Distance`, `Stroke`, `Course`, and `Gender`
6. Convert `DOB` and `Date` into DateTime format
7. Create `ID` column, which is a concatenation of `Last`, `DOB`, `Distance`, `Stroke`, and `Course`. The purpose of this column is to allow matching to occur between athletes and events in further analysis.
8. Export formatted CSV file

