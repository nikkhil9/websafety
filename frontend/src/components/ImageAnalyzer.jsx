import { useState } from 'react'
import axios from 'axios'
import './Analyzer.css'

function ImageAnalyzer({ onAnalyze }) {
    const [file, setFile] = useState(null)
    const [preview, setPreview] = useState(null)
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState(null)
    const [dragActive, setDragActive] = useState(false)
    const [fileInfo, setFileInfo] = useState(null)

    // Helper function to resize image
    const resizeImage = (file, maxWidth = 800, maxHeight = 800) => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader()
            reader.onload = (e) => {
                const img = new Image()
                img.onload = () => {
                    const canvas = document.createElement('canvas')
                    let width = img.width
                    let height = img.height

                    // Calculate new dimensions
                    if (width > height) {
                        if (width > maxWidth) {
                            height = (height * maxWidth) / width
                            width = maxWidth
                        }
                    } else {
                        if (height > maxHeight) {
                            width = (width * maxHeight) / height
                            height = maxHeight
                        }
                    }

                    canvas.width = width
                    canvas.height = height

                    const ctx = canvas.getContext('2d')
                    ctx.drawImage(img, 0, 0, width, height)

                    canvas.toBlob((blob) => {
                        const resizedFile = new File([blob], file.name, {
                            type: 'image/jpeg',
                            lastModified: Date.now()
                        })
                        resolve(resizedFile)
                    }, 'image/jpeg', 0.9)
                }
                img.onerror = reject
                img.src = e.target.result
            }
            reader.onerror = reject
            reader.readAsDataURL(file)
        })
    }

    // Validate file
    const validateFile = (file) => {
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        const maxSize = 10 * 1024 * 1024 // 10MB

        if (!validTypes.includes(file.type)) {
            alert('Please upload a valid image file (JPG, PNG, or WebP)')
            return false
        }

        if (file.size > maxSize) {
            alert('File size must be less than 10MB')
            return false
        }

        return true
    }

    const handleFileChange = async (e) => {
        const selectedFile = e.target.files[0]
        if (selectedFile && validateFile(selectedFile)) {
            await processFile(selectedFile)
        }
    }

    const processFile = async (selectedFile) => {
        try {
            // Store file info
            setFileInfo({
                name: selectedFile.name,
                size: selectedFile.size,
                originalSize: selectedFile.size
            })

            // Resize image for faster upload and processing
            setLoading(true)
            const resizedFile = await resizeImage(selectedFile)
            setLoading(false)

            setFile(resizedFile)
            setPreview(URL.createObjectURL(resizedFile))
            setResult(null)

            // Update file info with resized size
            setFileInfo(prev => ({
                ...prev,
                size: resizedFile.size
            }))
        } catch (error) {
            console.error('Error processing image:', error)
            alert('Error processing image. Please try another file.')
            setLoading(false)
        }
    }

    // Drag and drop handlers
    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }

    const handleDrop = async (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0]
            if (validateFile(droppedFile)) {
                await processFile(droppedFile)
            }
        }
    }

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes'
        const k = 1024
        const sizes = ['Bytes', 'KB', 'MB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    }

    const handleAnalyze = async () => {
        if (!file) {
            alert('Please select an image to analyze')
            return
        }

        setLoading(true)
        setResult(null)

        const formData = new FormData()
        formData.append('image', file)

        try {
            const response = await axios.post('/api/analyze/image', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            setResult(response.data)
            onAnalyze(response.data.is_safe)
        } catch (error) {
            console.error('Error analyzing image:', error)
            alert('Error analyzing image. Make sure ML service is running!')
        } finally {
            setLoading(false)
        }
    }

    const getThreatClass = (level) => {
        switch (level) {
            case 'safe': return 'safe'
            case 'low': return 'warning'
            case 'medium': return 'warning'
            case 'high': return 'danger'
            default: return ''
        }
    }

    return (
        <div className="analyzer">
            <h2>🖼️ AI Image Safety Analysis</h2>
            <p className="description">
                Scan images for NSFW, violence, and inappropriate content using Computer Vision
            </p>

            <div className="input-section">
                <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="file-input"
                    id="image-upload"
                    style={{ display: 'none' }}
                />
                <label
                    htmlFor="image-upload"
                    className={`file-drop-area ${dragActive ? 'drag-active' : ''}`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    {preview ? (
                        <div className="image-preview">
                            <img src={preview} alt="Preview" />
                            <p className="change-text">Click to change image or drag new one</p>
                        </div>
                    ) : (
                        <div className="upload-placeholder">
                            <span className="icon">📁</span>
                            <p>Click to upload or drag and drop an image</p>
                            <p style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.7 }}>
                                Supports JPG, PNG, WebP (Max 10MB)
                            </p>
                        </div>
                    )}
                </label>

                {fileInfo && (
                    <div className="file-info">
                        <span className="file-name">📄 {fileInfo.name}</span>
                        <span className="file-size">{formatFileSize(fileInfo.size)}</span>
                        {fileInfo.originalSize !== fileInfo.size && (
                            <span className="file-size" style={{ color: 'var(--success)' }}>
                                (optimized from {formatFileSize(fileInfo.originalSize)})
                            </span>
                        )}
                    </div>
                )}

                <button
                    className="btn-primary"
                    onClick={handleAnalyze}
                    disabled={loading || !file}
                >
                    {loading ? '🔍 Scanning...' : '🚀 Scan Image'}
                </button>
            </div>

            {loading && !result && (
                <div className="loading">
                    <div className="spinner"></div>
                    <p>AI is analyzing your image...</p>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                        This usually takes 2-5 seconds
                    </p>
                </div>
            )}

            {result && !loading && (
                <div className={`result-card fade-in ${getThreatClass(result.threat_level)}`}>
                    <div className="result-header">
                        <h3>
                            {result.is_safe ? '✅ Safe Image' : '⚠️ Unsafe Image Detected'}
                        </h3>
                        <span className={`badge ${getThreatClass(result.threat_level)}`}>
                            {result.threat_level.toUpperCase()}
                        </span>
                    </div>

                    <div className="result-details">
                        <div className="score-section">
                            <div className="overall-score">
                                <span className="score-label">Threat Probability</span>
                                <span className="score-value">{(result.overall_score * 100).toFixed(1)}%</span>
                            </div>
                        </div>

                        <div className="categories">
                            <h4>Analysis Breakdown</h4>
                            {Object.entries(result.categories).map(([category, score]) => {
                                // Determine color based on category and score
                                const isThreatCategory = ['nsfw', 'violence', 'gore'].includes(category)
                                const barColor = isThreatCategory && score > 0.5
                                    ? 'var(--danger)'
                                    : isThreatCategory
                                        ? 'var(--warning)'
                                        : 'var(--success)'

                                return (
                                    <div key={category} className="category-item">
                                        <div className="category-header">
                                            <span className="category-name">{category.toUpperCase()}</span>
                                            <span className="category-score">{(score * 100).toFixed(1)}%</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div
                                                className="progress-fill"
                                                style={{
                                                    width: `${score * 100}%`,
                                                    backgroundColor: barColor
                                                }}
                                            />
                                        </div>
                                    </div>
                                )
                            })}
                            {result.models && (
                                <div className="model-info">
                                    <small>Models: {Object.values(result.models).join(' + ')}</small>
                                </div>
                            )}
                            {result.model && (
                                <div className="model-info">
                                    <small>Model: {result.model}</small>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ImageAnalyzer
