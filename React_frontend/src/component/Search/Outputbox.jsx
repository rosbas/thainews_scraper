import React, { Component } from 'react';
import axios from 'axios';
import loading1 from '../../loading1.svg'
import { useEffect } from 'react';
import { CSVLink, CSVDownload } from "react-csv";

const Outputbox = ({keyword}) => {
    const [resultItem, setresultItem] = React.useState([]);
    const [loading, setLoading] = React.useState(false);
    var firsturl = 'https://acaya-intern.et.r.appspot.com/' + 'searching?search_field=' + keyword.toString();
    const [url1, seturl] = React.useState( firsturl + '');
    
    const resultFunction = async () => {
        try {
            const data = await axios
            //.get('https://api.lyrics.ovh/v1/Dragonforce/Through%20the%20Fire%20and%20Flames')
            //const url = 'https://acaya-intern.et.r.appspot.com/searching?search_field='
            //url = url + keyword
            //.get(url)
            //console.log('before post ',url1)
            .post(url1)
            
            .then(res1 => {
                console.log(res1);
                //setresultItem(keyword);
                setresultItem(res1.data.news);
                //setresultItem(res1.data.lyrics);
            });
            setLoading(true);
        } catch (e) {
            console.log(e)
        }
    }

    useEffect(() => {
        resultFunction()
    }, [] );

    const listItems = resultItem.map((indivnew, index) =>
    <div>
        <div style={{display: 'inline-block', justifyContent: 'center', margin: '2px', padding: '1px'}}>
            <div>{indivnew.title}</div>
            <div className = "bborder2"></div>
            <div style = {{display: 'flex', justifyContent: 'center', margin: '1px', padding: '4px'}}>
                <div style = {{margin: '10px'}}>{indivnew.date}</div>
                <div className = "column-divider"></div>
                <div style = {{margin: '10px'}}>{indivnew.category}</div>
                <div className = "column-divider"></div>
                <div style = {{margin: '10px'}}>{indivnew.author}</div>
            </div>
            <div className = "bborder2"></div>
            <div style = {{margin: '4px', padding: '1%'}}>{indivnew.body}</div>
            <div className = "bborder2"></div>
            <div className = "urlbox">{indivnew.url}</div>  
        </div>
        <div className = "bborder"></div>
    </div>
    );

    return (
    <div>
        <span>
            <span>{'Showing '}</span>
            <span>{resultItem.length}</span>
            <span>{' Results'}</span>
        </span>
        <div>
            <CSVLink data = {resultItem} filename={"News.csv"} className="btn btn-primary" target="_blank" >Download as CSV</CSVLink>
        </div>
        <div className = "bborder"></div>
        {loading ? listItems : <img src={loading1} className="loadingpic" alt="loading" /> }
    </div>
    );
};

export default Outputbox;