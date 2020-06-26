import React, { useEffect, useState } from 'react';
import { Input, AutoComplete } from 'antd';
import { News } from '../Components/News';

const Main = () => {
	// const [movies, setMovies] = useState([]);
	const [news, setNews] = useState([]);
	useEffect(() => {
		fetch('http://localhost:5000/news', {
			headers: {
				accepts: 'application/json',
			},
		}).then((response) =>
			response.json().then((data) => {
				console.log(data.news);
				setNews(data.news);
			})
		);
	}, []);

	return (
		<div className="App">
			<AutoComplete
				dropdownMatchSelectWidth={252}
				style={{
					width: 300,
				}}
				// options={options}
				// onSelect={onSelect}
				// onSearch={handleSearch}
			>
				<Input.Search size="large" placeholder="Search key words" enterButton />
			</AutoComplete>
			<News news={news} />
		</div>
	);
};

export default Main;
