import React, { Component } from 'react';
import '../App.css';
import { Navbar, Nav, NavDropdown } from "react-bootstrap";

const Navbarc = () => {
    return(
        <div className="App">
        <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark">
        <Navbar.Brand href="/">INTERN BOIS NEWS CRAWLER</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="mr-auto">
            <Nav.Link href="/Searchbar">Search Bar</Nav.Link>
            <Nav.Link href="/Howwedoit">How we do it</Nav.Link>
            <NavDropdown title="Others" id="collasible-nav-dropdown">
              <NavDropdown.Item href="https://uncyclopedia.ca/wiki/Coronavirus">Coronavirus</NavDropdown.Item>
              <NavDropdown.Item href="https://uncyclopedia.ca/wiki/JavaScript">JavaScript</NavDropdown.Item>
              <NavDropdown.Item href="https://uncyclopedia.ca/wiki/Twitter">Twitter</NavDropdown.Item>
              <NavDropdown.Divider />
              <NavDropdown.Item href="http://th.uncyclopedia.info/wiki/%E0%B9%82%E0%B8%88%E0%B9%82%E0%B8%88%E0%B9%89_%E0%B8%A5%E0%B8%AD%E0%B8%9A%E0%B8%86%E0%B9%88%E0%B8%B2%E0%B8%AA%E0%B8%B1%E0%B8%94%E0%B8%94%E0%B8%B4%E0%B8%A7%E0%B8%B0">Ora!</NavDropdown.Item>
            </NavDropdown>
          </Nav>
          <Nav>
            <Nav.Link href="/Moreyeets">More yeets</Nav.Link>
            <Nav.Link eventKey={2} href="/Dankmemes">
              Dank memes
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      </div>
    )
}

export default Navbarc;