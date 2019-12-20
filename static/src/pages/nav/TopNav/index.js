import React from 'react';
import DefaultNav from './DefaultNav'
import MobileNav from './MobileNav'

function TopNav(props) {
    return (
        <div>
            <MobileNav/>
            <DefaultNav/>
        </div>
    )
}

export default TopNav;
