import React, { Component } from 'react';
import loading1 from '../loading1.svg';
import '../App.css';

import Searchbox from './Searchbox';




class Searchbar extends Component {
    
    render() { 
        return (  
            <React.Fragment>
                <div className="App">
                    <Searchbox></Searchbox>
                </div>
            </React.Fragment>
        );
    }

}

export default Searchbar;
