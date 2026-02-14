import { useState } from 'react'
import axios from 'axios'
import './Analyzer.css'

function TextAnalyzer({ onAnalyze }) {
    const [text, setText] = useState('')
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)

    const handleAnalyze = async () => {
        if (!text.trim()) {
            alert('Please enter text to analyze')
            return
        }

        setLoading(true)
        setResult(null)

        try {
            const response = await axios.post('/api/analyze/text', { text })
            setResult(response.data)
            onAnalyze(response.data.is_safe)
        } catch (error) {
            console.error('Error analyzing text:', error)
            alert('Error analyzing text. Make sure ML service is running!')
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
            <h2>🤖 AI Text Analysis</h2>
            <p className="description">
                Detect toxic, hateful, threatening, and abusive content using advanced NLP models
            </p>

            <div className="input-section">
                <textarea
                    className="text-input"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Enter text to analyze for toxic content, threats, hate speech, and more..."
                    rows={6}
                />

                <button
                    className="btn-primary"
                    onClick={handleAnalyze}
                    disabled={loading}
                >
                    {loading ? '🔍 Analyzing...' : '🚀 Analyze Text'}
                </button>
            </div>

            {loading && (
                <div className="loading">
                    <div className="spinner"></div>
                    <p>AI is analyzing the content...</p>
                </div>
            )}

            {result && !loading && (
                <div className={`result-card fade-in ${getThreatClass(result.threat_level)}`}>
                    <div className="result-header">
                        <h3>
                            {result.is_safe ? '✅ Safe Content' : '⚠️ Threat Detected'}
                        </h3>
                        <span className={`badge ${getThreatClass(result.threat_level)}`}>
                            {result.threat_level.toUpperCase()}
                        </span>
                    </div>

                    <div className="result-details">
                        <div className="score-section">
                            <div className="overall-score">
                                <span className="score-label">Overall Threat Score</span>
                                <span className="score-value">{(result.overall_score * 100).toFixed(1)}%</span>
                            </div>
                        </div>

                        <div className="categories">
                            <h4>Category Breakdown</h4>
                            {Object.entries(result.categories).map(([category, score]) => (
                                <div key={category} className="category-item">
                                    <div className="category-header">
                                        <span className="category-name">{category.replace('_', ' ')}</span>
                                        <span className="category-score">{(score * 100).toFixed(1)}%</span>
                                    </div>
                                    <div className="progress-bar">
                                        <div
                                            className="progress-fill"
                                            style={{
                                                width: `${score * 100}%`,
                                                backgroundColor: score > 0.7 ? 'var(--danger)' : score > 0.4 ? 'var(--warning)' : 'var(--success)'
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

export default TextAnalyzer
