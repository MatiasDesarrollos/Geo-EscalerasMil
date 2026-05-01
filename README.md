# Gestor de Rutas — Escaleras Mil

Sistema interno de logística para armar y seguir rutas de reparto, integrado con Odoo vía JSON-RPC.

## 🚀 Deploy en Vercel

Este repo está listo para deployar en Vercel. Solo tenés que:

1. Hacer push a GitHub
2. Vercel detecta los cambios y deploya automáticamente
3. Abrir la URL de Vercel y configurar las credenciales de Odoo

### URL de producción

Una vez deployado, la app vive en algo como:
```
https://gestor-rutas-escalerasmil.vercel.app
```

## 📁 Estructura

```
.
├── api/
│   └── odoo.py          # Serverless function (proxy CORS hacia Odoo)
├── index.html           # App principal (gestor de rutas)
├── vercel.json          # Configuración de Vercel
└── README.md
```

## ⚙️ Configuración

### Variables de entorno (Vercel Dashboard → Settings → Environment Variables)

Opcional. Si no las definís, usa el default:

- `ODOO_URL`: URL del servidor Odoo (por defecto: instancia de test)

### Configuración de la app (en el navegador)

1. Abrir la app
2. Click en **⚙ Config**
3. Completar:
   - **URL**: dejar vacío (usa el proxy del propio Vercel)
   - **Base de datos**: `odoo` (o la que corresponda)
   - **Usuario**: tu email de Odoo
   - **API Key**: generala en Odoo > Preferencias > Account Security
   - **Picking Type ID**: ej. `8` para LOCAL/OUT
   - **OpenRouteService API Key**: opcional, para ver rutas reales en mapa
     - Conseguila gratis en [openrouteservice.org/dev/#/signup](https://openrouteservice.org/dev/#/signup)

## 🔧 Desarrollo local

Para correr localmente (sin Vercel):

1. Tener Python 3.8+
2. Usar el `odoo_proxy.py` original que sirve archivos estáticos + proxy
3. `python odoo_proxy.py`
4. Abrir `http://localhost:8765/`

## 🛠 Stack

- **Frontend**: HTML + JavaScript vanilla, Leaflet para mapas, OpenStreetMap como tiles
- **Backend**: Vercel Serverless Function en Python (proxy a Odoo)
- **Routing**: OpenRouteService (gratis, 2000 reqs/día)
- **Almacenamiento**: localStorage del navegador (rutas, config, cache de coords)

## 📋 Features

- ✅ Carga de pickings desde Odoo en tiempo real
- ✅ Segmentación geográfica por zonas (AMBA, GBA Norte/Sur/Oeste, provincias)
- ✅ Drag & drop para armar rutas
- ✅ Geocoding automático (usa coords de Odoo si existen, fallback a Nominatim)
- ✅ Visualización en mapa fullscreen con routing real
- ✅ Botón "Abrir en Google Maps" (sin API key)
- ✅ Validación automática del picking en Odoo al marcar como entregado
- ✅ Estados: pendiente, entregado, rechazado, reprogramado
- ✅ Recálculo automático de la ruta al ir entregando
- ✅ Hoja de ruta imprimible (A4) con mapa y branding corporativo

## 🔒 Notas de seguridad

- La API key de Odoo se guarda en el `localStorage` del navegador del usuario (cliente)
- El proxy serverless solo reenvía requests, no almacena credenciales
- Cada usuario debe configurar su propia API key
- La API key de Odoo dura 1 hora en el ambiente de test (renovar)

## 📞 Contacto

Escaleras Mil — Av. Caseros 1980, CABA  
Tel: 5365-8896 / 4306-1111  
WhatsApp: 11 3725-3323  
Email: info@escalerasmil.com  
Web: [escalerasmil.com.ar](https://escalerasmil.com.ar)

---

© Escaleras Mil — Sistema interno de logística
