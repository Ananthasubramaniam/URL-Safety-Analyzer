import React from 'react';
import { AlertTriangle, CheckCircle, ShieldAlert, Info, ShieldCheck, ShieldX, Activity } from 'lucide-react';

const ResultCard = ({ result }) => {
    if (!result) return null;

    const { score, verdict, breakdown, reasons, recommendations, ml_probability } = result;

    const getVerdictClass = (v) => {
        const lowerV = v.toLowerCase();
        if (lowerV === 'safe') return 'text-safe';
        if (lowerV === 'suspicious') return 'text-suspicious';
        if (lowerV === 'unsafe' || lowerV.includes('danger') || lowerV.includes('phishing')) return 'text-danger';
        return 'text-secondary';
    };

    const getVerdictIcon = (v) => {
        const lowerV = v.toLowerCase();
        const size = 32;
        if (lowerV === 'safe') return <ShieldCheck className="text-safe" size={size} />;
        if (lowerV === 'suspicious') return <AlertTriangle className="text-suspicious" size={size} />;
        if (lowerV.includes('unsafe') || lowerV.includes('danger') || lowerV.includes('phishing')) return <ShieldX className="text-danger" size={size} />;
        return <Info className="text-secondary" size={size} />;
    };

    return (
        <div className="result-card animate-fade-in" style={{ maxWidth: '800px' }}>
            {/* Header: Score and Verdict */}
            <div className="card-header" style={{ paddingBottom: 'var(--spacing-lg)', borderBottom: '1px solid var(--border-color)' }}>
                <div className="verdict-container">
                    {getVerdictIcon(verdict)}
                    <div className="verdict-label">
                        <span className={`verdict-title ${getVerdictClass(verdict)}`} style={{ fontSize: '1.5rem' }}>{verdict}</span>
                        <span className="verdict-subtitle">Security Analysis Result</span>
                    </div>
                </div>

                <div className="score-container" style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', lineHeight: '1' }} className={getVerdictClass(verdict)}>
                        {score}
                    </div>
                    <span className="score-label" style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Risk Score / 100</span>
                </div>
            </div>

            <div className="card-body" style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1.5fr) minmax(0, 1fr)', gap: 'var(--spacing-xl)', paddingTop: 'var(--spacing-lg)' }}>
                {/* Left Column: Reasons and Recommendations */}
                <div className="risk-details">
                    <section style={{ marginBottom: 'var(--spacing-lg)' }}>
                        <h3 className="details-title" style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1rem', marginBottom: 'var(--spacing-md)' }}>
                            <Activity size={18} className="text-accent-primary" />
                            Risk Indicators
                        </h3>
                        <ul className="details-list" style={{ listStyle: 'none', padding: 0 }}>
                            {reasons && reasons.length > 0 ? (
                                reasons.map((reason, index) => (
                                    <li key={index} className="detail-item" style={{ display: 'flex', gap: '8px', marginBottom: '8px', fontSize: '0.9rem' }}>
                                        <span style={{ marginTop: '6px', minWidth: '6px', height: '6px', borderRadius: '50%', backgroundColor: 'var(--accent-primary)' }}></span>
                                        <span>{reason}</span>
                                    </li>
                                ))
                            ) : (
                                <li className="detail-item">No specific risk indicators found.</li>
                            )}
                        </ul>
                    </section>

                    <section>
                        <h3 className="details-title" style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '1rem', marginBottom: 'var(--spacing-md)', color: 'var(--status-safe)' }}>
                            <ShieldCheck size={18} />
                            Safety Advice
                        </h3>
                        <div style={{ backgroundColor: 'var(--bg-tertiary)', padding: 'var(--spacing-md)', borderRadius: 'var(--radius-md)', fontSize: '0.85rem' }}>
                            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                                {recommendations && recommendations.length > 0 ? (
                                    recommendations.map((rec, index) => (
                                        <li key={index} style={{ marginBottom: '8px', display: 'flex', gap: '8px' }}>
                                            <span style={{ color: 'var(--status-safe)' }}>•</span>
                                            {rec}
                                        </li>
                                    ))
                                ) : (
                                    <li>Always be cautious with unfamiliar links.</li>
                                )}
                            </ul>
                        </div>
                    </section>
                </div>

                {/* Right Column: Breakdown and ML */}
                <div className="risk-breakdown">
                    <h3 className="details-title" style={{ fontSize: '1rem', marginBottom: 'var(--spacing-md)' }}>Structure Analysis</h3>

                    {breakdown && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)', marginBottom: 'var(--spacing-lg)' }}>
                            {Object.entries(breakdown).map(([key, value]) => (
                                <div key={key}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', marginBottom: '4px', textTransform: 'capitalize' }}>
                                        <span className="text-secondary">
                                            {key === 'virustotal' ? 'VirusTotal Analysis' :
                                                key === 'ml' ? 'Machine Learning Analysis' :
                                                    key === 'network' ? 'Network Validation' :
                                                        key === 'pattern' ? 'Pattern Analysis' :
                                                            key === 'blacklist' ? 'Blacklist' :
                                                                `${key} Analysis`}
                                        </span>
                                        <span className="font-bold">{value}%</span>
                                    </div>
                                    <div className="progress-bar-bg" style={{ height: '6px' }}>
                                        <div
                                            className="progress-bar-fill"
                                            style={{
                                                width: `${value}%`,
                                                height: '100%',
                                                backgroundColor: value > 60 ? 'var(--status-danger)' : value > 30 ? 'var(--status-suspicious)' : 'var(--status-safe)'
                                            }}
                                        ></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
};

export default ResultCard;
