import React from 'react';
import NavLinks from './NavLinks'


function Sidebar(props) {
    return (
        <nav className="col-md-2 d-none d-md-block bg-light sidebar">
            <div className="sidebar-body">
                <NavLinks className="nav flex-column"/>
            </div>
        </nav>
    )
}

export default Sidebar;
