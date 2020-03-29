import { csrftoken } from './cookies';

async function chargeToken(token, data) {
    const body = JSON.stringify(Object.assign({}, {token: token.id}, data));

    const response = await fetch('/donate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body
    });

    return response.json();
}

export { chargeToken }
