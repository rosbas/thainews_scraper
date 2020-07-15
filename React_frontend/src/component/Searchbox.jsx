import React, { Component } from 'react';
import { useEffect } from 'react';
import '../App.css';

import Outputbox from './Outputbox';

const Searchbox = () => {
    const [keyword, setkeyword] = React.useState('');
    const [subStat, setsubStat] = React.useState(false);
    const fetch1 = (e) => {
        e.preventDefault();
        console.log(keyword);
        setsubStat(true);
    }

    const crawl1 = () => {
        window.open('https://www.youtube.com/watch?v=Gd9OhYroLN0', "_blank");
    };

    const clear1 = () => {
        setsubStat(false);
        setkeyword('');
    };

    return (
        <div>
            <span style={ {fontSize: 50, margin: 20} }>Searchbar</span>
            <div className="bborder">
                <form>
                    <div style={{display: 'flex', justifyContent: 'center'}}>
                        <input style={{fontSize: 40, width: 600, margin: 20}} type='text' placeholder = 'Keyword' value = {keyword} onChange={(e) => setkeyword(e.target.value)}/>
                        <button className = "btn btn-secondary btn-sm" style = {{ fontSize: '30px', margin:20}} onClick = {fetch1}>Fetch</button>
                        <button className = "btn btn-danger btn-sm" style = {{ fontSize: '30px', margin:20}} onClick = {crawl1}>Crawl</button>
                        <button className = "btn btn-primary btn-sm" style = {{ fontSize: '30px', margin:20}} onClick = {clear1}>Clear</button>
                    </div>
                </form>
            </div>
            <div className="resultbox">
                {subStat ? <Outputbox keyword={keyword} /> : <span style={{fontSize: 200, color: '#C8C8C8', margin: 20}}>Nothing Here!</span> }
            </div>
        </div>
    );
};

export default Searchbox;