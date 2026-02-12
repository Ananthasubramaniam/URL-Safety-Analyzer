import React, { useState, useEffect } from 'react';
import { History, Shield, ShieldAlert, ShieldX, Clock, Loader2 } from 'lucide-react';
import { getHistory } from '../services/api';

const HistoryPage = () => {
    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const data = await getHistory();
                setHistory(data);
            } catch (err) {
                setError('Failed to load history items.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchHistory();
    }, []);

    const getStatusInfo = (verdict) => {
        switch (verdict.toLowerCase()) {
            case 'safe':
                return { icon: <Shield className="text-safe" size={18} />, className: 'text-safe', bg: 'rgba(22, 163, 74, 0.1)' };
            case 'suspicious':
                return { icon: <ShieldAlert className="text-suspicious" size={18} />, className: 'text-suspicious', bg: 'rgba(217, 119, 6, 0.1)' };
            case 'phishing':
            case 'danger':
            case 'malicious':
                return { icon: <ShieldX className="text-danger" size={18} />, className: 'text-danger', bg: 'rgba(220, 38, 38, 0.1)' };
            default:
                return { icon: <Shield size={18} />, className: '', bg: 'var(--bg-tertiary)' };
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    };

    if (loading) {
        return (
            <div className="container main-content flex-center">
                <div className="col-center">
                    <Loader2 className="animate-spin text-accent-primary" size={48} />
                    <p style={{ marginTop: 'var(--spacing-md)', color: 'var(--text-secondary)' }}>Loading scan history...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container main-content animate-fade-in" style={{ maxWidth: '1000px' }}>
            <div className="text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <div className="flex-center" style={{ marginBottom: 'var(--spacing-md)', color: 'var(--accent-primary)' }}>
                    <History size={64} />
                </div>
                <h1 className="page-title">Scan History</h1>
                <p className="page-subtitle">
                    Review your recent URL safety analyzes and track detected threats.
                </p>
            </div>

            {error && (
                <div style={{
                    padding: 'var(--spacing-md)',
                    backgroundColor: 'rgba(220, 38, 38, 0.1)',
                    border: '1px solid var(--status-danger)',
                    borderRadius: 'var(--radius-md)',
                    color: 'var(--status-danger)',
                    marginBottom: 'var(--spacing-lg)'
                }}>
                    {error}
                </div>
            )}

            {!loading && history.length === 0 ? (
                <div className="placeholder-card">
                    <History className="placeholder-icon" size={48} />
                    <h2 style={{ fontSize: '1.25rem', fontWeight: '700', marginBottom: 'var(--spacing-sm)' }}>No history found</h2>
                    <p className="page-subtitle" style={{ margin: '0 auto' }}>
                        You haven't performed any scans yet. Start by analyzing a URL or email.
                    </p>
                </div>
            ) : (
                <div style={{
                    backgroundColor: 'var(--bg-secondary)',
                    borderRadius: 'var(--radius-lg)',
                    border: '1px solid var(--border-color)',
                    overflow: 'hidden',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead style={{ backgroundColor: 'var(--bg-tertiary)', fontSize: '0.875rem' }}>
                            <tr>
                                <th style={{ padding: 'var(--spacing-md) var(--spacing-lg)', fontWeight: '600', color: 'var(--text-secondary)' }}>URL / RESOURCE</th>
                                <th style={{ padding: 'var(--spacing-md)', fontWeight: '600', color: 'var(--text-secondary)' }}>VERDICT</th>
                                <th style={{ padding: 'var(--spacing-md)', fontWeight: '600', color: 'var(--text-secondary)', textAlign: 'center' }}>SCORE</th>
                                <th style={{ padding: 'var(--spacing-md) var(--spacing-lg)', fontWeight: '600', color: 'var(--text-secondary)', textAlign: 'right' }}>DATE</th>
                            </tr>
                        </thead>
                        <tbody>
                            {history.map((item, index) => {
                                const status = getStatusInfo(item.verdict);
                                return (
                                    <tr key={index} style={{ borderBottom: index < history.length - 1 ? '1px solid var(--border-color)' : 'none', transition: 'background-color 0.2s' }}>
                                        <td style={{ padding: 'var(--spacing-md) var(--spacing-lg)' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
                                                <div style={{
                                                    maxWidth: '400px',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis',
                                                    whiteSpace: 'nowrap',
                                                    fontSize: '0.95rem',
                                                    fontWeight: '500'
                                                }}>
                                                    {item.url}
                                                </div>
                                            </div>
                                        </td>
                                        <td style={{ padding: 'var(--spacing-md)' }}>
                                            <div style={{
                                                display: 'inline-flex',
                                                alignItems: 'center',
                                                gap: 'var(--spacing-xs)',
                                                padding: '4px 12px',
                                                borderRadius: '20px',
                                                backgroundColor: status.bg,
                                                fontSize: '0.75rem',
                                                fontWeight: '700',
                                                textTransform: 'uppercase'
                                            }} className={status.className}>
                                                {status.icon}
                                                {item.verdict}
                                            </div>
                                        </td>
                                        <td style={{ padding: 'var(--spacing-md)', textAlign: 'center' }}>
                                            <span style={{ fontWeight: '700', fontSize: '1.1rem' }} className={status.className}>
                                                {item.score}
                                            </span>
                                        </td>
                                        <td style={{ padding: 'var(--spacing-md) var(--spacing-lg)', textAlign: 'right', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 'var(--spacing-xs)' }}>
                                                <Clock size={14} />
                                                {formatDate(item.created_at)}
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default HistoryPage;
