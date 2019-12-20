import React from 'react';
import { connect } from 'react-redux'
import { getLogoutThunkCreator } from '@/redux/contextReducers'


class NotFound extends React.Component {
    componentDidMount(){
        this.props.Logout()
    }
    render() {
        return (
            <div>
            </div>
        )
    }
}

export default connect((state)=>state, {Logout: getLogoutThunkCreator})(NotFound);
