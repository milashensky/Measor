import React from 'react';
import { Link } from 'react-router-dom'
import DashIcon from 'pages/icons/dash.inline.svg'
import CreateIcon from 'pages/icons/create.inline.svg'


function NavLinks(props) {
    return (
        <ul className={props.className}>
            <li className="nav-item">
                <Link className="nav-link" to="/">
                    <DashIcon/>
                    Dashboard
                </Link>
            </li>
            <li className="nav-item">
                <Link className="nav-link" to="/create">
                    <CreateIcon/>
                    Create Item
                </Link>
            </li>
            { props.children }
        </ul>
    )
}

export default NavLinks;
