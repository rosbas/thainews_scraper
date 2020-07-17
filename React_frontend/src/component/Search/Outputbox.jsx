import React, { Component } from 'react';
import axios from 'axios';
import loading1 from '../../loading1.svg'
import { useEffect } from 'react';

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
            <li>{indivnew.title}</li>
            <div className = "bborder2"></div>
            <div style = {{display: 'flex', justifyContent: 'center', margin: '1px', padding: '4px'}}>
                <li style = {{margin: '10px'}}>{indivnew.date}</li>
                <div className = "column-divider"></div>
                <li style = {{margin: '10px'}}>{indivnew.category}</li>
                <div className = "column-divider"></div>
                <li style = {{margin: '10px'}}>{indivnew.author}</li>
            </div>
            <div className = "bborder2"></div>
            <li style = {{margin: '5px'}}>{indivnew.body}</li>
            <div className = "bborder2"></div>
            <li style = {{margin: '10px'}}>{indivnew.url}</li>  
        </div>
        <div className = "bborder"></div>
    </div>
    );  
    return (
    <div>
        {loading ? listItems : <img src={loading1} className="loadingpic" alt="loading" /> }
    </div>
    );
};

export default Outputbox;