import { action,
         store,
         observeStore } from './redux';

console.log('hello');

observeStore(next => {
  const mode = next.get('mode');
  console.log(`mode changed to ${mode}`);
}, s => s.get('mode'));

store.dispatch(action.initial('hello'));

window.setTimeout(() => {
  store.dispatch(action.secondary());
}, 2000);
