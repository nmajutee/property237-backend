import {
  Bell,
  BookOpen,
  Building2,
  Heart,
  Home,
  MapPin,
  Phone,
  Search,
  Settings,
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
            <div className="property237-nav-dropdown">
              <a href="/properties" className="property237-nav-link">
                <Home size={16} />
                {isEnglish ? 'Properties' : 'Propriétés'}
              </a>
              <div className="property237-dropdown-menu">
                <a href="/properties/for-rent">{isEnglish ? 'For Rent' : 'À Louer'}</a>
                <a href="/properties/for-sale">{isEnglish ? 'For Sale' : 'À Vendre'}</a>
                <a href="/properties/studio">{isEnglish ? 'Studios' : 'Studios'}</a>
                <a href="/properties/apartment">{isEnglish ? 'Apartments' : 'Appartements'}</a>
                <a href="/properties/bungalow">{isEnglish ? 'Bungalows' : 'Bungalows'}</a>
                <a href="/properties/villa-duplex">{isEnglish ? 'Villas & Duplex' : 'Villas & Duplex'}</a>
              </div>
            </div>

            <div className="property237-nav-dropdown">
              <a href="/agents" className="property237-nav-link">
                <User size={16} />
                {isEnglish ? 'Find an Agent' : 'Trouver un Agent'}
              </a>
              <div className="property237-dropdown-menu">
                <a href="/agents/residential">{isEnglish ? 'Residential Agents' : 'Agents Résidentiels'}</a>
                <a href="/agents/commercial">{isEnglish ? 'Commercial Agents' : 'Agents Commerciaux'}</a>
                <a href="/agents/luxury">{isEnglish ? 'Luxury Specialists' : 'Spécialistes Luxe'}</a>
                <a href="/agents/investment">{isEnglish ? 'Investment Advisors' : 'Conseillers Investissement'}</a>
              </div>
            </div>

            <div className="property237-nav-dropdown">
              <a href="/locations" className="property237-nav-link">
                <MapPin size={16} />
                {isEnglish ? 'Locations' : 'Localités'}
              </a>
              <div className="property237-dropdown-menu">
                <a href="/locations/yaounde">{isEnglish ? 'Yaoundé' : 'Yaoundé'}</a>
                <a href="/locations/douala">{isEnglish ? 'Douala' : 'Douala'}</a>
                <a href="/locations/bamenda">{isEnglish ? 'Bamenda' : 'Bamenda'}</a>
                <a href="/locations/bafoussam">{isEnglish ? 'Bafoussam' : 'Bafoussam'}</a>
                <a href="/locations/garoua">{isEnglish ? 'Garoua' : 'Garoua'}</a>
                <a href="/locations/ngaoundere">{isEnglish ? 'Ngaoundéré' : 'Ngaoundéré'}</a>
              </div>
            </div>

            <a href="/commercial" className="property237-nav-link">
              <Building2 size={16} />
              {isEnglish ? 'Commercial' : 'Commercial'}
            </a>
          </div>
        </div>

        <div className="property237-nav-right">
          {/* Secondary Navigation - Quick Actions */}
          <div className="property237-actions">
            <a href="/search" aria-label={isEnglish ? 'advanced search' : 'recherche avancée'} className="icon-btn">
              <Search size={18} />
            </a>
            <a href="/saved" aria-label={isEnglish ? 'saved properties' : 'propriétés sauvegardées'} className="icon-btn">
              <BookOpen size={18} />
            </a>
            <a href="/favorites" aria-label={isEnglish ? 'favorite properties' : 'propriétés favorites'} className="icon-btn">
              <Heart size={18} />
            </a>
            <a href="/notifications" aria-label={isEnglish ? 'notifications' : 'notifications'} className="icon-btn">
              <Bell size={18} />
            </a>
          </div>

          {/* Authentication & Settings */}
          <div className="property237-auth">
            <span className="currency">XAF</span>

            <a href="/contact" className="property237-contact-btn">
              <Phone size={14} />
              {isEnglish ? 'Contact' : 'Contact'}
            </a>

            <div className="property237-auth-dropdown">
              <a href="/signin" className="property237-sign-in-btn">
                <User size={14} />
                {isEnglish ? 'Sign In' : 'Connexion'}
              </a>
              <div className="property237-auth-menu">
                <a href="/signin">{isEnglish ? 'Sign In' : 'Se Connecter'}</a>
                <a href="/signup">{isEnglish ? 'Sign Up' : 'S\'inscrire'}</a>
                <a href="/agent/register">{isEnglish ? 'Agent Registration' : 'Inscription Agent'}</a>
                <hr />
                <a href="/profile">{isEnglish ? 'My Profile' : 'Mon Profil'}</a>
                <a href="/dashboard">{isEnglish ? 'Dashboard' : 'Tableau de bord'}</a>
                <a href="/settings">
                  <Settings size={14} />
                  {isEnglish ? 'Settings' : 'Paramètres'}
                </a>
              </div>
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
          </div>
        </div>
      </nav>
    </header>
  )
}