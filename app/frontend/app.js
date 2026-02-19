function el(tag, attrs = {}, children = []) {
  const node = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'className') node.className = v;
    else if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2).toLowerCase(), v);
    else node.setAttribute(k, v);
  });
  (Array.isArray(children) ? children : [children]).forEach((c) => {
    if (c === null || c === undefined) return;
    node.appendChild(typeof c === 'string' || typeof c === 'number' ? document.createTextNode(String(c)) : c);
  });
  return node;
}

async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

function buildDropdown(label, options, value, onChange) {
  const select = el('select', { onchange: (e) => onChange(e.target.value) }, [el('option', { value: '' }, 'All')]);
  options.forEach((o) => select.appendChild(el('option', { value: o }, o)));
  select.value = value || '';
  return el('label', { className: 'dropdown' }, [el('span', {}, label), select]);
}

function buildTable(title, headers, rows) {
  const theadRow = el('tr', {}, headers.map((h) => el('th', {}, h)));
  const tbody = el('tbody');
  rows.forEach((r) => tbody.appendChild(el('tr', {}, r.map((c) => el('td', {}, c)))));
  return el('div', { className: 'card' }, [
    el('h3', {}, title),
    el('table', {}, [el('thead', {}, [theadRow]), tbody]),
  ]);
}

function buildSimpleBarChart(planned, actual) {
  const maxVal = Math.max(planned, actual, 1);
  const plannedPct = Math.round((planned / maxVal) * 100);
  const actualPct = Math.round((actual / maxVal) * 100);

  const bar = (label, value, pct, cls) => el('div', { className: 'bar-row' }, [
    el('div', { className: 'bar-label' }, label),
    el('div', { className: 'bar-track' }, [
      el('div', { className: `bar-fill ${cls}`, style: `width:${pct}%` }, String(value)),
    ]),
  ]);

  return el('div', { className: 'card chart-card' }, [
    el('h3', {}, 'Planned vs Actual Enrollment'),
    bar('Planned', planned, plannedPct, 'planned'),
    bar('Actual', actual, actualPct, 'actual'),
  ]);
}

async function init() {
  const root = document.getElementById('root');
  const state = { filters: null, data: null, region: '', country: '', ta: '', indication: '' };

  async function reloadData() {
    const query = new URLSearchParams();
    if (state.region) query.set('region', state.region);
    if (state.country) query.set('country', state.country);
    if (state.ta) query.set('ta', state.ta);
    if (state.indication) query.set('indication', state.indication);
    state.data = await fetchJSON(`/api/enrollment?${query.toString()}`);
    render();
  }

  function render() {
    root.innerHTML = '';
    if (!state.filters || !state.data) {
      root.appendChild(el('div', { className: 'container' }, [el('p', {}, 'Loading...')]));
      return;
    }

    const filters = el('div', { className: 'filters' }, [
      buildDropdown('WHO Region', state.filters.regions, state.region, (v) => { state.region = v; reloadData(); }),
      buildDropdown('Country', state.filters.countries, state.country, (v) => { state.country = v; reloadData(); }),
      buildDropdown('Therapeutic Area', state.filters.therapeutic_areas, state.ta, (v) => { state.ta = v; reloadData(); }),
      buildDropdown('Indication Class', state.filters.indication_classes, state.indication, (v) => { state.indication = v; reloadData(); }),
    ]);

    const countryRows = state.data.by_country.map((x) => [x.country, x.planned, x.actual]);
    const siteRows = state.data.by_site.map((x) => [x.site_name, x.country, x.planned, x.actual]);

    root.appendChild(el('div', { className: 'container' }, [
      el('h1', {}, 'Clinical Trial Operational Analytics'),
      el('p', { className: 'subtitle' }, 'Operational enrollment tracking by WHO region, country, and therapeutic area'),
      filters,
      buildSimpleBarChart(state.data.summary.planned, state.data.summary.actual),
      el('div', { className: 'grid' }, [
        buildTable('Country Enrollment (Top 50)', ['Country', 'Planned', 'Actual'], countryRows),
        buildTable('Site Enrollment (Top 100)', ['Site', 'Country', 'Planned', 'Actual'], siteRows),
      ]),
      el('div', { className: 'footnote' }, `Source: ${state.data.source.join(', ')} • Last generated: ${new Date(state.data.generated_at).toLocaleString()}`),
    ]));
  }

  try {
    state.filters = await fetchJSON('/api/filters');
    await reloadData();
  } catch (err) {
    root.innerHTML = '';
    root.appendChild(el('div', { className: 'container' }, [
      el('h2', {}, 'Unable to load dashboard'),
      el('p', {}, `Error: ${err.message}`),
      el('p', {}, 'Please ensure backend is running with: python app/backend/server.py'),
    ]));
  }
}

init();
