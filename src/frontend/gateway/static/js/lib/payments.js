import { csrftoken } from './cookies';

async function chargePaymentMethod(data) {
    const body = JSON.stringify(data);

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

export { chargePaymentMethod }
