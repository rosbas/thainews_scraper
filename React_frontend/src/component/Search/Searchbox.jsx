import React, { Component } from 'react';
import axios from 'axios';
import '../../App.css';

import Outputbox from './Outputbox';

const Searchbox = () => {
    const [keyword, setkeyword] = React.useState('');
    const [subStat, setsubStat] = React.useState(4);
    const [crawlreply, setCrawlreply] = React.useState('no reply');

    const fetch1 = (e) => {
        e.preventDefault();
        console.log(keyword);
        setsubStat(1);
    }

    const crawl1 = (e) => {
        //e.preventDefault(); prevents the state from re-rendering back to the default state
        e.preventDefault();

        console.log(keyword);

         // POST request using axios inside useEffect React hook
        //const article = { title: 'React Hooks POST Request Example' };
        //axios.post('https://reqres.in/api/articles', article)
            //.then(response => setCrawlreply(response.data.id));
        const article = { search_field: {keyword} };
        axios.post('https://acaya-intern.et.r.appspot.com/scraping', article)
            .then(response => setCrawlreply(response.data));

        setsubStat(2);
    };

    const clear1 = (e) => {
        e.preventDefault();
        setsubStat(0);
        setkeyword('');
    };

    const decideOutput = (subS) => {
        switch(subS) 
        {
            case 0:
                return (<span style={{fontSize: '5vmin', color: '#C8C8C8', margin: 20}}>Nothing Here!</span>);
            case 1:
                return (<Outputbox keyword={keyword} />);
            case 2:
                return (
                    <div>
                        <div>
                            <span>
                                {'The Request to Scrape by the keyword: '}
                            </span>
                            <span>
                                {keyword}
                            </span>
                            <span>
                                {', had been sent to the server'}
                            </span>
                        </div>
                        <div>
                            <span>
                                {'Response: '}
                            </span>
                            <span>
                                {crawlreply}
                            </span>
                        </div>
                    </div>);;
            default:
                return (<span style={{fontSize: 200, color: '#C8C8C8', margin: 20}}>Nothing Here!</span>);
          }
    }

    return (
        <div>
            <span style={ {fontSize: 50, margin: 20} }>Searchbar</span>
            <div className="bborder">
                <form>
                    <div style={{display: 'flex', justifyContent: 'center'}}>
                        <input className = "mainsearchinput"  type='text' placeholder = 'Keyword' value = {keyword} onChange={(e) => setkeyword(e.target.value)}/>
                        <button className = "btn btn-secondary btn-sm mainsearchbutton" onClick = {fetch1}><span className = 'mainbuttontext1'>Fetch</span></button>
                        <button className = "btn btn-danger btn-sm mainsearchbutton" onClick = {crawl1}><span className = 'mainbuttontext1'>Crawl</span></button>
                        <button className = "btn btn-primary btn-sm mainsearchbutton" onClick = {clear1}><span className = 'mainbuttontext1'>Clear</span></button>
                    </div>
                </form>
            </div>
            <div className="resultbox">
                <div>
                    {decideOutput(subStat)}
                </div>
            </div>
        </div>
    );
};

export default Searchbox;