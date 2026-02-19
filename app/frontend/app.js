const { useEffect, useMemo, useRef, useState } = React;

function App() {
  const [filters, setFilters] = useState({ regions: [], countries: [], therapeutic_areas: [], indication_classes: [] });
  const [region, setRegion] = useState("");
  const [country, setCountry] = useState("");
  const [ta, setTa] = useState("");
  const [indication, setIndication] = useState("");
  const [data, setData] = useState(null);
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  useEffect(() => {
    fetch('/api/filters').then(r => r.json()).then(setFilters);
  }, []);

  const query = useMemo(() => {
    const p = new URLSearchParams();
    if (region) p.set('region', region);
    if (country) p.set('country', country);
    if (ta) p.set('ta', ta);
    if (indication) p.set('indication', indication);
    return p.toString();
  }, [region, country, ta, indication]);

  useEffect(() => {
    fetch(`/api/enrollment?${query}`).then(r => r.json()).then(setData);
  }, [query]);

  useEffect(() => {
    if (!data || !chartRef.current) return;
    const ctx = chartRef.current.getContext('2d');

    if (chartInstanceRef.current) {
      chartInstanceRef.current.destroy();
    }

    chartInstanceRef.current = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Planned Enrollment', 'Actual Enrollment'],
        datasets: [{
          label: 'Enrollment Count',
          data: [data.summary.planned, data.summary.actual],
          backgroundColor: ['#1f77b4', '#2ca02c']
        }]
      },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  }, [data]);

  return React.createElement('div', { className: 'container' }, [
    React.createElement('h1', { key: 'h' }, 'Clinical Trial Operational Analytics'),
    React.createElement('p', { key: 'p', className: 'subtitle' }, 'ClinicalTrials.gov-powered site and country enrollment tracking'),

    React.createElement('div', { key: 'filters', className: 'filters' }, [
      dropdown('WHO Region', region, setRegion, filters.regions),
      dropdown('Country', country, setCountry, filters.countries),
      dropdown('Therapeutic Area', ta, setTa, filters.therapeutic_areas),
      dropdown('Indication Class', indication, setIndication, filters.indication_classes)
    ]),

    React.createElement('div', { key: 'card', className: 'card chart-card' },
      React.createElement('canvas', { ref: chartRef, height: 120 })
    ),

    data && React.createElement('div', { key: 'tables', className: 'grid' }, [
      renderTable('Country Enrollment (Top 50)', ['Country', 'Planned', 'Actual'], data.by_country.map(x => [x.country, x.planned, x.actual])),
      renderTable('Site Enrollment (Top 100)', ['Site', 'Country', 'Planned', 'Actual'], data.by_site.map(x => [x.site_name, x.country, x.planned, x.actual]))
    ]),

    data && React.createElement('div', { key: 'f', className: 'footnote' }, `Source: ${data.source.join(', ')} • Last generated: ${new Date(data.generated_at).toLocaleString()}`)
  ]);
}

function dropdown(label, value, setter, options) {
  return React.createElement('label', { className: 'dropdown', key: label }, [
    React.createElement('span', { key: 's' }, label),
    React.createElement('select', { key: 'd', value, onChange: e => setter(e.target.value) }, [
      React.createElement('option', { key: 'all', value: '' }, 'All'),
      ...(options || []).map(o => React.createElement('option', { key: o, value: o }, o))
    ])
  ]);
}

function renderTable(title, headers, rows) {
  return React.createElement('div', { className: 'card', key: title }, [
    React.createElement('h3', { key: 't' }, title),
    React.createElement('table', { key: 'tb' }, [
      React.createElement('thead', { key: 'h' }, React.createElement('tr', {}, headers.map(h => React.createElement('th', { key: h }, h)))),
      React.createElement('tbody', { key: 'b' }, rows.map((r, i) => React.createElement('tr', { key: `${title}-${i}` }, r.map((c, j) => React.createElement('td', { key: `${i}-${j}` }, c)))))
    ])
  ]);
}

ReactDOM.createRoot(document.getElementById('root')).render(React.createElement(App));
