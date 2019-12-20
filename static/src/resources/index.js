const apiUrl = window.apiUrl || '/api/';
const defaultOptions = () => ({
    method: 'GET',
    mode: 'cors',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        "credentials": "same-origin",
        "Authorization": getAuth(),
    },
});

function getCookie(name){
    let re = new RegExp(name + "=([^;]+)"),
        value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

function getAuth(){
    return 'Basic ' + getCookie('auth')
}

function resource (url, data, method="GET", options={}) {
    return new Promise((res, rej) => {
        fetch(url, Object.assign(defaultOptions(), {
            method,
            body: JSON.stringify(data),
        }, options))
            .then(resp => {
                res(resp.json())
            }).catch(err => {
                rej(err)
            });
    })
}

export default {
    ContextResource: {
        get(data, options = {}) {
            return resource(apiUrl + 'context/', data, 'GET', options)
        },
    },
    LoginResource: {
        post(data) {
            return resource(apiUrl + 'login/', data, 'POST')
        }
    },
    LogoutResource: {
        post(data) {
            return resource(apiUrl + 'logout/', data, 'POST')
        }
    },
    RegistrationResource: {
        post(data) {
            return resource(apiUrl + 'registration', data, 'POST')
        }
    },
    TaskResource: {
        get(data) {
            let slug = data && data.slug ? data.slug + '/' : '';
            return resource(apiUrl + 'task/' + slug)
        },
        save(data) {
            let slug = data && data.slug ? data.slug + '/' : '';
            return resource(apiUrl + 'task/' + slug, data, 'POST')
        },
        update(data) {
            let slug = data && data.slug ? data.slug + '/' : '';
            return resource(apiUrl + 'task/' + slug, data, 'PUT')
        },
        del(data) {
            let slug = data && data.slug ? data.slug + '/' : '';
            return resource(apiUrl + 'task/' + slug, data, 'DELETE')
        }
    },
    TaskLogsResource: {
        get(data) {
            let slug = data && data.slug ? data.slug : '',
                log = data && data.log ? data.log + '/' : '';
            return resource(`${apiUrl}task/${data.slug}/log/${log}`)
        }
    }
}
