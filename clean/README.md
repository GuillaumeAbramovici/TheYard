
# Clean

A clean script to clean a structured folder directory under with the following structure:
> /mnt/prod/{prod}/sequence/{sequence}/{shot}/{department}/render/{shot}-{department}-v{version}/{shot}-{department}-v{version}.{SEQ}.{extension}

The script is avaible as a cli with the argument path where the path for your structure is

python clean.py --path yourpath --create_data bool

It goes throught the struture, find the severals versions for the last folder which contains the version,
keep only the last 3 ones and move the rest to a folder version struture under the name clean

