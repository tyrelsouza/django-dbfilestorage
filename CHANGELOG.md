## CHANGELOG

- 2018-06-04 [Tyrel Souza] Move to gitlab, bump to 1.0.1
- 2018-03-01 [Tyrel Souza] Release Version 1.0.0
- 2018-02-01 [Tyrel Souza] Bump versions to django 1.11 and testing with Python3
- 2017-05-10 [Pamela McA'Nulty] Have save overwrite existing files
- 2017-02-06 [Tyrel Souza] Set primary key to `id` not `name`, this involves a lot of migrations, so I've kept them in multiple files
- 2017-01-27 [Tyrel Souza] Get rid of filehash
- 2017-01-26 [Tyrel Souza] Check filehash and filename, not just hash when checking if it needs to be saved.
- 2017-01-25 [Tyrel Souza] Keeping Filename on upload.
- 2017-01-23 [Tyrel Souza] Add Modified Time to storage support
- 2017-01-23 [Tyrel Souza] Everything should return a "filename" even if it's generated. Make the filename be the hash + ext. (fall back to .txt)
- 2017-01-20 [Tyrel Souza] Make path return None if no file
- 2017-01-20 [Tyrel Souza] Make path return filename
- 2017-01-20 [Tyrel Souza] Add another migration, and redo all the initial migrations.
- 2017-01-20 [Tyrel Souza] Make sure migrations is actually there.
- 2017-01-20 [Tyrel Souza] Split filename and filehash.
- 2016-12-09 [Tyrel Souza] Add signing key to readme.
- 2016-12-09 [Tyrel Souza] Update Tests, add some cleanup.
- 2016-12-08 [Tyrel Souza] Add more documentation.
- 2016-12-07 [Tyrel Souza] Update Readme, move to github, gitlab wasn't functioning properly.
- 2016-12-07 [Tyrel Souza] Initial commits and basic project setup
