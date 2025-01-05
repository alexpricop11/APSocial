import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000/',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor pentru cereri
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptor pentru răspunsuri
apiClient.interceptors.response.use(
    (response) => {
        // Verifică dacă răspunsul conține un nou token
        if (response.data && response.data.new_token) {
            localStorage.setItem('token', response.data.new_token);
        }
        return response;
    },
    (error) => {
        // Gestionează erorile
        if (error.response && error.response.status === 401) {
            // Token invalid sau expirat
            localStorage.removeItem('token'); // Șterge token-ul expirat
            window.location.href = '/auth'; // Redirecționează către pagina de autentificare
        }
        return Promise.reject(error);
    }
);

export default apiClient;