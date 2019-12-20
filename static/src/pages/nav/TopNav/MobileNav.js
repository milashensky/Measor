import React from 'react';
import { Link } from 'react-router-dom'
import NavLinks from '../NavLinks'


function MobileNav(props) {
    let [showNav, toggleNav] = React.useState(0);
    return (
        <nav className="navbar navbar-dark d-flex justify-content-between sticky-top bg-dark d-md-none">
            <Link className="navbar-brand border-0" to="/">
                Measor
            </Link>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#expandNav" aria-controls="expandNav" aria-expanded="false" aria-label="Toggle navigation" onClick={() => toggleNav(!showNav)}>
                <span className="navbar-toggler-icon"/>
            </button>
            <div className={`collapse navbar-collapse ` + (showNav ? 'show' : '')} id="expandNav">
                <NavLinks className="navbar-nav mr-auto">
                    <li className="nav-item">
                        <Link className="nav-link" to="/logout">Sign out</Link>
                    </li>
                </NavLinks>
            </div>
        </nav>
    )
}

export default MobileNav;
