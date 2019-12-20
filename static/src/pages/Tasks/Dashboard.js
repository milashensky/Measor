import React from 'react';
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'
import { ts2date } from '@/utils/time'
import { getTaskRunThunk, getFetchTasksThunk } from '@/redux/taskReducers'


const UPDATE_INTERVAL_SECONDS = 10;
const getIntervalUnits = (data) => {
    switch (data) {
        case '0':
        return <span>Seconds</span>
        case '1':
        return <span>Minutes</span>
        case '2':
        return <span>Hours</span>
        case '3':
        return <span>Days</span>
    }
    return <span></span>
};


class Dashboard extends React.Component {
    componentDidMount(){
        this.updateInterval = setInterval(() => {
            this.props.updateTasks()
        }, 1000 * UPDATE_INTERVAL_SECONDS);
        this.props.updateTasks()
    }
    componentWillUnmount() {
        clearInterval(this.updateInterval)
    }
    render() {
        return (
            <div>
                <h2>List of tasks</h2>
                <div className="table-responsive">
                    <table className="table table-striped table-md">
                        <thead>
                            <tr>
                                <th></th>
                                <th>Name</th>
                                <th>Created</th>
                                <th>Interval</th>
                                <th>Last run</th>
                                <th>Status</th>
                                <th>Last duriation</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                        {this.props.tasks.length ? this.props.tasks.map(task => (
                            <tr key={task.slug}>
                                <td className="td-icon">
                                    {!task.running && !task.pause ? <i className="fa fa-sun text-info" tooltip="Wait"></i> : ''}
                                    {task.running ? <i className="fa fa-certificate fa-spin text-success" tooltip="Running now"></i> : ''}
                                    {!task.running && task.pause ? <i className="fa fa-certificate text-muted" tooltip="Paused"></i> : ''}
                                </td>
                                <td>
                                    <Link to={'/task/' + task.slug}>{task.name}</Link>
                                </td>
                                <td>{ ts2date(task.created) }</td>
                                <td>
                                    <span>
                                        { task.interval }
                                        { getIntervalUnits(task.interval_units) }
                                    </span>
                                </td>
                                <td>{ ts2date(task.last_run) }</td>
                                <td>
                                    {task.last_status === undefined ?
                                        <span>-</span>
                                        :<span className={(task.last_status? 'text-success': 'text-danger')}>{(task.last_status? 'Success': 'Failed')}</span>
                                    }
                                </td>
                                <td>{task.last_duriation} sec.</td>
                                <td className="td-icon">
                                    { !task.build_now && !task.pause ? <i className="fa fa-clock text-info" tooltip="Run now" onClick={() => this.props.run(task.slug)}></i> : '' }
                                    { task.build_now && !task.pause ? <i className="fa fa-clock text-warning" tooltip="Added to queue"></i> : '' }
                                    { task.pause ? <i className="fa fa-clock text-muted" tooltip="Task paused"></i> : '' }
                                </td>
                            </tr>
                        ))
                        : (
                            <tr className="text-center">
                                <td colSpan="9">No tasks</td>
                            </tr>
                        )}
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    tasks: state.tasks.tasks,
    updated: state.tasks.updated
})

export default connect(mapStateToProps, {
    run: getTaskRunThunk,
    updateTasks: getFetchTasksThunk,
})(Dashboard)
