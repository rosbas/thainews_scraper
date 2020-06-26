import React from 'react';
import { List, Tag } from 'antd';

export const News = ({ news }) => {
	return (
		<div>
			<List
				itemLayout="horizontal"
				dataSource={news}
				renderItem={(item) => (
					<>
						<List.Item>
							<List.Item.Meta
								title={<p>{item.title}</p>}
								description={'Author: ' + item.author + ' Date: ' + item.date + ' URL: ' + item.url}
							/>
						</List.Item>
						<Tag className="list_tag"> {item.category} </Tag>
					</>
				)}
			/>
		</div>
	);
};