import { useState } from 'react'
import axios from 'axios'
import './App.css'
import TextAnalyzer from './components/TextAnalyzer'
import URLScanner from './components/URLScanner'
import ImageAnalyzer from './components/ImageAnalyzer'
import Header from './components/Header'
import Stats from './components/Stats'

const API_BASE = '/api'

function App() {
    const [activeTab, setActiveTab] = useState('text')
    const [stats, setStats] = useState({
        totalScans: 0,
        threatsDetected: 0,
        safeContent: 0
    })

    const updateStats = (isSafe) => {
        setStats(prev => ({
            totalScans: prev.totalScans + 1,
            threatsDetected: isSafe ? prev.threatsDetected : prev.threatsDetected + 1,
            safeContent: isSafe ? prev.safeContent + 1 : prev.safeContent
        }))
    }

    return (
        <div className="app">
            <Header />

            <main className="container">
                <Stats stats={stats} />

                <div className="tabs">
                    <button
                        className={`tab ${activeTab === 'text' ? 'active' : ''}`}
                        onClick={() => setActiveTab('text')}
                    >
                        <span className="icon">📝</span> Text Analysis
                    </button>
                    <button
                        className={`tab ${activeTab === 'url' ? 'active' : ''}`}
                        onClick={() => setActiveTab('url')}
                    >
                        <span className="icon">🔗</span> URL Scanner
                    </button>
                    <button
                        className={`tab ${activeTab === 'image' ? 'active' : ''}`}
                        onClick={() => setActiveTab('image')}
                    >
                        <span className="icon">🖼️</span> Image Safety
                    </button>
                </div>

                <div className="tab-content fade-in">
                    {activeTab === 'text' && <TextAnalyzer onAnalyze={updateStats} />}
                    {activeTab === 'url' && <URLScanner onAnalyze={updateStats} />}
                    {activeTab === 'image' && <ImageAnalyzer onAnalyze={updateStats} />}
                </div>
            </main>

            <footer className="footer">
                <p>© 2026 Web Safety - Final Year Project | AI-Powered Content Protection</p>
            </footer>
        </div>
    )
}

export default App
