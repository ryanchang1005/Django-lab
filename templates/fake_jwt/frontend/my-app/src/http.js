
export default class ApiService {
    makeRequest(method, path, data) {
        const accessToken = "";
        const headers = {
            "Content-Type": "application/json",
            "Authorization": "",
        }
        const host = `http://localhost:8000/`
        const fullUrl = `${host}${path}`
        if (method === "POST") {

        } else {

        }

    }

    login(username, password) {
        const data = {
            username: username,
            password: password,
        }
        const url = `http://localhost:8000/api/users/login/`
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log(`data`);
                console.log(data);
            })
    }
}