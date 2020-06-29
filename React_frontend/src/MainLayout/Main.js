import React, { useEffect, useState } from 'react';
import { AutoComplete, Button } from 'antd';
import { News } from './Components/News';
import app from './Functions/axoisConfig';
import { DownloadOutlined } from '@ant-design/icons';

const Main = () => {
	// const [movies, setMovies] = useState([]);
	const [news, setNews] = useState([]);
	const [word, setWord] = useState('');
	// const headers = {
	// 	'Content-Type': 'multipart/form-data',
	// };
	const onChange = (data) => {
		setWord(data);
	};
	const scrapeInternet = () => {
		console.log(`Scrapy now begin searching on ${word}`);
		const url = 'http://localhost:5000/scraping';
		// const here = 'https://cors-anywhere.herokuapp.com/' + url;
		app.post(url, { search_field: `${word}` })
			.then((res) => {
				const recieveData = res.data;
				console.log(recieveData);
			})
			.catch(() => console.log('Can’t access ' + url + ' response. Blocked by browser?'));
	};
	// const onSearch = (searchText) => {
	// 	console.log('searching');
	// 	console.log(searchText + ' searching');
	// };
	// const onSelect = (data) => {
	// 	console.log('I did select');
	// };
	//this is for getting data.
	useEffect(() => {
		fetch('http://localhost:5000/news', {
			headers: {
				accepts: 'application/json',
			},
		}).then((response) =>
			response.json().then((data) => {
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
				value={word}
				onChange={onChange}
				// options={options}
				// onSelect={onSelect}
				// onSearch={onSearch}
				required
			></AutoComplete>
			<Button type="primary" onClick={scrapeInternet}>
				Scrape Internet
			</Button>
			<Button type="primary">Filter</Button>
			<Button type="primary" icon={<DownloadOutlined />} size={'large'}>
				Download
			</Button>
			<News news={news} />
		</div>
	);
};

export default Main;
