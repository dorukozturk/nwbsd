import Immutable from 'immutable';

import { actionType } from '../action';

const initial = Immutable.fromJS({
  graph: {
    nodes: null,
    links: null
  }
});

const reducer = (state = initial, action = {}) => {
  let newState = state;

  if (action.type === undefined) {
    throw new Error('fatal: undefined action type');
  }

  switch (action.type) {
    case actionType.setGraphData:
      newState = state.setIn(['graph', 'nodes'], action.nodes)
        .setIn(['graph', 'links'], action.links);
      break;
  }

  return newState;
};

export {
  reducer
};
