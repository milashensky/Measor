import React from 'react';
import { Link } from 'react-router-dom'

function DefaultNav(props) {
    return (
        <nav className="navbar navbar-dark bg-dark flex-md-nowrap p-0 d-none d-md-flex">
            <Link className="navbar-brand border-0" to="/">Measor</Link>
            <ul className="navbar-nav px-3 d-none d-md-block">
                <li className="nav-item text-nowrap">
                    <Link className="nav-link" to="/logout">Sign out</Link>
                </li>
            </ul>
        </nav>
    )
}

export default DefaultNav;
