import React, { useState } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle, Download, Loader2 } from 'lucide-react';
import axios from 'axios';

const BulkAnalysisPage = () => {
    const [urls, setUrls] = useState('');
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [progress, setProgress] = useState(0);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            const reader = new FileReader();
            reader.onload = (event) => {
                setUrls(event.target.result);
            };
            reader.readAsText(selectedFile);
        }
    };

    const handleAnalyze = async () => {
        const urlList = urls.split('\n').map(u => u.trim()).filter(u => u);
        if (urlList.length === 0) return;

        setLoading(true);
        setResults([]);
        setProgress(0);

        // Client-side batching to report progress
        const batchSize = 10;
        const total = urlList.length;
        let processed = 0;
        const allResults = [];

        try {
            for (let i = 0; i < total; i += batchSize) {
                const batch = urlList.slice(i, i + batchSize);

                // Call backend API
                const response = await axios.post('http://localhost:8000/api/bulk-analyze', batch);

                allResults.push(...response.data);
                processed += batch.length;
                setProgress(Math.round((processed / total) * 100));
            }
            setResults(allResults);
        } catch (error) {
            console.error("Bulk analysis failed", error);
            alert("Analysis failed. See console for details.");
        } finally {
            setLoading(false);
        }
    };

    const downloadCSV = () => {
        if (!results) return;
        const header = "URL,Verdict,Score,Details\n";
        const rows = results.map(r => {
            if (r.error) return `"${r.url}","Error","0","${r.error}"`;
            return `"${r.url}","${r.result.verdict}","${r.result.score}","${r.result.reasons.join('; ')}"`;
        }).join('\n');

        const blob = new Blob([header + rows], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'bulk_scan_results.csv';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    };

    return (
        <div className="container main-content animate-fade-in" style={{ maxWidth: '1000px' }}>
            <div className="text-center" style={{ marginBottom: 'var(--spacing-xl)' }}>
                <div className="flex-center" style={{ marginBottom: 'var(--spacing-md)', color: 'var(--accent-primary)' }}>
                    <FileText size={64} />
                </div>
                <h1 className="page-title">Bulk URL Analysis</h1>
                <p className="page-subtitle">
                    Scan multiple URLs at once. Paste a list or upload a text file.
                </p>
            </div>

            <div className="card" style={{ padding: 'var(--spacing-lg)', marginBottom: 'var(--spacing-xl)' }}>
                <div className="form-group">
                    <label className="form-label">
                        Enter URLs (one per line) or Upload File
                    </label>
                    <textarea
                        className="form-input"
                        rows="10"
                        placeholder="http://example.com&#10;http://test.com"
                        value={urls}
                        onChange={(e) => setUrls(e.target.value)}
                        style={{ fontFamily: 'monospace', fontSize: '0.9rem' }}
                    />
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'var(--spacing-md)' }}>
                    <label className="btn btn-secondary" style={{ cursor: 'pointer' }}>
                        <Upload size={18} /> Upload .txt
                        <input type="file" accept=".txt,.csv" onChange={handleFileChange} style={{ display: 'none' }} />
                    </label>

                    <button
                        className="btn btn-primary"
                        onClick={handleAnalyze}
                        disabled={loading || !urls.trim()}
                    >
                        {loading ? <><Loader2 className="animate-spin" size={18} /> Scanning... {progress}%</> : 'Start Bulk Scan'}
                    </button>
                </div>
            </div>

            {results && (
                <div className="card animate-slide-up" style={{ padding: 'var(--spacing-lg)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--spacing-md)' }}>
                        <h2 className="section-title">Scan Results ({results.length})</h2>
                        <button className="btn btn-outline" onClick={downloadCSV}>
                            <Download size={18} /> Export CSV
                        </button>
                    </div>

                    <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
                        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
                            <thead style={{ position: 'sticky', top: 0, background: 'var(--bg-secondary)', zIndex: 1 }}>
                                <tr>
                                    <th style={{ padding: '12px', textAlign: 'left', borderBottom: '2px solid var(--border-color)' }}>URL</th>
                                    <th style={{ padding: '12px', textAlign: 'center', borderBottom: '2px solid var(--border-color)' }}>Verdict</th>
                                    <th style={{ padding: '12px', textAlign: 'center', borderBottom: '2px solid var(--border-color)' }}>Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                {results.map((r, i) => (
                                    <tr key={i} style={{ borderBottom: '1px solid var(--border-color)' }}>
                                        <td style={{ padding: '12px' }}>{r.url}</td>
                                        <td style={{ padding: '12px', textAlign: 'center' }}>
                                            {r.error ? (
                                                <span style={{ color: 'var(--status-danger)', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                                                    <AlertCircle size={14} /> Error
                                                </span>
                                            ) : (
                                                <span className={`status-badge status-${(r.result.verdict || 'unknown').toLowerCase().split(' ')[0]}`}>
                                                    {r.result.verdict}
                                                </span>
                                            )}
                                        </td>
                                        <td style={{ padding: '12px', textAlign: 'center', fontWeight: 'bold' }}>
                                            {r.error ? '-' : r.result.score}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default BulkAnalysisPage;
