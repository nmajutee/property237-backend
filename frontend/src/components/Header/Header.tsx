import React from 'react'
import { Home, User, BookOpen, Heart } from 'lucide-react'

export interface HeaderProps {
  activeLanguage: 'EN' | 'FR'
  onLanguageChange: (language: 'EN' | 'FR') => void
}

export default function Header({ activeLanguage, onLanguageChange }: HeaderProps) {
  return (
    <header className="property237-header">
      <nav className="property237-nav">
        <div className="property237-nav-left">
          <a href="/" className="property237-logo">
            <Home size={22} />
            <span>Property237</span>
          </a>

          <div className="property237-nav-links">
            <a href="#" className="property237-nav-link">
              <Home size={16}/> Find a Home
            </a>
            <a href="#" className="property237-nav-link">
              <User size={16}/> Find an Agent
            </a>
            <a href="#" className="property237-nav-link">
              <BookOpen size={16}/> News
            </a>
          </div>
        </div>

        <div className="property237-nav-right">
          <div className="property237-actions">
            <button aria-label="saved properties" className="icon-btn">
              <BookOpen size={18}/>
            </button>
            <button aria-label="favorite properties" className="icon-btn">
              <Heart size={18}/>
            </button>
          </div>

          <div className="property237-auth">
            <span className="currency">XAF</span>
            <a href="#" className="property237-sign-in-btn">
              <User size={14}/> Sign In
            </a>
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