import React from 'react';
import { History } from 'lucide-react';

const HistoryPage = () => {
    return (
        <div className="container main-content col-center animate-fade-in">
            <div className="placeholder-card">
                <History className="placeholder-icon" size={48} />
                <h1 className="page-title">Scan History</h1>
                <p className="page-subtitle">
                    Your recent analysis history will appear here. Track past scans and monitor threats over time.
                </p>
            </div>
        </div>
    );
};

export default HistoryPage;
