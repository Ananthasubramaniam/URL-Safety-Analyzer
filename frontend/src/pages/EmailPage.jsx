import React from 'react';
import EmailForm from '../components/EmailForm';

const EmailPage = () => {
    return (
        <div className="container main-content col-center animate-fade-in">
            <div className="text-center">
                <h1 className="page-title">Email Security Scan</h1>
                <p className="page-subtitle">
                    Analyze email headers and body content for phishing indicators.
                </p>
            </div>
            <EmailForm />
        </div>
    );
};

export default EmailPage;
