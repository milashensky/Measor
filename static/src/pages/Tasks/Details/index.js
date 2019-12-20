import React, { useEffect } from 'react';
import { connect } from 'react-redux'
import { Link, withRouter } from 'react-router-dom'
import { getFetchTasksThunk, getFetchTaskLogsThunk, getDeleteTaskThunk, getTaskPauseToggleThunk } from '@/redux/taskReducers'
import LogDetail from './LogDetail'
import LogList from './LogList'


class Details extends React.Component {
    constructor(props) {
        super(props);
        this.url = `/task/${this.props.match.params.slug}`
    }
    componentDidMount() {
        if (!this.props.task || this.props.task.slug != this.props.match.params.slug)
            this.fetchTask()
    }
    componentDidUpdate() {
        let params = this.props.match.params,
            logName = params.log,
            currentLog = this.props.log || {};
        if (!logName && this.props.logs && this.props.logs.length)
            logName = this.props.logs[0].name
        if (this.props.task && this.props.task.slug == params.slug && logName && logName != currentLog.name)
            this.fetchLogs(logName)
    }
    fetchLogs(log) {
        this.props.fetchLog({slug: this.props.match.params.slug, log})
    }
    fetchTask() {
        this.props.fetchTask({slug: this.props.match.params.slug})
        this.fetchLogs()
    }
    deleteTask() {
        if (confirm('Are you sure?'))
            this.props.deleteTask({slug: this.props.match.params.slug})
    }
    render() {
        return (
            <div>
                {this.props.task ?
                    <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
                        <h1 className="h2">{this.props.task.name} task details</h1>
                        <div className="d-flex text-white">
                            <a className="btn btn-sm btn-secondary mr-2" onClick={() => this.props.pause(this.props.task.slug) }>
                                { this.props.task.pause ?
                                    "Unpause task"
                                    :"Pause task"
                                }
                            </a>
                            <Link className="btn btn-sm btn-info" to={`${this.url}/edit`}>Edit task</Link>
                            <a className="btn btn-sm btn-danger ml-2" onClick={() => this.deleteTask() }>Delete task</a>
                        </div>
                    </div>
                :
                    <div>
                    "Loading..."
                    </div>
                }
                <div className="row w-100">
                    <LogDetail log={this.props.log || {}}/>
                    <LogList logs={this.props.logs || []} curr={this.props.log || {}}/>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => ({
    task: state.tasks.task,
    updated: state.tasks.updated,
    logs: state.tasks.logs,
    log: state.tasks.currentLog,
})

export default connect(mapStateToProps, {fetchTask: getFetchTasksThunk, fetchLog: getFetchTaskLogsThunk, deleteTask: getDeleteTaskThunk, pause: getTaskPauseToggleThunk})(withRouter(Details))
