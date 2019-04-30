#! /bin/sh

cd IMAv2/
git pull
cd slice_aggregator/
python3.6 slice_aggregator.py aggregatorS1.yml > slice_aggregator.log
