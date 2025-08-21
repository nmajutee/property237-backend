import { useEffect, useState } from 'react'
import api from './lib/api'
import './App.css'
import {
  Home,
  Building2,
  Search,
  Settings,
  Save,
  Map,
  List,
  Bed,
  Bath,
  Ruler,
  MapPin,
  Heart,
  User,
  Calculator,
  BookOpen
} from 'lucide-react'

type Property = {
  id: number
  title: string
  slug: string
  price: number
  listing_type: string
  property_type?: { name: string }
  area?: { name: string }
  no_of_bedrooms: number
  no_of_bathrooms: number
  description: string
  created_at: string
}

const sampleProperties = [
  {
    id: 1,
    title: "Modern Apartment in City Center",
    slug: "modern-apartment-city-center",
    price: 250000,
    listing_type: "rent",
    property_type: { name: "Apartment" },
    area: { name: "Yaoundé, Cameroon" },
    no_of_bedrooms: 2,
    no_of_bathrooms: 1,
    description: "Beautiful modern apartment with great city views",
    created_at: "2025-08-21"
  },
  {
    id: 2,
    title: "Luxury Villa with Pool",
    slug: "luxury-villa-pool",
    price: 450000,
    listing_type: "sale",
    property_type: { name: "Villa" },
    area: { name: "Douala, Cameroon" },
    no_of_bedrooms: 3,
    no_of_bathrooms: 2,
    description: "Spacious family home in quiet neighborhood",
    created_at: "2025-08-21"
  }
]

export default function App() {
  const [properties, setProperties] = useState<Property[]>([])
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [activeTab, setActiveTab] = useState('residential')
  const [viewMode, setViewMode] = useState('list')

  useEffect(() => {
    let alive = true
    setLoading(true)

    api.get('/properties/')
      .then(res => {
        if (!alive) return
        const data = Array.isArray(res.data?.results) ? res.data.results : (Array.isArray(res.data) ? res.data : [])
        setProperties([...data, ...sampleProperties])
      })
      .catch(() => {
        if (!alive) return
        setProperties(sampleProperties)
      })
      .finally(() => alive && setLoading(false))

    return () => { alive = false }
  }, [])

  const filteredProperties = properties.filter(property =>
    property.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    property.area?.name.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="property237-app-container">
      {/* Header */}
      <header className="property237-header">
        // Navigation bar
        <nav className="property237-nav">
          <div style={{display: 'flex', alignItems: 'center', gap: 12}}>
            <a href="/" className="property237-logo">
              <Home size={24} />
              Property237
            </a>
          </div>

          <div style={{display:'flex', alignItems:'center', gap:16}}>
            <div className="property237-nav-links" style={{marginRight: 8}}>
              <a href="#" className="property237-nav-link"><Home size={16}/> Find a Home</a>
              <a href="#" className="property237-nav-link"><User size={16}/> Find an Agent</a>
              <a href="#" className="property237-nav-link"><Calculator size={16}/> Mortgage Calculators</a>
              <a href="#" className="property237-nav-link"><BookOpen size={16}/> Latest News</a>
            </div>

            <div style={{display: 'flex', alignItems:'center', gap:8, marginRight: 8}}>
              <button aria-label="saved" style={{background:'rgba(255,255,255,0.12)', borderRadius:8, padding:6, border:'none', color:'white'}}>
                <BookOpen size={18}/>
              </button>
              <button aria-label="favorites" style={{background:'rgba(255,255,255,0.12)', borderRadius:8, padding:6, border:'none', color:'white'}}>
                <Heart size={18}/>
              </button>
            </div>

            <div className="property237-auth">
              <span style={{opacity:0.95}}>XAF</span>
              <a href="#" className="property237-sign-in-btn"><User size={16}/> Sign In</a>
              <div className="property237-lang">
                <button className="lang-btn active">EN</button>
                <button className="lang-btn">FR</button>
              </div>
            </div>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="property237-hero-section">
        <h1 className="property237-hero-title">
          Search {properties.length.toLocaleString()} listings from Property237®
        </h1>

        <div className="property237-property-type-tabs">
          <button
            className={`property237-property-type-tab ${activeTab === 'residential' ? 'active' : ''}`}
            onClick={() => setActiveTab('residential')}
          >
            <Home size={20} />
            Residential
          </button>
          <button
            className={`property237-property-type-tab ${activeTab === 'commercial' ? 'active' : ''}`}
            onClick={() => setActiveTab('commercial')}
          >
            <Building2 size={20} />
            Commercial
          </button>
        </div>

        <div className="property237-hero-search">
          <input
            type="text"
            placeholder="City, Neighbourhood, Address or Property237® number"
            className="property237-hero-search-input"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button className="property237-hero-search-btn">
            <Search size={20} />
            Search
          </button>
        </div>
      </section>

      {/* Main Content */}
      <main className="property237-main-container">
        {/* Search Filters */}
        <div className="property237-search-filters">
          <select className="property237-filter-select">
            <option>For rent</option>
            <option>For sale</option>
          </select>
          <select className="property237-filter-select">
            <option>Min Rent</option>
            <option>50,000 XAF</option>
            <option>100,000 XAF</option>
            <option>200,000 XAF</option>
          </select>
          <select className="property237-filter-select">
            <option>Max Rent</option>
            <option>300,000 XAF</option>
            <option>500,000 XAF</option>
            <option>1,000,000 XAF</option>
          </select>
          <select className="property237-filter-select">
            <option>Beds</option>
            <option>1+</option>
            <option>2+</option>
            <option>3+</option>
          </select>
          <select className="property237-filter-select">
            <option>Baths</option>
            <option>1+</option>
            <option>2+</option>
            <option>3+</option>
          </select>
          <button className="property237-filters-btn">
            <Settings size={16} />
            Filters
          </button>
          <button className="property237-save-search-btn">
            <Save size={16} />
            Save Search
          </button>
        </div>

        {/* Results Section */}
        <div className="property237-results-section">
          {/* Listings Panel */}
          <div className="property237-listings-panel">
            <div className="property237-results-header">
              <div className="property237-results-count">
                Results: {filteredProperties.length} Listings
              </div>
              <div className="property237-view-toggle">
                <button
                  className={`property237-view-btn ${viewMode === 'map' ? 'active' : ''}`}
                  onClick={() => setViewMode('map')}
                >
                  <Map size={16} />
                  Map
                </button>
                <button
                  className={`property237-view-btn ${viewMode === 'list' ? 'active' : ''}`}
                  onClick={() => setViewMode('list')}
                >
                  <List size={16} />
                  List
                </button>
              </div>
            </div>

            {/* Sort */}
            <div style={{ marginBottom: '16px' }}>
              <label style={{ marginRight: '8px' }}>Sort By</label>
              <select className="property237-filter-select" style={{ minWidth: '120px' }}>
                <option>Newest</option>
                <option>Price: Low to High</option>
                <option>Price: High to Low</option>
              </select>
            </div>

            {/* Property Listings */}
            {loading ? (
              <div className="property237-loading">
                Loading properties...
              </div>
            ) : (
              <div>
                {filteredProperties.map((property) => (
                  <div key={property.id} className="property237-property-listing">
                    <div className="property237-property-image-container">
                      <div className="property237-property-image">
                        <Home size={48} />
                      </div>
                      <button className="property237-property-heart">
                        <Heart size={20} />
                      </button>
                    </div>
                    <div className="property237-property-details">
                      <div>
                        <div className="property237-property-price">
                          {property.price?.toLocaleString()} XAF/Monthly
                        </div>
                        <div className="property237-property-address">
                          <MapPin size={14} />
                          {property.area?.name || 'Cameroon'}
                        </div>
                        <div className="property237-property-title">{property.title}</div>
                        <div className="property237-property-specs">
                          <span>
                            <Bed size={16} />
                            {property.no_of_bedrooms}
                          </span>
                          <span>
                            <Bath size={16} />
                            {property.no_of_bathrooms}
                          </span>
                          <span>
                            <Ruler size={16} />
                            1200 sqft
                          </span>
                        </div>
                      </div>
                      <div className="property237-property-time">6 hours ago</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Map Panel */}
          <div className="property237-map-container">
            <Map size={48} />
            <div>Interactive Map View</div>
            <small>(Map integration coming soon)</small>
          </div>
        </div>
      </main>
    </div>
  )
}