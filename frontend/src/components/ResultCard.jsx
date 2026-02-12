import React from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert, Info } from 'lucide-react';

const ResultCard = ({ result }) => {
    if (!result) return null;

    const { score, verdict, details, ml_probability } = result;

    const getVerdictClass = (v) => {
        const lowerV = v.toLowerCase();
        if (lowerV === 'safe') return 'text-safe';
        if (lowerV === 'suspicious') return 'text-suspicious';
        if (lowerV === 'unsafe' || lowerV === 'malicious') return 'text-danger';
        return 'text-secondary';
    };

    const getVerdictIcon = (v) => {
        const lowerV = v.toLowerCase();
        const size = 32;
        if (lowerV === 'safe') return <CheckCircle className="text-safe" size={size} />;
        if (lowerV === 'suspicious') return <AlertTriangle className="text-suspicious" size={size} />;
        if (lowerV === 'unsafe' || lowerV === 'malicious') return <ShieldAlert className="text-danger" size={size} />;
        return <Info className="text-secondary" size={size} />;
    };

    return (
        <div className="result-card animate-fade-in">
            <div className="card-header">
                <div className="verdict-container">
                    {getVerdictIcon(verdict)}
                    <div className="verdict-label">
                        <span className={`verdict-title ${getVerdictClass(verdict)}`}>{verdict}</span>
                        <span className="verdict-subtitle">Security Verdict</span>
                    </div>
                </div>

                <div className="score-container">
                    <span className={`score-value ${getVerdictClass(verdict)}`}>{score}</span>
                    <span className="score-label">Safety Score / 100</span>
                </div>
            </div>

            <div className="card-body">
                <h3 className="details-title">
                    <Info size={18} className="text-accent" />
                    Analysis Details
                </h3>

                <ul className="details-list">
                    {details && details.length > 0 ? (
                        details.map((detail, index) => {
                            const isSkipped = detail.includes("skipped") || detail.includes("failed");
                            const isDanger = detail.includes("found") || detail.includes("detected");

                            return (
                                <li key={index} className="detail-item">
                                    <span className={`detail-dot ${isSkipped ? 'bg-warning' : isDanger ? 'bg-danger' : ''}`}
                                        style={isSkipped ? { backgroundColor: 'var(--status-suspicious)' } :
                                            isDanger ? { backgroundColor: 'var(--status-danger)' } : {}}>
                                    </span>
                                    <span style={isSkipped ? { color: 'var(--status-suspicious)' } : {}}>{detail}</span>
                                </li>
                            );
                        })
                    ) : (
                        <li className="detail-item">No specific issues detected.</li>
                    )}
                </ul>

                {ml_probability !== null && ml_probability !== undefined && (
                    <div className="ml-section">
                        <div className="ml-header">
                            <span className="text-secondary">ML Threat Probability</span>
                            <span className="text-primary font-bold">{(ml_probability * 100).toFixed(1)}%</span>
                        </div>
                        <div className="progress-bar-bg">
                            <div
                                className={`progress-bar-fill ${ml_probability > 0.5 ? 'bg-danger' : 'bg-safe'}`}
                                style={{ width: `${ml_probability * 100}%` }}
                            ></div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ResultCard;
