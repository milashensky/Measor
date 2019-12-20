import React, {Component} from 'react';
import { Router, Switch, Route, Redirect } from 'react-router-dom';
import { Provider, connect } from 'react-redux'

import { history } from '@/utils/history'
import { getContextThunkCreator } from '@/redux/contextReducers'
import Layout from 'pages/Layout'
import Login from 'pages/Login'
import NotFound from 'pages/NotFound'

class App extends Component {
    componentDidMount(){
        this.props.getContext()
    }

    render () {
        return (
            <Router history={history}>
                <div className="App">
                    {this.props.fetched ?
                        <Switch>
                            <Route path="/login" exact
                                render={props => !this.props.user_id ?
                                    <Login/>
                                    :<Redirect to={{pathname: "/", state: {nextPathname: props.location.pathname}}}/>}
                            />
                            <Route path="/"
                                render={props => this.props.user_id ?
                                    <Layout user={this.props.user_id}/>
                                    :<Redirect to={{pathname: "/login", state: {nextPathname: props.location.pathname}}}/>}
                            />
                            <Route path="*">
                                <NotFound/>
                            </Route>
                            </Switch>
                        :
                        <div>Loading</div>
                    }
                </div>
            </Router>
        );
    }
}

const mapStateToProps = (state) => {
    return {
        user_id: state.context.id,
        fetched: state.context.status
    }
}
export default connect(mapStateToProps, {getContext: getContextThunkCreator})(App);
