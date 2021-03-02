#! /bin/bash    
DIR=$(dirname $(readlink -f $0))
cd $(dirname "$DIR")

venv=$(poetry env info --path)
source "${venv}/bin/activate"

python scripts/collect_feeds_and_sync.py