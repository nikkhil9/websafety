import { useState } from 'react'
import axios from 'axios'
import './Analyzer.css'

function URLScanner({ onAnalyze }) {
    const [url, setUrl] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)

    const handleScan = async () => {
        if (!url.trim()) {
            alert('Please enter a URL to scan')
            return
        }

        setLoading(true)
        setResult(null)

        try {
            const response = await axios.post('/api/analyze/url', { url })
            setResult(response.data)
            onAnalyze(response.data.is_safe)
        } catch (error) {
            console.error('Error scanning URL:', error)
            alert('Error scanning URL. Make sure ML service is running!')
        } finally {
            setLoading(false)
        }
    }

    const getThreatClass = (level) => {
        switch (level) {
            case 'safe': return 'safe'
            case 'low': return 'warning'  // Orange for low threat
            case 'medium': return 'warning'  // Orange for medium threat
            case 'high': return 'danger'  // Red for high threat
            default: return ''
        }
    }

    return (
        <div className="analyzer">
            <h2>🔍 URL Security Scanner</h2>
            <p className="description">
                Detect phishing, malware, and suspicious URLs using intelligent analysis
            </p>

            <div className="input-section">
                <input
                    type="text"
                    className="url-input"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    placeholder="https://example.com"
                    onKeyPress={(e) => e.key === 'Enter' && handleScan()}
                />

                <button
                    className="btn-primary"
                    onClick={handleScan}
                    disabled={loading}
                >
                    {loading ? '🔍 Scanning...' : '🚀 Scan URL'}
                </button>
            </div>

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                    <p>Analyzing URL security...</p>
                </div>
            )}

            {result && !loading && (
                <div className={`result-card fade-in ${getThreatClass(result.threat_level)}`}>
                    <div className="result-header">
                        <h3>
                            {result.is_safe ? '✅ URL Appears Safe' : '⚠️ Suspicious URL Detected'}
                        </h3>
                        <span className={`badge ${getThreatClass(result.threat_level)}`}>
                            {result.threat_level.toUpperCase()}
                        </span>
                    </div>

                    <div className="result-details">
                        <div className="score-section">
                            <div className="overall-score">
                                <span className="score-label">Threat Score</span>
                                <span className="score-value">{(result.overall_score * 100).toFixed(1)}%</span>
                            </div>
                        </div>

                        <div className="url-info">
                            <h4>URL Information</h4>
                            <div className="info-grid">
                                <div className="info-item">
                                    <span className="info-label">Domain</span>
                                    <span className="info-value">{result.domain_info.domain}</span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">HTTPS</span>
                                    <span className="info-value">
                                        {result.domain_info.has_https ? '✅ Yes' : '❌ No'}
                                    </span>
                                </div>
                                <div className="info-item">
                                    <span className="info-label">URL Length</span>
                                    <span className="info-value">{result.domain_info.url_length} chars</span>
                                </div>
                            </div>
                        </div>

                        <div className="categories">
                            <h4>Threat Categories</h4>
                            {Object.entries(result.categories).map(([category, score]) => (
                                <div key={category} className="category-item">
                                    <div className="category-header">
                                        <span className="category-name">{category}</span>
                                        <span className="category-score">{(score * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="progress-bar">
                                        <div
                                            className="progress-fill"
                                            style={{
                                                width: `${score * 100}%`,
                                                backgroundColor: category === 'safe'
                                                    ? (score > 0.7 ? 'var(--success)' : score > 0.4 ? 'var(--warning)' : 'var(--danger)')
                                                    : (score > 0.7 ? 'var(--danger)' : score > 0.4 ? 'var(--warning)' : 'var(--success)')
                                            }}
                                        />
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default URLScanner
