import './Header.css'

function Header() {
    return (
        <header className="header">
            <div className="container">
                <div className="header-content">
                    <div className="logo">
                        <span className="logo-icon">🛡️</span>
                        <div>
                            <h1>Web Safety</h1>
                            <p className="tagline">AI-Powered Content Protection</p>
                        </div>
                    </div>
                    <div className="status">
                        <span className="status-dot"></span>
                        <span>ML Service Active</span>
                    </div>
                </div>
            </div>
        </header>
    )
}

export default Header
