import React from 'react';
import './App.css';
import Dankmemes from "./component/Dankmemes.jsx";
import Searchbar from "./component/Search/Searchbar.jsx";
import Navbarc from "./component/Navbar.jsx";
import Howwedoit from "./component/Howwedoit.jsx";
import Moreyeets from "./component/Moreyeets.jsx";
import Homepage from "./component/Homepage.jsx";

import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  return (
    <div className="App">

      <Router>
        <Navbarc />
          {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
            {/* Order is important */}
          <Switch>
            <Route path="/Howwedoit" component = {Howwedoit}>
              <Howwedoit />
            </Route>
            <Route path="/Moreyeets" component = {Moreyeets}>
              <Moreyeets />
            </Route>
            <Route path="/Searchbar" component = {Searchbar}>
              <Searchbar />
            </Route>
            <Route path="/Dankmemes" component = {Dankmemes}>
              <Dankmemes />
            </Route>
            <Route path="/" component = {Homepage}>
              <Homepage />
            </Route>
          </Switch>
      </Router>

    </div>
  );
}

export default App;
