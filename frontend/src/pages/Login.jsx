import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import './Login.css'
import password_icon from '../assets/icons/password.png'
import user_icon from '../assets/icons/username.png'
import axios_instance, { API_URL } from '../services/api';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    // console.log(API_URL);

    const handleLogin = async (e) => {
        e.preventDefault();
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);
        try {
            const response = await axios_instance.post(`/auth/login`, params, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            });

            localStorage.setItem('access_token', response.data.access_token);
            alert(response.data.message);
            navigate('/hello');
        } catch (error) {
            alert(error.response?.data?.detail || "An error occurred during login.");
            console.error("Login error:", error.response || error.message || error);
        }
    };

    return(
        <>
            <div className="container">
                <div className="header">
                    <div className="text">
                        <h1>Login</h1>
                        <img src={user_icon} alt="usericon" className="icon"></img>
                    </div>
                    
                    <div className="underline"></div>
                </div>
                
                <form onSubmit={handleLogin}>
                    <div className="input-group">
                        <div className="input">
                            <img src={user_icon} alt="username" className="icon"/>
                            <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required/>
                        </div>        
                    </div>
                    <div className="input-group">
                        <div className="input">
                            <img src={password_icon} alt="password" className="icon"/>
                            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required/>
                        </div>        
                    </div>
                    <div className="submit-container">
                        <button type="submit" className="login-button">
                            <svg viewBox="0 0 30 30">  
                                <line x1="6" y1="15" x2="24" y2="15" strokeLinecap="round" />
                                <polyline points="16 7 24 15 16 23" strokeLinecap="round" />
                            </svg>
                        </button>
                    </div>
                </form>
                <Link to="/signup">Create Account</Link>
            </div>
        </>
    );
}

export default Login;