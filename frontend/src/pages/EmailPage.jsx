import React from 'react';
import EmailForm from '../components/EmailForm';

import { Mail } from 'lucide-react';

const EmailPage = () => {
    return (
        <div className="container main-content col-center animate-fade-in">
            <div className="text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <div className="flex-center" style={{ marginBottom: 'var(--spacing-md)', color: 'var(--accent-primary)' }}>
                    <Mail size={64} />
                </div>
                <h1 className="page-title">
                    Email Security Scan
                </h1>
                <p className="page-subtitle">
                    Analyze email headers and body content for phishing indicators.
                </p>
            </div>
            <EmailForm />
        </div>
    );
};

export default EmailPage;
