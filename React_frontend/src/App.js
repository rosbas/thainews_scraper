import React, { useEffect } from 'react';

const App = () => {
	useEffect(() => {
		fetch('http://localhost:5000/movies', {
			headers: {
				accepts: 'application/json',
			},
		}).then((response) =>
			response
				.json()
				.then((data) => console.log(data))
				.catch(() => console.log("Can't access due to fucking CORS policy"))
		);
	}, []);

	return <div className="App" />;
};

export default App;
