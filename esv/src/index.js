import { select } from 'd3-selection';

import { action,
         store,
         observeStore } from './redux';
import graph from '../graph.json';
import mainpage from './index.pug';

document.write(mainpage());

store.dispatch(action.setGraphData(graph.nodes, graph.links));

observeStore(next => {
  const graph = next.get('graph').toJS();
  const nodelink = next.get('nodelink');

  if (!nodelink) {
    const el = select('#graph').node();
    const depths = graph.nodes.map(x => x.depth);
    const maxdepth = Math.max(...graph.nodes.map(x => x.depth));
    window.setTimeout(() => store.dispatch(action.createGraph(el, window.innerWidth, window.innerHeight, maxdepth)), 0);
  } else {
    window.setTimeout(() => store.dispatch(action.updateGraph()), 0);
  }
}, s => s.get('graph'));
