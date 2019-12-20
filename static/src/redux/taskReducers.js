import resource from '@/resources'
import { history } from '@/utils/history'


export const TASK_RUN = 'TASK_RUN'
export const TASK_PAUSE = 'TASK_PAUSE'
export const TASKS_UPDATED = 'TASKS_UPDATED'
export const CURRENT_TASK_UPDATED = 'CURRENT_TASK_UPDATED'
export const TASKS_NEW_ERROR = 'TASKS_NEW_ERROR'
export const CURRENT_LOG_UPDATED = "CURRENT_LOG_UPDATED"
export const LOGS_UPDATED = "LOGS_UPDATED"
export const TASK_UPDATED = "TASK_UPDATED"

export const toggleTaskRun = (status, slug) => ({type: TASK_RUN, status, slug})
export const toggleTaskPause = (status, slug) => ({type: TASK_PAUSE, status, slug})
export const updateTasks = (tasks) => ({type: TASKS_UPDATED, tasks})
export const updateCurrentTask = (task) => ({type: CURRENT_TASK_UPDATED, task})
export const updatedTask = () => ({type: TASK_UPDATED})
export const createTaskError = (errors) => ({type: TASKS_NEW_ERROR, errors})
export const updateCurrentLog = (log) => ({type: CURRENT_LOG_UPDATED, log})
export const updateLogs = (logs) => ({type: LOGS_UPDATED, logs})


export const getTaskRunThunk = slug => dispatch => {
    dispatch(toggleTaskRun(true, slug));
    resource.TaskResource.save({slug: slug, action: 'build_now'}).then( resp => {
        dispatch(toggleTaskRun(false, slug));
    });
}
export const getTaskPauseToggleThunk = slug => dispatch => {
    resource.TaskResource.save({slug: slug, action: 'pause'}).then( resp => {
        dispatch(toggleTaskPause(resp.paused, slug));
    });
}

function fetchTasks(dispatch, data) {
    resource.TaskResource.get(data).then( resp => {
        if (data && data.slug)
            dispatch(updateCurrentTask(resp));
        else
            dispatch(updateTasks(resp));
    });
}
export const getFetchTasksThunk = (data) => dispatch => {
    fetchTasks(dispatch, data)
}

export const getSaveTaskThunk = (data) => dispatch => {
    resource.TaskResource.save(data).then( resp => {
        if (resp.status)
            dispatch(updatedTask());
        else
            dispatch(createTaskError(resp.errors || {}));
    });
}
export const getUpdateTaskThunk = (data) => dispatch => {
    resource.TaskResource.update(data).then( resp => {
        if (resp.status)
            dispatch(updatedTask());
        else
            dispatch(createTaskError(resp.errors || {}));
    });
}
export const getDeleteTaskThunk = (data) => dispatch => {
    resource.TaskResource.del(data).then( resp => {
        dispatch(updatedTask());
    });
}

function fetchTaskLogs(dispatch, data) {
    resource.TaskLogsResource.get(data).then( resp => {
        if (data && data.log)
            dispatch(updateCurrentLog(resp));
        else
            dispatch(updateLogs(resp));
    });
}
export const getFetchTaskLogsThunk = (data) => dispatch => {
    fetchTaskLogs(dispatch, data)
}

export default function tasksReducer(state = {tasks: []}, action) {
    let newState = {...state, updated: Date.now(), addTaskErrors: ''};
    switch (action.type) {
        case TASK_RUN:
            if (newState.tasks && newState.tasks.length && !action.status && action.slug) {
                let task = newState.tasks.find(x => x.slug == action.slug)
                if (task) {
                    newState.tasks[newState.tasks.indexOf(task)].build_now = true
                }
            }
            return newState;
        case TASK_PAUSE:
            if (newState.tasks && newState.tasks.length && !action.status && action.slug) {
                let task = newState.tasks.find(x => x.slug == action.slug)
                if (task) {
                    newState.tasks[newState.tasks.indexOf(task)].pause = action.status
                }
            }
            if (newState.task && newState.task.slug == action.slug)
                newState.task.pause = action.status
            return newState;
        case TASKS_UPDATED:
            return {...newState, tasks: action.tasks || []}
        case CURRENT_TASK_UPDATED:
            return {...newState, task: action.task || []}
        case TASK_UPDATED:
            delete newState.task
            setTimeout(function () {
                history.push('/')
            }, 10);
            return newState
        case TASKS_NEW_ERROR:
            return {...state, updated: Date.now(), addTaskErrors: action.errors}
        case CURRENT_LOG_UPDATED:
            return {...newState, currentLog: action.log}
        case LOGS_UPDATED:
            return {...newState, logs: action.logs}
    }
    return state
}
