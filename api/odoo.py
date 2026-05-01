"""
Vercel Serverless Function — Proxy a Odoo

Endpoint: /api/odoo
Reenvía requests JSON-RPC al servidor Odoo, resolviendo CORS para que la app
estática pueda comunicarse desde el navegador.

Variables de entorno opcionales (configurables en Vercel Dashboard):
- ODOO_URL: URL base del servidor Odoo. Default: instancia de test de Escaleras Mil
"""

import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

ODOO_URL = os.environ.get(
    "ODOO_URL",
    "https://train-escalerasmil-29-04-1.adhoc.inc"
).rstrip("/")


class handler(BaseHTTPRequestHandler):

    def _set_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            target_url = f"{ODOO_URL}/jsonrpc"
            req = urllib.request.Request(
                target_url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    response_body = resp.read()
                    status_code = resp.getcode()
            except urllib.error.HTTPError as e:
                response_body = e.read()
                status_code = e.code

            self.send_response(status_code)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_body)))
            self.end_headers()
            self.wfile.write(response_body)

        except Exception as e:
            self.send_response(500)
            self._set_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_body = json.dumps({
                "error": {
                    "message": f"Proxy error: {str(e)}",
                    "type": type(e).__name__
                }
            }).encode("utf-8")
            self.wfile.write(error_body)

    def do_GET(self):
        # Endpoint de health check
        self.send_response(200)
        self._set_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok",
            "proxy_target": ODOO_URL,
            "message": "Odoo proxy listo. Hace POST con JSON-RPC body."
        }).encode("utf-8"))
