import './Stats.css'

function Stats({ stats }) {
    return (
        <div className="stats-grid">
            <div className="stat-card">
                <div className="stat-icon">📊</div>
                <div>
                    <div className="stat-value">{stats.totalScans}</div>
                    <div className="stat-label">Total Scans</div>
                </div>
            </div>

            <div className="stat-card success">
                <div className="stat-icon">✅</div>
                <div>
                    <div className="stat-value">{stats.safeContent}</div>
                    <div className="stat-label">Safe Content</div>
                </div>
            </div>

            <div className="stat-card danger">
                <div className="stat-icon">⚠️</div>
                <div>
                    <div className="stat-value">{stats.threatsDetected}</div>
                    <div className="stat-label">Threats Detected</div>
                </div>
            </div>
        </div>
    )
}

export default Stats
