import React from 'react';

const LinkPieChart = ({ data }) => {
    // Expect data = { "Safe": 10, "Suspicious": 5, "Phishing": 2 }

    const total = Object.values(data).reduce((a, b) => a + b, 0);

    if (total === 0) {
        return (
            <div className="pie-chart-container empty">
                <div className="pie-chart-placeholder">No Data</div>
            </div>
        );
    }

    // Calculate percentages for conic-gradient
    // Colors: Safe=Green, Suspicious=Amber, Phishing=Red
    const safeCount = data['Safe'] || 0;
    const suspiciousCount = data['Suspicious'] || 0;
    const phishingCount = (data['Phishing / Unsafe'] || 0) + (data['Phishing'] || 0); // Handle variety of labels if needed

    const safeDeg = (safeCount / total) * 360;
    const suspiciousDeg = (suspiciousCount / total) * 360;
    const phishingDeg = (phishingCount / total) * 360;

    // Conic Gradient Logic
    // safe starts at 0, ends at safeDeg
    // suspicious starts at safeDeg, ends at safeDeg + suspiciousDeg
    // phishing starts at safeDeg + suspiciousDeg, ends at 360

    const gradient = `conic-gradient(
        var(--status-safe) 0deg ${safeDeg}deg,
        var(--status-suspicious) ${safeDeg}deg ${safeDeg + suspiciousDeg}deg,
        var(--status-danger) ${safeDeg + suspiciousDeg}deg 360deg
    )`;

    return (
        <div className="pie-chart-wrapper" style={{ display: 'flex', gap: '2rem', alignItems: 'center', justifyContent: 'center' }}>
            <div
                className="pie-chart"
                style={{
                    width: '200px',
                    height: '200px',
                    borderRadius: '50%',
                    background: gradient,
                    position: 'relative',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}
            />

            <div className="legend" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                <div className="legend-item" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: 'var(--status-safe)' }}></div>
                    <span>Safe ({safeCount})</span>
                </div>
                <div className="legend-item" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: 'var(--status-suspicious)' }}></div>
                    <span>Suspicious ({suspiciousCount})</span>
                </div>
                <div className="legend-item" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: 'var(--status-danger)' }}></div>
                    <span>Phishing / Unsafe ({phishingCount})</span>
                </div>
            </div>
        </div>
    );
};

export default LinkPieChart;
