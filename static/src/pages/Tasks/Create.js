import React from 'react';
import { connect } from 'react-redux'
import { getSaveTaskThunk } from '@/redux/taskReducers'
import CreateView from './CreateEditView'


function Create (props) {
    let defaults = Object.assign({
        name: '',
        interval: '',
        interval_units: '',
        code: '',
        max_logs_count: '',
        max_log_life: '',
    }, props.defaults)
    function submit(form) {
        props.saveTask(Object.fromEntries(Object.entries(form).map(x => {x[1] = x[1].value; return x })));
    }
    return (
        <CreateView defaults={defaults} title="Create new task" submit={submit} errors={props.errors}/>
    )
}

const mapStateToProps = (state) => ({
    updated: state.tasks.updated,
    errors: state.tasks.addTaskErrors,
    defaults: state.context.defaults
})

export default connect(mapStateToProps, {saveTask: getSaveTaskThunk})(Create)
