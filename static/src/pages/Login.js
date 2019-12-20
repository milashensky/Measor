import React from 'react';
import { connect } from 'react-redux'
import { getLoginThunkCreator } from '@/redux/contextReducers'

import 'styles/forms.css'


function Login (props) {
    let data = {
        username: React.createRef(),
        password: React.createRef(),
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        props.doLogin({username: data.username.value, password: data.password.value})
    }
    return (
        <div className="login">
            <h4>Login</h4>
            <form onSubmit={handleSubmit}>
                {props.errors.map((err, i) =>
                    <p className="error" key={i}>
                        {err}
                    </p>
                )}
                <input placeholder="username" name="username" type="text" ref={(e) => data.username = e }/>
                <input placeholder="password" name="password" type="password" ref={(e) => data.password = e }/>
                <button>Sing in</button>
            </form>
        </div>
    );
}


const mapStateToProps = (state) => ({
    errors: state.context.errors || [],
    user: state.context.id
})

export default connect(mapStateToProps, {doLogin: getLoginThunkCreator})(Login);
