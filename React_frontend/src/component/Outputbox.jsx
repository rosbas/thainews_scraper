import React, { Component } from 'react';
import axios from 'axios';
import loading1 from '../loading1.svg'
import { useEffect } from 'react';

const Outputbox = ({keyword}) => {
    const [resultItem, setresultItem] = React.useState([]);
    const [loading, setLoading] = React.useState(false);

    const resultFunction = async () => {
        try {
            const data = await axios
            //.get('https://api.lyrics.ovh/v1/Dragonforce/Through%20the%20Fire%20and%20Flames')
            .get('https://acaya-intern.et.r.appspot.com/news')
            //https://api.lyrics.ovh/v1/coldplay/
            .then(res1 => {
                console.log(res1);
                //setresultItem(keyword);
                setresultItem(res1.news);
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


    return (
    <div>
        {loading ? resultItem : <img src={loading1} className="loadingpic" alt="loading" /> }
    </div>
    );
};

export default Outputbox;