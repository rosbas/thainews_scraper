import React, { useEffect, useState } from 'react';
import { AutoComplete, Button } from 'antd';
import { News } from './Components/News';
import app from './Functions/axoisConfig';
import { DownloadOutlined } from '@ant-design/icons';

const Main = () => {
	const [news, setNews] = useState([]);
	const [word, setWord] = useState('');
	const onChange = (data) => {
		setWord(data);
	};
	const scrapeInternet = () => {
		console.log(`Scrapy now begin searching on ${word}`);
		app.post('/scraping', { search_field: `${word}` })
			.then((res) => {
				const recieveData = res.data;
				console.log(recieveData);
			})
			.catch(() => console.log('Can’t access ' + app.baseURL + '/scraping response. Blocked by browser?'));
	};

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
			{/* need bigger brain to implement this function. */}
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
