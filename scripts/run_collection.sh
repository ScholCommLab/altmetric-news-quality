#! /bin/bash    
DIR=$(dirname $(readlink -f $0))
cd $(dirname "$DIR")

RECIPIENTS="asura.enkhbayar@gmail.com","juan@alperin.ca"

# echo `pwd`
source .venv/bin/activate

output=$(python scripts/collect_feeds_and_sync.py)
echo $output