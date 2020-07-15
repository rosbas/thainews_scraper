import React, { Component } from 'react';
import catwork from '../catwork.gif';
import '../App.css';


const Homepage = () => {
    return(
        <div className="App">
            <img src={catwork} className="App-logo" alt="logo" />
            <h1>Home Page</h1>
            <h2>Go to Searchbar and type in the keyword!</h2>
        </div>
    )
}

export default Homepage;