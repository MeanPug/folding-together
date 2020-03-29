async function chargeToken(token, data) {
  const body = JSON.stringify(Object.assign({}, { token: token.id }, data));

  const response = await fetch('/donate/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body
  });

  return response.json();
}

export { chargeToken }
