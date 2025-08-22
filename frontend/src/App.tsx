import {
  Bath,
  Bed,
  Building2,
  Heart,
  Home,
  List,
  Map,
  MapPin,
  Ruler,
  Save,
  Search,
  Settings
} from 'lucide-react'
import { useEffect, useState } from 'react'
import Header from './components/Header'
import './index.css'
import api from './lib/api'

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

const sampleProperties: Property[] = [
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
  const [viewMode, setViewMode] = useState<'list' | 'map'>('list')
  const [activeLanguage, setActiveLanguage] = useState<'EN' | 'FR'>('EN')

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
    (property.area?.name || '').toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="property237-app-container">
      <Header
        activeLanguage={activeLanguage}
        onLanguageChange={setActiveLanguage}
      />

      {/* Hero Section */}
      <section className="property237-hero-section">
        <h1 className="property237-hero-title">
          Search {properties.length.toLocaleString()} listings in Cameroon
        </h1>

        <div className="property237-hero-controls">
          <div className="property237-property-type-tabs">
            <button
              className={`property237-property-type-tab ${activeTab === 'residential' ? 'active' : ''}`}
              onClick={() => setActiveTab('residential')}
            >
              <Home size={18} />
              Residential
            </button>
            <button
              className={`property237-property-type-tab ${activeTab === 'commercial' ? 'active' : ''}`}
              onClick={() => setActiveTab('commercial')}
            >
              <Building2 size={18} />
              Commercial
            </button>
          </div>

          <div className="property237-hero-search">
            <div className="search-pill">
              <input
                type="text"
                placeholder="City, Neighbourhood, Address or Property237® number"
                className="property237-hero-search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <button className="property237-hero-search-btn" onClick={() => { /* noop - already filters */ }}>
                <Search size={18} />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="property237-main-container">
        {/* Search Filters */}
        <aside className="property237-search-filters">
          <select className="property237-filter-select">
            <option>All</option>
            <option>For rent</option>
            <option>For sale</option>
          </select>
          <select className="property237-filter-select">
            <option>Min</option>
            <option>50,000 XAF</option>
            <option>100,000 XAF</option>
          </select>
          <select className="property237-filter-select">
            <option>Max</option>
            <option>300,000 XAF</option>
            <option>500,000 XAF</option>
          </select>
          <select className="property237-filter-select">
            <option>Beds</option>
            <option>1+</option>
            <option>2+</option>
          </select>
          <select className="property237-filter-select">
            <option>Baths</option>
            <option>1+</option>
            <option>2+</option>
          </select>

          <div className="filter-actions">
            <button className="property237-filters-btn">
              <Settings size={16} />
              Filters
            </button>
            <button className="property237-save-search-btn">
              <Save size={16} />
              Save Search
            </button>
          </div>
        </aside>

        {/* Results Section */}
        <section className="property237-results-section">
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

          <div className="property237-results-body">
            <div className="property237-listings-panel">
              {/* Sort */}
              <div className="property237-sort-row">
                <label>Sort By</label>
                <select className="property237-filter-select">
                  <option>Newest</option>
                  <option>Price: Low to High</option>
                  <option>Price: High to Low</option>
                </select>
              </div>

              {/* Property Listings */}
              {loading ? (
                <div className="property237-loading">Loading properties...</div>
              ) : (
                <div className="property237-grid">
                  {filteredProperties.map((property) => (
                    <article key={property.id} className="property237-card">
                      <div className="property237-card-media">
                        {/* Replace placeholder path with real image url if available */}
                        <img
                          src="/src/assets/placeholder-property.jpg"
                          alt={property.title}
                          className="property237-card-image"
                        />
                        <button className="property237-card-heart" aria-label="favorite">
                          <Heart size={18} />
                        </button>

                        <div className="property237-card-price">
                          {property.price?.toLocaleString()} XAF
                          <span className="frequency">/mo</span>
                        </div>
                      </div>

                      <div className="property237-card-body">
                        <div className="property237-card-title">{property.title}</div>
                        <div className="property237-card-address">
                          <MapPin size={14} />
                          <span>{property.area?.name || 'Cameroon'}</span>
                        </div>

                        <div className="property237-card-specs">
                          <span><Bed size={14} /> {property.no_of_bedrooms}</span>
                          <span><Bath size={14} /> {property.no_of_bathrooms}</span>
                          <span><Ruler size={14} /> 1200 sqft</span>
                        </div>

                        <div className="property237-card-meta">
                          <small>{new Date(property.created_at).toLocaleDateString()}</small>
                        </div>
                      </div>
                    </article>
                  ))}
                </div>
              )}
            </div>

            {/* Map Panel */}
            {viewMode === 'map' ? (
              <div className="property237-map-panel">
                <Map size={48} />
                <div>Interactive Map View</div>
                <small>(Map integration coming soon)</small>
              </div>
            ) : (
              <div className="property237-map-panel property237-map-placeholder" aria-hidden>
                <Map size={36} />
                <div>Switch to Map view to see map</div>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}