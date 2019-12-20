import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux'

import App from './App';
import reduxStore from '@/redux'
import './styles/index.css';
import './styles/styles.css';
import './styles/bootstrap/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.css';

ReactDOM.render(
    <Provider store={reduxStore}>
        <App />
    </Provider>,
    document.getElementById('app')
);
