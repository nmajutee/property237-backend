import { useEffect, useState } from "react";
import Header from "./components/Header";
import Hero from "./components/Hero";
import MapPanel from "./components/ResultsSection/MapPanel";
import PropertyGrid from "./components/ResultsSection/PropertyGrid";
import ResultsHeader from "./components/ResultsSection/ResultsHeader";
import SortRow from "./components/ResultsSection/SortRow";
import "./index.css";
import api from "./lib/api";

type Property = {
  id: number;
  title: string;
  slug: string;
  price: number;
  listing_type: string;
  property_type?: { name: string };
  area?: { name: string };
  no_of_bedrooms: number;
  no_of_bathrooms: number;
  description: string;
  created_at: string;
};

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
    created_at: "2025-08-21",
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
    created_at: "2025-08-21",
  },
];

export default function App() {
  const [properties, setProperties] = useState<Property[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [activeTab, setActiveTab] = useState("residential");
  const [viewMode, setViewMode] = useState<"list" | "map">("list");
  const [activeLanguage, setActiveLanguage] = useState<"EN" | "FR">("EN");

  useEffect(() => {
    let alive = true;
    setLoading(true);

    api
      .get("/properties/")
      .then((res) => {
        if (!alive) return;
        const data = Array.isArray(res.data?.results)
          ? res.data.results
          : Array.isArray(res.data)
            ? res.data
            : [];
        setProperties([...data, ...sampleProperties]);
      })
      .catch(() => {
        if (!alive) return;
        setProperties(sampleProperties);
      })
      .finally(() => alive && setLoading(false));

    return () => {
      alive = false;
    };
  }, []);

  const filteredProperties = properties.filter(
    (property) =>
      property.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (property.area?.name || "")
        .toLowerCase()
        .includes(searchQuery.toLowerCase())
  );

  return (
    <div className="property237-app-container">
      <Header activeLanguage={activeLanguage} onLanguageChange={setActiveLanguage} />
      <Hero
        propertiesCount={properties.length}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      <main className="property237-main-container">
        <section className="property237-results-section">
          <ResultsHeader
            resultsCount={filteredProperties.length}
            viewMode={viewMode}
            setViewMode={setViewMode}
          />
          <div className="property237-results-body">
            <div className="property237-listings-panel">
              <SortRow />
              {loading ? (
                <div className="property237-loading">Loading properties...</div>
              ) : (
                <PropertyGrid properties={filteredProperties} />
              )}
            </div>
            <MapPanel viewMode={viewMode} />
          </div>
        </section>
      </main>
    </div>
  );
}
