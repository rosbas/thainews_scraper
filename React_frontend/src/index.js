import React from 'react';
import ReactDOM from 'react-dom';
import Main from './MainLayout/Main';
import * as serviceWorker from './serviceWorker';
import '../node_modules/antd/dist/antd.css';
// import App from './App';

ReactDOM.render(
	<React.StrictMode>
		<Main />
	</React.StrictMode>,
	document.getElementById('root')
);
serviceWorker.unregister();
