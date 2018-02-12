import { select } from 'd3-selection';

import { action,
         store,
         observeStore } from './redux';
import graph from '../../graph.json';
import mainpage from './index.pug';

import { makeGraph } from './nodelink';

document.write(mainpage());

store.dispatch(action.setGraphData(graph.nodes, graph.links));

observeStore(next => {
  const graph = next.get('graph');

  const el = select('#graph').node();
  makeGraph(el, {
    width: window.innerWidth,
    height: window.innerHeight,
    nodes: graph.get('nodes'),
    links: graph.get('links')
  });
}, s => s.get('graph'));
