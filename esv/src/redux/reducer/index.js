import Immutable from 'immutable';

import { actionType } from '../action';

import { Graph } from '../../nodelink';

const initial = Immutable.fromJS({
  graph: null,
  nodelink: null
});

const reducer = (state = initial, action = {}) => {
  let newState = state;

  if (action.type === undefined) {
    throw new Error('fatal: undefined action type');
  }

  switch (action.type) {
    case actionType.setGraphData:
      newState = state.set('graph', Immutable.fromJS({
        nodes: action.nodes,
        links: action.links
      }));
      break;

    case actionType.createGraph:
      const data = state.get('graph').toJS();
      const nodelink = new Graph(action.el, {
        width: action.width,
        height: action.height,
        maxdepth: action.maxdepth,
        nodes: data.nodes,
        links: data.links
      });

      newState = state.set('nodelink', nodelink);
      break;

    case actionType.updateGraph:
      {
        const nodelink = state.get('nodelink');
        const data = state.get('graph').toJS();
        nodelink.update(data.nodes, data.links);
      }
      break;

    case actionType.toggleHide:
      newState = state.updateIn(['graph', 'nodes', action.index, 'hidden'], x => !x);
      break;

    case actionType.savePositions:
      const nodes = state.get('graph').toJS().nodes;

      let table = {};
      nodes.forEach((x, i) => table[x.name] = i);

      newState = state.withMutations(s => {
        action.data.forEach(d => {
          s = s.updateIn(['graph', 'nodes', table[d.name], 'x'], val => d.x)
            .updateIn(['graph', 'nodes', table[d.name], 'y'], val => d.y);
        });
      });
      break;
  }

  return newState;
};

export {
  reducer
};
