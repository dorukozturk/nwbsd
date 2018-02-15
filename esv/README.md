# Experimental Structure Visualization (ESV) prototype

## Build Instructions

1. Install NPM dependencies: `npm i`
2. Make sure the sample data file is downloaded: `sh download_data.sh`
2. Build the graph data: `cd esv; python data/dumptree.py ../tests/570014520.nwb
   | python data/tree2graph.py >graph.json`
2. Build the application: `npm run build`
3. Serve the application: `npm run serve`
4. Visit http://localhost:8080 in your browser.
