import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import './SignUp.css'
import password_icon from '../assets/icons/password.png'
import user_icon from '../assets/icons/username.png'
import axios_instance from '../services/api';

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [retypePassword, setRetypePassword] = useState('');
    const navigate = useNavigate();

    const handleSignUp = async (e) => {
        e.preventDefault();
        if (password !== retypePassword) {
            alert("Passwords do not match");
            return;
        }
        try {
            const response = await axios_instance.post('/register', {
                username,
                password
            });
            alert(response.data.message);
            navigate('/login');
        } catch (error) {
            alert(error.response.data.detail);
        }
    };

    return(
        <>
            <div className="container">
                <div className="header">
                    <div className="text">
                        <h1>Sign Up</h1>
                        <img src={user_icon} alt="usericon" className="icon"></img>
                    </div>
                    
                    <div className="underline"></div>
                </div>
                
                <form onSubmit={handleSignUp}>
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
                    <div className="input-group">
                        <div className="input">
                            <img src={password_icon} alt="retype password" className="icon"/>
                            <input type="password" placeholder="Retype Password" value={retypePassword} onChange={(e) => setRetypePassword(e.target.value)} required/>
                        </div>        
                    </div>
                    <div className="submit-container">
                        <button type="submit" className="login-button">
                            <svg viewBox="0 0 30 30">  
                                <line x1="6" y1="15" x2="24" y2="15" stroke-linecap="round" />
                                <polyline points="16 7 24 15 16 23" stroke-linecap="round" />
                            </svg>
                        </button>
                    </div>
                </form>
                <Link to="/login">Already have an account?</Link>
            </div>
        </>
    );
}

export default SignUp;