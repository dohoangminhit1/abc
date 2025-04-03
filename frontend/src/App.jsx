import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Login from './pages/Login.jsx';
import SignUp from './pages/SignUp.jsx';
import Hello from './pages/Hello.jsx';
function App() {
    return (
        <div>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/hello" element={<Hello />} />
            </Routes>
        </div>
    );
}

export default App;