# Experimental Structure Visualization (ESV) prototype

## Build Instructions

1. Install NPM dependencies: `npm i`
2. Make sure the sample data file is downloaded: `sh download_data.sh`
3. Build the graph data: `cd esv; python data/dumptree.py ../tests/570014520.nwb
   | python data/tree2graph.py >graph.json`
4. Build the application: `npm run build`
5. Serve the application: `npm run serve`
6. Visit http://localhost:8080 in your browser.
7. Right click on the nodes to open a context menu.
