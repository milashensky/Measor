import React from 'react';
import { connect } from 'react-redux'
import { useParams } from 'react-router-dom'
import { getUpdateTaskThunk, getFetchTasksThunk } from '@/redux/taskReducers'
import CreateView from './CreateEditView'


function Edit (props) {
    let defaults = Object.assign({
        name: '',
        interval: '',
        interval_units: '',
        code: '',
        max_logs_count: '',
        max_log_life: '',
    }, props.defaults)
    let task = (<div/>);
    let params = useParams()
    if (!props.task || props.task.slug != params.slug)
        props.fetchTask({slug: params.slug})
    else {
        defaults = Object.assign(defaults, props.task)
        task = (<CreateView defaults={defaults} title={`Edit ${props.task.name} task`} submit={submit} errors={props.errors}/>)
    }
    function submit(form) {
        props.saveTask({slug: params.slug, ...Object.fromEntries(Object.entries(form).map(x => {x[1] = x[1].value; return x }))});
    }
    return (
        task
    )
}

const mapStateToProps = (state) => ({
    task: state.tasks.task,
    updated: state.tasks.updated,
    errors: state.tasks.addTaskErrors,
    defaults: state.context.defaults
})

export default connect(mapStateToProps, {saveTask: getUpdateTaskThunk, fetchTask: getFetchTasksThunk})(Edit)
