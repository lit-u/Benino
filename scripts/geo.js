#!/usr/bin/env node
/**
 * geo.js — greitai gauk koordinates pagal adresą
 * Naudojimas:
 *   node scripts/geo.js "Birutės al. 60, Palanga"
 *   node scripts/geo.js "Ganyklų g. 8"
 */
const https = require('https');

// Palangos pakrantės regionas
const LAT_MIN = 55.5, LAT_MAX = 56.6, LNG_MIN = 20.5, LNG_MAX = 21.8;
const inRegion = (lat, lng) => lat >= LAT_MIN && lat <= LAT_MAX && lng >= LNG_MIN && lng <= LNG_MAX;

const query = process.argv.slice(2).join(' ');
if (!query) {
  console.error('Naudojimas: node scripts/geo.js "adresas"');
  process.exit(1);
}

const q = query.includes('Lietuva') ? query : query + ', Lietuva';
const encoded = encodeURIComponent(q);
const url = `https://photon.komoot.io/api/?q=${encoded}&limit=5`;

https.get(url, { headers: { 'User-Agent': 'PajurioPortalas/1.0 (sekmes.lt)' } }, res => {
  let body = '';
  res.on('data', d => body += d);
  res.on('end', () => {
    const data = JSON.parse(body);
    const features = data.features || [];
    if (!features.length) { console.log('Nerasta nieko.'); return; }

    // Pick first result within region, fallback to first overall
    const best = features.find(f => {
      const [lng, lat] = f.geometry.coordinates;
      return inRegion(lat, lng);
    }) || features[0];

    const p = best.properties;
    const [lng, lat] = best.geometry.coordinates;
    const label = [p.street, p.housenumber, p.city, p.country].filter(Boolean).join(', ');
    const inR = inRegion(lat, lng);

    console.log(`\n✅ ${inR ? 'Regione' : '⚠️  Ne regione'}: ${label}`);
    console.log(`\n   "lat": ${lat},`);
    console.log(`   "lng": ${lng}`);
  });
}).on('error', e => console.error('Klaida:', e.message));
