import React from 'react';
import { Link, useRouteMatch, useParams } from 'react-router-dom'
import { ts2date } from '@/utils/time'


export default function ({logs, curr}) {
    let params = useParams();
    function getPath(name) {
        return `/task/${params.slug}/log/${name}`
    }
    return (
        <div className="col-12">
            <h2>History</h2>
            <small>Tolal found {logs.length} logs</small>
            <div className="table-responsive" id="logs">
                <table className="table table-striped table-md">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Date</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {logs && logs.map(log => (
                            <tr key={log.name}>
                                <td>
                                    { log.name != curr.name ?
                                        <Link className="btn btn-sm btn-info" to={getPath(log.name)}>
                                            {log.name}
                                        </Link>
                                        :
                                        log.name
                                    }
                                </td>
                                <td>{ ts2date(log.date) }</td>
                                <td>
                                    { log.status ?
                                        <span className="text-success">Success</span>
                                        :<span className="text-danger">Failed</span>
                                    }
                                </td>
                            </tr>
                            )
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    )
}
