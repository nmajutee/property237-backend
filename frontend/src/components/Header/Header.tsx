import { Globe, Home, LogIn, PlusSquare } from 'lucide-react'
import { useEffect } from 'react'

export interface HeaderProps {
  activeLanguage: 'EN' | 'FR'
  onLanguageChange: (language: 'EN' | 'FR') => void
}

export default function Header({ activeLanguage, onLanguageChange }: HeaderProps) {
  const isEnglish = activeLanguage === 'EN'

  useEffect(() => {
    // Load persisted language on mount if present
    try {
      const saved = localStorage.getItem('p237-lang')
      if (saved === 'EN' || saved === 'FR') {
        if (saved !== activeLanguage) onLanguageChange(saved as 'EN' | 'FR')
      } else {
        // infer from browser locale (first visit)
        const navLang = navigator.language || (navigator as any).userLanguage || 'en'
        const inferred = navLang.toLowerCase().startsWith('fr') ? 'FR' : 'EN'
        if (inferred !== activeLanguage) onLanguageChange(inferred)
      }
    } catch (e) { }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function toggleLang() {
    const next = activeLanguage === 'EN' ? 'FR' : 'EN'
    onLanguageChange(next)
    try { localStorage.setItem('p237-lang', next) } catch { }
  }

  return (
    <header className="property237-header">
      <nav className="property237-nav" role="navigation" aria-label="Main navigation">
        <div className="property237-nav-left">
          <a href="/" className="property237-logo" aria-label="Property237 home">
            <Home size={22} />
            <span>Property237</span>
          </a>
        </div>

        <div className="property237-nav-center" aria-hidden={false}>
          <ul className="property237-nav-links" role="menubar">
            <li><a href="/rent" className="property237-nav-link">{isEnglish ? 'Rent' : 'Louer'}</a></li>
            <li><a href="/buy" className="property237-nav-link">{isEnglish ? 'Buy' : 'Acheter'}</a></li>
            <li><a href="/sell" className="property237-nav-link">{isEnglish ? 'Sell' : 'Vendre'}</a></li>
            <li><a href="/guesthouses" className="property237-nav-link">{isEnglish ? 'Guesthouses' : 'Maisons d\'hôtes'}</a></li>
            <li><a href="/advice" className="property237-nav-link">{isEnglish ? 'Advice' : 'Conseils'}</a></li>
            {/* List a Property as a regular nav-link (icon + text, no shadow) */}
            <li>
              <a href="/list-property" className="property237-nav-link">
                <PlusSquare size={16} />
                {isEnglish ? 'List a Property' : 'Publier une annonce'}
              </a>
            </li>
          </ul>
        </div>

        <div className="property237-nav-right">
          {/* Sign In (icon) */}
          <a href="/signin" className="property237-secondary-btn signin-btn" aria-label="Sign in">
            <LogIn size={16} />
            <span>{isEnglish ? 'Sign In' : 'Se connecter'}</span>
          </a>

          {/* Language switch — single round toggle */}
          <button
            type="button"
            className={`property237-lang-toggle ${activeLanguage === 'EN' ? 'en' : 'fr'}`}
            aria-label={`Switch language (current ${activeLanguage})`}
            onClick={toggleLang}
            title={activeLanguage === 'EN' ? 'English' : 'Français'}
          >
            <Globe size={14} />
            <span className="sr-only">{activeLanguage}</span>
          </button>
        </div>
      </nav>
    </header>
  )
}