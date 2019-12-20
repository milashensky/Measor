import React from 'react';


export default function ({log}) {
    return (
        <div className="row w-100">
            <div className="col-6">
                { log.name ?
                <h3 className="h2">{log.name} log</h3>
                :''
                }
            </div>
            <div className="col-6 text-right">
                <h4>Status:
                { log.status ?
                    <span className="text-success">Success</span>
                    :<span className="text-danger">Failed</span>
                }
                </h4>
            </div>
            <div className="col-12">
                <pre className="logs">
                    <code>
                        { log.data && log.data.map((line, $i) => (
                            <span key={$i}>{ line }</span>
                        )) }
                    </code>
                </pre>
            </div>
        </div>
    )
}
