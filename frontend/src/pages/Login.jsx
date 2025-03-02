import React from "react";
import { Link } from "react-router-dom";
import './Login.css'
import email_icon from '../assets/icons/email.png'
import password_icon from '../assets/icons/password.png'
import user_icon from '../assets/icons/username.png'

const Login = () => {
    return(
<>
    <div className="container">
            <div className="header">
            <div className="text">
                <h1>Login</h1>
                <img src={user_icon} alt = "usericon" className = "icon"></img>
            </div>
            
            <div className="underline"></div>
        </div>
        
        <div className="input-group">
            <div className="input">
                <img src={email_icon} alt="email" className="icon"/>
                <input type="text" placeholder="Email"/>
            </div>        
        </div>
        <div className="input-group">
            <div className="input">
                <img src={password_icon} alt="password" className="icon"/>
                <input type="password" placeholder="Password"/>
            </div>        
        </div>

        <div className="submit-container">
        <button className="login-button">
            <svg viewBox="0 0 30 30">  
                <line x1="6" y1="15" x2="24" y2="15" stroke-linecap="round" />
                <polyline points="16 7 24 15 16 23" stroke-linecap="round" />
            </svg>
        </button>

        </div>
            <Link to="/signup">Create Account</Link>
        </div>
</>
        
    );
}
export default Login;