import { createStore, applyMiddleware, combineReducers } from 'redux';
import thunkMiddleware from 'redux-thunk';

import context from './contextReducers.js'
import tasksReducer from './taskReducers.js'

const store = createStore(
    combineReducers({
        context,
        tasks: tasksReducer,
    }),
    applyMiddleware(thunkMiddleware),
)

export default store
