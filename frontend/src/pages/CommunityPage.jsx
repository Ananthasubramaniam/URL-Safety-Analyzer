import React from 'react';
import { Users } from 'lucide-react';

const CommunityPage = () => {
    return (
        <div className="container main-content col-center animate-fade-in">
            <div className="placeholder-card">
                <Users className="placeholder-icon" size={48} />
                <h1 className="page-title">Community Intelligence</h1>
                <p className="page-subtitle">
                    Join thousands of security researchers and users sharing threat intelligence.
                </p>
                <div style={{ color: 'var(--accent-primary)', fontWeight: '600', marginTop: 'var(--spacing-md)' }}>
                    Coming Soon
                </div>
            </div>
        </div>
    );
};

export default CommunityPage;
