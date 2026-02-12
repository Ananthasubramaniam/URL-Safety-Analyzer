import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LayoutDashboard, Activity, AlertTriangle, CheckCircle, ShieldAlert } from 'lucide-react';
import LinkPieChart from '../components/LinkPieChart';

const DashboardPage = () => {
    const [summary, setSummary] = useState(null);
    const [distribution, setDistribution] = useState(null);
    const [recent, setRecent] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [summaryRes, distRes, recentRes] = await Promise.all([
                    axios.get('http://localhost:8000/api/dashboard/summary'),
                    axios.get('http://localhost:8000/api/dashboard/distribution'),
                    axios.get('http://localhost:8000/api/dashboard/recent')
                ]);

                setSummary(summaryRes.data);
                setDistribution(distRes.data);
                setRecent(recentRes.data);
            } catch (error) {
                console.error("Dashboard data fetch failed", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="container main-content flex-center">
                <div className="animate-spin" style={{ border: '4px solid var(--bg-tertiary)', borderTop: '4px solid var(--accent-primary)', borderRadius: '50%', width: '40px', height: '40px' }}></div>
            </div>
        );
    }

    return (
        <div className="container main-content animate-fade-in">
            <div className="text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <div className="flex-center" style={{ marginBottom: 'var(--spacing-md)', color: 'var(--accent-primary)' }}>
                    <LayoutDashboard size={64} />
                </div>
                <h1 className="page-title">Analytics Dashboard</h1>
                <p className="page-subtitle">Overview of threat detection activity and recent scans.</p>
            </div>

            {/* Summary Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--spacing-lg)', marginBottom: 'var(--spacing-xl)' }}>
                <div className="card" style={{ padding: 'var(--spacing-lg)', textAlign: 'center' }}>
                    <div style={{ color: 'var(--text-secondary)', marginBottom: 'var(--spacing-sm)' }}>Total Scans</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--text-primary)' }}>{summary?.total_scans || 0}</div>
                </div>
                <div className="card" style={{ padding: 'var(--spacing-lg)', textAlign: 'center', borderTop: '4px solid var(--status-safe)' }}>
                    <div style={{ color: 'var(--status-safe)', marginBottom: 'var(--spacing-sm)', fontWeight: '600' }}>Safe URLs</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--text-primary)' }}>{summary?.safe || 0}</div>
                </div>
                <div className="card" style={{ padding: 'var(--spacing-lg)', textAlign: 'center', borderTop: '4px solid var(--status-suspicious)' }}>
                    <div style={{ color: 'var(--status-suspicious)', marginBottom: 'var(--spacing-sm)', fontWeight: '600' }}>Suspicious</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--text-primary)' }}>{summary?.suspicious || 0}</div>
                </div>
                <div className="card" style={{ padding: 'var(--spacing-lg)', textAlign: 'center', borderTop: '4px solid var(--status-danger)' }}>
                    <div style={{ color: 'var(--status-danger)', marginBottom: 'var(--spacing-sm)', fontWeight: '600' }}>Phishing / Unsafe</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: '800', color: 'var(--text-primary)' }}>{summary?.phishing || 0}</div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--spacing-xl)', alignItems: 'start' }}>

                {/* Distribution Chart */}
                <div className="card" style={{ padding: 'var(--spacing-xl)' }}>
                    <h2 className="section-title" style={{ marginBottom: 'var(--spacing-lg)', textAlign: 'center' }}>Verdict Distribution</h2>
                    {distribution ? <LinkPieChart data={distribution} /> : <p className="text-center">No data available</p>}
                </div>

                {/* Recent Threats */}
                <div className="card" style={{ padding: 'var(--spacing-xl)' }}>
                    <h2 className="section-title" style={{ marginBottom: 'var(--spacing-lg)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <ShieldAlert size={20} className="text-danger" /> Recent Threats
                    </h2>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
                        {recent.length === 0 ? (
                            <p className="text-center text-secondary">No recent threats detected.</p>
                        ) : (
                            recent.map((item, index) => (
                                <div key={index} style={{
                                    padding: 'var(--spacing-md)',
                                    border: '1px solid var(--border-color)',
                                    borderRadius: 'var(--radius-sm)',
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    backgroundColor: 'var(--bg-tertiary)'
                                }}>
                                    <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', maxWidth: '70%' }}>
                                        <div style={{ fontWeight: '600', fontSize: '0.9rem' }}>{item.url}</div>
                                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                                            {new Date(item.time).toLocaleString()}
                                        </div>
                                    </div>
                                    <div className={`status-badge status-${(item.verdict || 'unknown').toLowerCase().split(' ')[0]}`}>
                                        {item.score}
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
};

export default DashboardPage;
