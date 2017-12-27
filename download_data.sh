#!/bin/bash

if ! [ -f tests/570014520.nwb ]; then
  curl -o tests/570014520.nwb "https://data.kitware.com/api/v1/file/5a4f91618d777f5e872f8101/download"
fi
