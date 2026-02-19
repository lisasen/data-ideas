"""WHO regional mapping utilities."""

WHO_REGION_BY_COUNTRY = {
    # AFRO
    "Algeria": "AFRO", "Angola": "AFRO", "Benin": "AFRO", "Botswana": "AFRO", "Burkina Faso": "AFRO",
    "Burundi": "AFRO", "Cabo Verde": "AFRO", "Cameroon": "AFRO", "Central African Republic": "AFRO",
    "Chad": "AFRO", "Comoros": "AFRO", "Congo": "AFRO", "Cote d'Ivoire": "AFRO", "Ivory Coast": "AFRO",
    "Democratic Republic of the Congo": "AFRO", "Djibouti": "AFRO", "Egypt": "EMRO", "Equatorial Guinea": "AFRO",
    "Eritrea": "AFRO", "Eswatini": "AFRO", "Ethiopia": "AFRO", "Gabon": "AFRO", "Gambia": "AFRO",
    "Ghana": "AFRO", "Guinea": "AFRO", "Guinea-Bissau": "AFRO", "Kenya": "AFRO", "Lesotho": "AFRO",
    "Liberia": "AFRO", "Libya": "EMRO", "Madagascar": "AFRO", "Malawi": "AFRO", "Mali": "AFRO",
    "Mauritania": "AFRO", "Mauritius": "AFRO", "Morocco": "EMRO", "Mozambique": "AFRO", "Namibia": "AFRO",
    "Niger": "AFRO", "Nigeria": "AFRO", "Rwanda": "AFRO", "Sao Tome and Principe": "AFRO",
    "Senegal": "AFRO", "Seychelles": "AFRO", "Sierra Leone": "AFRO", "Somalia": "EMRO", "South Africa": "AFRO",
    "South Sudan": "AFRO", "Sudan": "EMRO", "Togo": "AFRO", "Tunisia": "EMRO", "Uganda": "AFRO",
    "United Republic of Tanzania": "AFRO", "Tanzania": "AFRO", "Zambia": "AFRO", "Zimbabwe": "AFRO",

    # AMRO
    "Antigua and Barbuda": "AMRO", "Argentina": "AMRO", "Bahamas": "AMRO", "Barbados": "AMRO",
    "Belize": "AMRO", "Bolivia": "AMRO", "Brazil": "AMRO", "Canada": "AMRO", "Chile": "AMRO",
    "Colombia": "AMRO", "Costa Rica": "AMRO", "Cuba": "AMRO", "Dominica": "AMRO",
    "Dominican Republic": "AMRO", "Ecuador": "AMRO", "El Salvador": "AMRO", "Grenada": "AMRO",
    "Guatemala": "AMRO", "Guyana": "AMRO", "Haiti": "AMRO", "Honduras": "AMRO", "Jamaica": "AMRO",
    "Mexico": "AMRO", "Nicaragua": "AMRO", "Panama": "AMRO", "Paraguay": "AMRO", "Peru": "AMRO",
    "Saint Kitts and Nevis": "AMRO", "Saint Lucia": "AMRO", "Saint Vincent and the Grenadines": "AMRO",
    "Suriname": "AMRO", "Trinidad and Tobago": "AMRO", "United States": "AMRO", "United States of America": "AMRO",
    "Uruguay": "AMRO", "Venezuela": "AMRO",

    # EMRO
    "Afghanistan": "EMRO", "Bahrain": "EMRO", "Iran": "EMRO", "Iraq": "EMRO", "Jordan": "EMRO",
    "Kuwait": "EMRO", "Lebanon": "EMRO", "Oman": "EMRO", "Pakistan": "EMRO", "Qatar": "EMRO",
    "Saudi Arabia": "EMRO", "Syrian Arab Republic": "EMRO", "Syria": "EMRO", "United Arab Emirates": "EMRO",
    "Yemen": "EMRO",

    # EURO
    "Albania": "EURO", "Andorra": "EURO", "Armenia": "EURO", "Austria": "EURO", "Azerbaijan": "EURO",
    "Belarus": "EURO", "Belgium": "EURO", "Bosnia and Herzegovina": "EURO", "Bulgaria": "EURO",
    "Croatia": "EURO", "Cyprus": "EURO", "Czechia": "EURO", "Czech Republic": "EURO", "Denmark": "EURO",
    "Estonia": "EURO", "Finland": "EURO", "France": "EURO", "Georgia": "EURO", "Germany": "EURO",
    "Greece": "EURO", "Hungary": "EURO", "Iceland": "EURO", "Ireland": "EURO", "Israel": "EURO",
    "Italy": "EURO", "Kazakhstan": "EURO", "Kyrgyzstan": "EURO", "Latvia": "EURO", "Lithuania": "EURO",
    "Luxembourg": "EURO", "Malta": "EURO", "Monaco": "EURO", "Montenegro": "EURO", "Netherlands": "EURO",
    "North Macedonia": "EURO", "Norway": "EURO", "Poland": "EURO", "Portugal": "EURO", "Republic of Moldova": "EURO",
    "Moldova": "EURO", "Romania": "EURO", "Russian Federation": "EURO", "Russia": "EURO", "San Marino": "EURO",
    "Serbia": "EURO", "Slovakia": "EURO", "Slovenia": "EURO", "Spain": "EURO", "Sweden": "EURO",
    "Switzerland": "EURO", "Tajikistan": "EURO", "Turkiye": "EURO", "Turkey": "EURO", "Turkmenistan": "EURO",
    "Ukraine": "EURO", "United Kingdom": "EURO", "Uzbekistan": "EURO",

    # SEARO
    "Bangladesh": "SEARO", "Bhutan": "SEARO", "Democratic People's Republic of Korea": "WPRO",
    "India": "SEARO", "Indonesia": "SEARO", "Maldives": "SEARO", "Myanmar": "SEARO", "Nepal": "SEARO",
    "Sri Lanka": "SEARO", "Thailand": "SEARO", "Timor-Leste": "SEARO",

    # WPRO
    "Australia": "WPRO", "Brunei Darussalam": "WPRO", "Cambodia": "WPRO", "China": "WPRO",
    "Fiji": "WPRO", "Japan": "WPRO", "Kiribati": "WPRO", "Lao People's Democratic Republic": "WPRO",
    "Laos": "WPRO", "Malaysia": "WPRO", "Marshall Islands": "WPRO", "Micronesia": "WPRO",
    "Mongolia": "WPRO", "Nauru": "WPRO", "New Zealand": "WPRO", "Palau": "WPRO", "Papua New Guinea": "WPRO",
    "Philippines": "WPRO", "Republic of Korea": "WPRO", "South Korea": "WPRO", "Samoa": "WPRO",
    "Singapore": "WPRO", "Solomon Islands": "WPRO", "Tonga": "WPRO", "Tuvalu": "WPRO", "Vanuatu": "WPRO",
    "Viet Nam": "WPRO", "Vietnam": "WPRO",
}


def country_to_who_region(country: str) -> str:
    if not country:
        return "Unknown"
    return WHO_REGION_BY_COUNTRY.get(country.strip(), "Unknown")
