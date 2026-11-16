const statusBox = document.getElementById('statusBox');
const responseOutput = document.getElementById('responseOutput');
const balanceOutput = document.getElementById('balanceOutput');

let token = '';

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.style.borderColor = isError ? 'rgba(255, 125, 125, 0.7)' : 'rgba(100, 210, 255, 0.4)';
}

function renderJson(value) {
  responseOutput.textContent = JSON.stringify(value, null, 2);
}

async function apiRequest(url, options = {}) {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });

  const text = await response.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!response.ok) {
    throw new Error(data?.detail ? JSON.stringify(data.detail) : text || 'Request failed');
  }

  return data;
}

document.getElementById('registerForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = Object.fromEntries(form.entries());
  payload.date_of_birth = new Date(payload.date_of_birth).toISOString().slice(0, 10);

  try {
    setStatus('Registering user...');
    const result = await apiRequest('/onboarding-service/create/user', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    if (result.development_otp) {
      document.querySelector('#otpForm [name="email"]').value = payload.email;
      document.querySelector('#otpForm [name="otp"]').value = result.development_otp;
    }
    renderJson(result);
    setStatus('User registered. Please validate OTP.');
  } catch (error) {
    renderJson({ error: error.message });
    setStatus(error.message, true);
  }
});

document.getElementById('otpForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = Object.fromEntries(form.entries());

  try {
    setStatus('Validating OTP...');
    const result = await apiRequest('/onboarding-service/validate/otp', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    renderJson(result);
    setStatus('OTP verified');
  } catch (error) {
    renderJson({ error: error.message });
    setStatus(error.message, true);
  }
});

document.getElementById('loginForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const payload = Object.fromEntries(form.entries());

  try {
    setStatus('Logging in...');
    const result = await apiRequest('/onboarding-service/user/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    token = result.access_token;
    const wallet = await apiRequest('/wallet-service/create', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    });
    renderJson({ login: result, wallet });
    setStatus('Logged in successfully');
  } catch (error) {
    renderJson({ error: error.message });
    setStatus(error.message, true);
  }
});

document.getElementById('balanceBtn').addEventListener('click', async () => {
  if (!token) {
    balanceOutput.textContent = 'Please log in first.';
    setStatus('Missing auth token', true);
    return;
  }

  try {
    setStatus('Fetching balance...');
    const result = await apiRequest('/wallet-service/get/balance', {
      method: 'GET',
      headers: { Authorization: `Bearer ${token}` },
    });
    balanceOutput.textContent = JSON.stringify(result, null, 2);
    renderJson(result);
    setStatus('Balance loaded');
  } catch (error) {
    balanceOutput.textContent = error.message;
    renderJson({ error: error.message });
    setStatus(error.message, true);
  }
});

document.getElementById('transferForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  if (!token) {
    renderJson({ error: 'Please log in before transferring.' });
    setStatus('Missing auth token', true);
    return;
  }

  const form = new FormData(event.currentTarget);
  const payload = Object.fromEntries(form.entries());

  try {
    setStatus('Sending transfer...');
    const result = await apiRequest('/txn-service/initiate/transaction', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload),
    });
    renderJson(result);
    setStatus('Transfer initiated');
  } catch (error) {
    renderJson({ error: error.message });
    setStatus(error.message, true);
  }
});
