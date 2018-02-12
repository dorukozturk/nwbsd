import { action,
         store,
         observeStore } from './redux';

import graph from '../../graph.json';

store.dispatch(action.setGraphData(graph.nodes, graph.links));

observeStore(next => {
  const graph = next.get('graph');
}, s => s.get('graph'));
