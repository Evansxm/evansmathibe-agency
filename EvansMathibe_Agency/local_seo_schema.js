// Dynamic Local SEO Schema Generator for Evans Mathibe | Mone | TYC
// Incorporates major South African business districts, shopping centers, and agency hubs.

(function() {
    const localSeoData = {
        "@context": "https://schema.org",
        "@type": "AdvertisingAgency",
        "@id": "https://evansmathibe.github.io/evansmathibe-agency/#local-seo",
        "name": "Evans Mathibe | Mone | TYC",
        "description": "Premier South African creative agency specializing in AI Brand Automation, Advertising, and Design. Serving national, provincial, and municipal business hubs.",
        "url": "https://evansmathibe.github.io/evansmathibe-agency/",
        "areaServed": [
            // National Capitals
            { "@type": "City", "name": "Pretoria", "alternateName": "Tshwane", "description": "Administrative Capital" },
            { "@type": "City", "name": "Cape Town", "description": "Legislative Capital" },
            { "@type": "City", "name": "Bloemfontein", "description": "Judicial Capital" },

            // Provincial Hubs
            { "@type": "City", "name": "Johannesburg", "containedInPlace": { "@type": "AdministrativeArea", "name": "Gauteng" } },
            { "@type": "City", "name": "Durban", "alternateName": "eThekwini", "containedInPlace": { "@type": "AdministrativeArea", "name": "KwaZulu-Natal" } },
            { "@type": "City", "name": "Polokwane", "containedInPlace": { "@type": "AdministrativeArea", "name": "Limpopo" } },
            { "@type": "City", "name": "Rustenburg", "containedInPlace": { "@type": "AdministrativeArea", "name": "North West" } },
            { "@type": "City", "name": "Mahikeng", "containedInPlace": { "@type": "AdministrativeArea", "name": "North West" } },
            { "@type": "City", "name": "Kimberley", "containedInPlace": { "@type": "AdministrativeArea", "name": "Northern Cape" } },
            { "@type": "City", "name": "Gqeberha", "alternateName": "Port Elizabeth", "containedInPlace": { "@type": "AdministrativeArea", "name": "Eastern Cape" } },
            { "@type": "City", "name": "Mbombela", "alternateName": "Nelspruit", "containedInPlace": { "@type": "AdministrativeArea", "name": "Mpumalanga" } },

            // Major Business Districts (CBDs)
            { "@type": "Place", "name": "Sandton CBD", "description": "Richest Square Mile in Africa" },
            { "@type": "Place", "name": "Rosebank Business District" },
            { "@type": "Place", "name": "Cape Town City Bowl" },
            { "@type": "Place", "name": "Umhlanga Ridge", "containedInPlace": { "@type": "City", "name": "Durban" } },
            { "@type": "Place", "name": "Century City", "containedInPlace": { "@type": "City", "name": "Cape Town" } },
            { "@type": "Place", "name": "Menlyn Maine", "containedInPlace": { "@type": "City", "name": "Pretoria" } },
            { "@type": "Place", "name": "Waterfall City", "containedInPlace": { "@type": "City", "name": "Midrand" } },
            { "@type": "Place", "name": "Melrose Arch" },
            { "@type": "Place", "name": "Illovo Boulevard" },
            { "@type": "Place", "name": "Stellenbosch Technopark" },
            { "@type": "Place", "name": "V&A Waterfront Business District" },
            
            // Strategic Agency Hubs
            { "@type": "Place", "name": "Bryanston", "description": "Advertising Agency Hub" },
            { "@type": "Place", "name": "Parkhurst", "description": "Creative District" },
            { "@type": "Place", "name": "Woodstock", "description": "Cape Town Creative Hub" },
            { "@type": "Place", "name": "Maboneng Precinct", "description": "Johannesburg Creative Hub" },
            { "@type": "Place", "name": "Braamfontein", "description": "Digital & Youth Culture Hub" },
            { "@type": "Place", "name": "De Waterkant", "description": "Cape Town Ad Agencies Hub" },
            { "@type": "Place", "name": "Florida Road", "description": "Durban Creative Zone" },

            // Proximity to Major Shopping Centers
            { "@type": "Place", "name": "Sandton City & Nelson Mandela Square" },
            { "@type": "Place", "name": "Mall of Africa" },
            { "@type": "Place", "name": "Gateway Theatre of Shopping" },
            { "@type": "Place", "name": "V&A Waterfront" },
            { "@type": "Place", "name": "Menlyn Park Shopping Centre" },
            { "@type": "Place", "name": "Canal Walk" },
            { "@type": "Place", "name": "Fourways Mall" },
            { "@type": "Place", "name": "The Pavilion" },
            { "@type": "Place", "name": "Eastgate Shopping Centre" },
            { "@type": "Place", "name": "Cresta Shopping Centre" },
            { "@type": "Place", "name": "Brooklyn Mall" },
            { "@type": "Place", "name": "Tyger Valley Shopping Centre" },
            { "@type": "Place", "name": "Baywest Mall" },
            { "@type": "Place", "name": "Mimosa Mall" },
            { "@type": "Place", "name": "Mall of the North" }
        ],
        "hasMap": "https://www.google.com/maps?q=Evans+Mathibe+Agency+South+Africa",
        "sameAs": [
            "https://www.tiktok.com/@evans_mathibe",
            "https://wa.me/27724165061",
            "https://www.linkedin.com/in/evansmathibe"
        ]
    };

    // Inject Schema into Head
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify(localSeoData);
    document.head.appendChild(script);
})();
