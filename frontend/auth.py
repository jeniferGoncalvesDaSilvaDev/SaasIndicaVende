import requests
import streamlit as st
import os

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def login(email: str, password: str):
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor: {e}")
        return None

def logout():
    st.session_state.user = None

def get_current_user():
    return st.session_state.get('user')

def make_authenticated_request(endpoint: str, method: str = "GET", data: dict = None):
    user = get_current_user()
    if not user:
        return None
    
    headers = {"X-User-Email": user.get('email')}
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers)
        
        return response
    except Exception as e:
        st.error(f"Erro ao conectar com o servidor: {e}")
        return None
