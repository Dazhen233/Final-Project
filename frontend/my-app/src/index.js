import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { MusicProvider } from './MusicContext';
import './index.css';
import App from './App';
import SecondPage from './SecondPage';
import ChatPage from './ChatPage';
import reportWebVitals from './reportWebVitals';




const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
   //<React.StrictMode>
    <MusicProvider>
      <Router> {/* 添加 Router 包裹 Routes */}
        <Routes>
          <Route path="/" element={<Navigate to="/welcome" />} />
          <Route path="/welcome" element={<App />} />
          <Route path="/style-choose" element={<SecondPage />} /> 
          <Route path="/chat" element={<ChatPage />} /> 
        </Routes>
      </Router>
    </MusicProvider>
   //</React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
