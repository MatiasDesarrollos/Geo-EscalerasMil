export default function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.status(200).json({
    db:       process.env.ODOO_DB       || '',
    username: process.env.ODOO_USERNAME || '',
    apikey:   process.env.ODOO_APIKEY   || '',
    ptype:    parseInt(process.env.ODOO_PTYPE || '8'),
  });
}
