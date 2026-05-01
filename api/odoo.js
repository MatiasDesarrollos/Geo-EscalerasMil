const ODOO_URL = (process.env.ODOO_URL || 'https://train-escalerasmil-29-04-1.adhoc.inc').replace(/\/$/, '');

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Max-Age': '86400',
};

export default async function handler(req, res) {
  Object.entries(CORS).forEach(([k, v]) => res.setHeader(k, v));

  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'GET') {
    return res.status(200).json({ status: 'ok', proxy_target: ODOO_URL });
  }

  if (req.method === 'POST') {
    try {
      const upstream = await fetch(`${ODOO_URL}/jsonrpc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req.body),
      });
      const data = await upstream.json();
      return res.status(upstream.status).json(data);
    } catch (err) {
      return res.status(500).json({ error: { message: `Proxy error: ${err.message}`, type: err.constructor.name } });
    }
  }

  return res.status(405).json({ error: { message: 'Method not allowed' } });
}
