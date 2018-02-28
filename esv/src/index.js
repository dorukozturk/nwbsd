import { select } from 'd3-selection';

import { action,
         store,
         observeStore } from './redux';
import { Graph } from './nodelink';
import graph from '../graph.json';
import mainpage from './index.pug';

document.write(mainpage());

store.dispatch(action.setGraphData(graph.nodes, graph.links));

const nodelink = new Graph(select('#graph').node(), {
  width: window.innerWidth,
  height: window.innerHeight,
  maxdepth: Math.max(...graph.nodes.map(x => x.depth))
});
