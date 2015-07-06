# dvrhelper
DVRs and PVRs oftentimes generate media files that are not optimally named for media center software. dvrhelper renames files according to information from thetvdb.com, corrects their metadata, places them in appropriate directories, and even transcodes.

# Setup
git clone https://github.com/ArthurZey/dvrhelper.git
cd dvrhelper
virtualenv -p python3 env
source env/bin/activate
pip install tvdb_api