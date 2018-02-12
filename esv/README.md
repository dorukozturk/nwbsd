# Experimental Structure Visualization (ESV) prototype

## Build Instructions

1. Install NPM dependencies: `npm i`
2. Build the data: `cd ..; python dumptree.py | python tree2graph.py
   >graph.json`
2. Build the application: `npm run build`
3. Serve the application: `npm run serve`
4. Visit http://localhost:8080 in your browser.
