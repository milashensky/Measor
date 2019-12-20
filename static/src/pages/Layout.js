import React from 'react';
import { Link, Route, Switch, useRouteMatch } from 'react-router-dom'
import Logout from 'pages/Logout'
import Dashboard from 'pages/Tasks/Dashboard'
import TaskDetails from 'pages/Tasks/Details'
import Create from 'pages/Tasks/Create'
import EditTask from 'pages/Tasks/Edit'
import TopNav from './nav/TopNav'
import Sidebar from './nav/Sidebar'

function Layout(props) {
    let { path, url } = useRouteMatch();
    return (
        <div className="home">
            <TopNav/>
            <div className="container-fluid">
                <div className="row">
                    <Sidebar/>
                    <main  className="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4">
                        <Switch>
                            <Route path={`${path}`} exact>
                                <Dashboard/>
                            </Route>
                            <Route path={`${path}create`} exact>
                                <Create/>
                            </Route>
                            <Route path={`${path}logout`} exact>
                                <Logout/>
                            </Route>
                            <Route path={`${path}task/:slug`} exact>
                                <TaskDetails/>
                            </Route>
                            <Route path={`${path}task/:slug/edit`} exact>
                                <EditTask/>
                            </Route>
                            <Route path={`${path}task/:slug/log/:log`} exact>
                                <TaskDetails/>
                            </Route>
                        </Switch>
                    </main>
                </div>
            </div>
        </div>
    );
}

export default Layout;
