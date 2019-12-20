import React from 'react';


export default function ({submit, defaults, title, errors}) {
    let form = {
        name: React.createRef(),
        interval: React.createRef(),
        interval_units: React.createRef(),
        code: React.createRef(),
        max_logs_count: React.createRef(),
        max_log_life: React.createRef(),
    }
    function handleSubmit(e) {
        e.preventDefault();
        submit(form);
    }
    return (
        <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pb-2 mb-3 border-bottom">
            <div className="row w-100">
                <div className="col-12">
                    <h1 className="h2">{title}</h1>
                </div>
                <div className="jumbotron col-sx-12 col-sm-8">
                    <form onSubmit={handleSubmit}>
                        <div className={ errors && errors.name ? "has-error form-group" : "form-group" }>
                            <label>Name</label>
                            <input className="form-control" type="text" name="name" ref={(e) => form.name = e } defaultValue={ defaults && defaults.name }/>
                            { errors && errors.name ?
                                <small className="invalid-feedback">{ errors.name }</small>
                                : ''
                            }
                        </div>
                        <div className={ errors && errors.interval ? "has-error form-group" : "form-group" }>
                            <label>Interval</label>
                            <div className="input-group">
                                <input className="form-control" type="number" name="interval" ref={(e) => form.interval = e } defaultValue={ defaults && defaults.interval }/>
                                <div className="input-group-append">
                                    <select className="form-control" name="interval_units" ref={(e) => form.interval_units = e } defaultValue={defaults && defaults.interval_units}>
                                        <option value="0">Seconds</option>
                                        <option value="1">Minutes</option>
                                        <option value="2">Hours</option>
                                        <option value="3">Days</option>
                                    </select>
                                </div>
                            </div>
                            { errors && errors.interval?
                                <small className="invalid-feedback">{ errors.interval }</small>
                                : ''
                            }
                        </div>
                        <div className={ errors && errors.code ? "has-error form-group" : "form-group" }>
                            <label>Code for task</label>
                            <textarea className="form-control task-code" name="code" ref={(e) => form.code = e } defaultValue={ defaults && defaults.code }></textarea>
                            { errors && errors.code ?
                                <small className="invalid-feedback">{errors.code}</small>
                                : ''
                            }
                        </div>
                        <div className={ errors && errors.max_logs_count ? "has-error form-group" : "form-group" }>
                            <label>Max # of logs to keep</label>
                            <input className="form-control" type="number" name="max_logs_count" ref={(e) => form.max_logs_count = e } defaultValue={ defaults && defaults.max_logs_count }/>
                            <small className="d-block block-info">If not empty, only up to this number of logs are kept</small>
                            { errors && errors.max_logs_count ?
                                <small className="invalid-feedback">{ errors.max_logs_count }</small>
                                : ''
                            }
                        </div>
                        <div className={ errors && errors.max_log_life ? "has-error form-group" : "form-group" }>
                            <label>Days to keep logs</label>
                            <input className="form-control" type="number" name="max_log_life" ref={(e) => form.max_log_life = e } defaultValue={ defaults && defaults.max_log_life }/>
                            <small className="d-block block-info">If not empty, logs are only kept up to this number of days</small>
                            { errors && errors.max_log_life ?
                                <small className="invalid-feedback">{ errors.max_log_life }</small>
                                : ''
                            }
                        </div>
                        <button className="btn btn-info" type="submit">
                            Create
                        </button>
                    </form>
                </div>
            </div>
        </div>
    )
}
