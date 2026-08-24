import { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [item, setItem] = useState(null)
  const [locations, setLocations] = useState([])
  const [recommendation, setRecommendation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [confirming, setConfirming] = useState(false)

  // Fetch initial data
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch a mock item to test the UI
        const itemRes = await fetch('http://127.0.0.1:8000/api/items/ITEM001')
        const itemData = await itemRes.json()
        setItem(itemData)

        // Fetch available locations
        const locRes = await fetch('http://127.0.0.1:8000/api/locations')
        const locData = await locRes.json()
        setLocations(locData)
      } catch (err) {
        console.error("Error fetching data", err)
      }
    }
    fetchData()
  }, [])

  const handleGetRecommendation = async () => {
    if (!item) return
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8000/api/stow/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
      })
      const data = await res.json()
      setRecommendation(data)
    } catch (err) {
      console.error("Error fetching recommendation", err)
    } finally {
      setLoading(false)
    }
  }

  const handleConfirm = async () => {
    if (!recommendation?.recommended_location) return
    setConfirming(true)
    try {
      await fetch(`http://127.0.0.1:8000/api/stow/confirm?location_id=${recommendation.recommended_location}`, {
        method: 'POST'
      })
      alert(`Successfully stowed item in ${recommendation.recommended_location}`)
      
      // Reset UI to simulate next item
      setRecommendation(null)
    } catch (err) {
      console.error("Error confirming", err)
    } finally {
      setConfirming(false)
    }
  }

  const handleReject = () => {
    // In a real app, this might pull from recommendation.alternative_locations
    alert("Placement rejected. Escalating to supervisor or showing next best option.")
    setRecommendation(null)
  }

  return (
    <div className="dashboard-container">
      <header>
        <h1>Agentic Stow Optimization</h1>
        <p>AI-Powered Space Utilisation for Inbound Operations</p>
      </header>

      <div className="grid-layout">
        {/* Left Column: Item Details */}
        <div className="left-column">
          <div className="glass-panel">
            <h2 className="section-title">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
              Incoming Item
            </h2>
            
            {item ? (
              <>
                <div className="item-grid">
                  <div className="item-stat">
                    <div className="item-stat-label">Item ID</div>
                    <div className="item-stat-value">{item.item_id}</div>
                  </div>
                  <div className="item-stat">
                    <div className="item-stat-label">Category</div>
                    <div className="item-stat-value" style={{textTransform: 'capitalize'}}>{item.category}</div>
                  </div>
                  <div className="item-stat">
                    <div className="item-stat-label">Dimensions (cm)</div>
                    <div className="item-stat-value">{item.length_cm} × {item.width_cm} × {item.height_cm}</div>
                  </div>
                  <div className="item-stat">
                    <div className="item-stat-label">Weight (kg)</div>
                    <div className="item-stat-value">{item.weight_kg}</div>
                  </div>
                </div>
                
                <button 
                  className="btn btn-primary" 
                  style={{width: '100%', marginTop: '1.5rem'}}
                  onClick={handleGetRecommendation}
                  disabled={loading}
                >
                  {loading ? 'Analyzing Options...' : 'Get AI Recommendation'}
                </button>
              </>
            ) : (
              <p>Loading item data...</p>
            )}
          </div>
        </div>

        {/* Right Column: Locations & Recommendation */}
        <div className="right-column">
          <div className="glass-panel">
            <h2 className="section-title">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              Available Stow Locations
            </h2>
            
            <table>
              <thead>
                <tr>
                  <th>Location ID</th>
                  <th>Dimensions (L×W×H)</th>
                  <th>Capacity (kg)</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {locations.map(loc => (
                  <tr key={loc.location_id}>
                    <td>{loc.location_id}</td>
                    <td>{loc.available_length_cm} × {loc.available_width_cm} × {loc.available_height_cm}</td>
                    <td>{loc.weight_capacity_kg}</td>
                    <td><span className="status-badge">{loc.status}</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Recommendation Result */}
          {recommendation && (
            <div className="glass-panel recommendation-panel">
              <div className="recommendation-header">
                <h2 className="section-title" style={{marginBottom: 0}}>
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent-color)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  Agent Recommendation
                </h2>
                <div className="recommendation-location">
                  {recommendation.recommended_location || "None"}
                </div>
              </div>

              {recommendation.recommended_location && (
                <>
                  <div className="metrics-container">
                    <div className="metric-circle" style={{'--progress': `${recommendation.space_utilisation_percent}%`}}>
                      <div className="metric-content">
                        <div className="metric-value">{recommendation.space_utilisation_percent}%</div>
                        <div className="metric-label">Utilisation</div>
                      </div>
                    </div>
                    <div className="metric-circle" style={{'--progress': '100%', '--accent-color': '#8b5cf6'}}>
                      <div className="metric-content">
                        <div className="metric-value">{recommendation.unused_volume_cm3}</div>
                        <div className="metric-label">Unused cm³</div>
                      </div>
                    </div>
                  </div>

                  <div className="llm-explanation">
                    {recommendation.llm_explanation}
                  </div>

                  <div className="action-bar">
                    <button className="btn btn-danger" onClick={handleReject}>✕ Reject</button>
                    <button className="btn btn-primary" onClick={handleConfirm} disabled={confirming}>
                      {confirming ? 'Confirming...' : '✓ Confirm Placement'}
                    </button>
                  </div>
                </>
              )}
              
              {!recommendation.recommended_location && (
                 <div className="llm-explanation">
                    {recommendation.llm_explanation || recommendation.reason}
                 </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
