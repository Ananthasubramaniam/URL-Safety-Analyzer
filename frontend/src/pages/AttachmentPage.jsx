import React from 'react';
import { FileText } from 'lucide-react';

const AttachmentPage = () => {
    return (
        <div className="container main-content col-center animate-fade-in">
            <div className="placeholder-card">
                <FileText className="placeholder-icon" size={48} />
                <h1 className="page-title">File Attachment Scanner</h1>
                <p className="page-subtitle">
                    Upload suspicious files to scan for malware and hidden execution vectors.
                </p>
                <div style={{ color: 'var(--accent-primary)', fontWeight: '600', marginTop: 'var(--spacing-md)' }}>
                    Coming Soon
                </div>
            </div>
        </div>
    );
};

export default AttachmentPage;
