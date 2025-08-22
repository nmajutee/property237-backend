import {
  Bell,
  Heart,
  Home,
  User
} from 'lucide-react'

export interface HeaderProps {
  activeLanguage: 'EN' | 'FR'
  onLanguageChange: (language: 'EN' | 'FR') => void
}

export default function Header({ activeLanguage, onLanguageChange }: HeaderProps) {
  const isEnglish = activeLanguage === 'EN'

  return (
    <header className="property237-header">
      <nav className="property237-nav">
        <div className="property237-nav-left">
          <a href="/" className="property237-logo">
            <Home size={22} />
            <span>Property237</span>
          </a>

          {/* Primary Navigation */}
          <div className="property237-nav-links">
            <a href="/buy" className="property237-nav-link">
              {isEnglish ? 'Buy' : 'Acheter'}
            </a>

            <a href="/sell" className="property237-nav-link">
              {isEnglish ? 'Sell' : 'Vendre'}
            </a>

            <a href="/rent" className="property237-nav-link">
              {isEnglish ? 'Rent' : 'Louer'}
            </a>

            <a href="/agents" className="property237-nav-link">
              {isEnglish ? 'Find an Agent' : 'Trouver un Agent'}
            </a>
          </div>
        </div>

        <div className="property237-nav-right">
          {/* Sign In - positioned close to Find an Agent */}
          <div className="property237-auth-section">
            <a href="/signin" className="property237-sign-in-btn">
              <User size={14} />
              {isEnglish ? 'Sign In' : 'Connexion'}
            </a>
          </div>

          {/* Language Switcher */}
          <div className="property237-lang">
            <button
              className={`lang-btn ${activeLanguage === 'EN' ? 'active' : ''}`}
              aria-pressed={activeLanguage === 'EN'}
              onClick={() => onLanguageChange('EN')}
            >
              EN
            </button>
            <button
              className={`lang-btn ${activeLanguage === 'FR' ? 'active' : ''}`}
              aria-pressed={activeLanguage === 'FR'}
              onClick={() => onLanguageChange('FR')}
            >
              FR
            </button>
          </div>

          {/* Heart and Bell icons at far right */}
          <div className="property237-actions">
            <a href="/favorites" aria-label={isEnglish ? 'favorite properties' : 'propriétés favorites'} className="icon-btn">
              <Heart size={18} />
            </a>
            <a href="/notifications" aria-label={isEnglish ? 'notifications' : 'notifications'} className="icon-btn">
              <Bell size={18} />
            </a>
          </div>
        </div>
      </nav>
    </header>
  )
}