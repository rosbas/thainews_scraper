import React, { Component } from 'react';
import ReactPlayer from 'react-player';

const Dankmemes = () => {
    return(
        <div className="App">
            <h1>Dankmemes</h1>
            <div style={{display: 'flex', justifyContent: 'center'}}>
            <ReactPlayer controls url='https://www.youtube.com/watch?v=tYzMYcUty6s' />
            </div>
        </div>
    )
}

export default Dankmemes;