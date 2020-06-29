import axios from 'axios';

const baseURL = 'http://localhost:5000';

const app = axios.create({
	baseURL,
	withCredentials: true,
});

export default app;
