import { select } from 'd3-selection';
import debounce from 'lodash.debounce';

import { action,
         store,
         observeStore } from './redux';
import { Graph } from './nodelink';
import graph from '../graph.json';
import mainpage from './index.pug';
import './index.styl';

document.write(mainpage());

// Initialize and then respond to change in window size.
store.dispatch(action.resizeWindow(window.innerWidth, window.innerHeight));
const debounceOptions = {
  leading: true,
  trailing: true
};
window.addEventListener('resize', debounce(() => {
  store.dispatch(action.resizeWindow(window.innerWidth, window.innerHeight));
}, 300, debounceOptions));

// Initialize the graph data.
graph.nodes.forEach(d => {
  d.collapsed = true;
});
store.dispatch(action.setGraphData(graph.nodes, graph.links));

// Set up a node link diagram.
const nodelink = new Graph(select('#graph').node(), {
  width: window.innerWidth,
  height: window.innerHeight,
  maxdepth: Math.max(...graph.nodes.map(x => x.depth))
});
