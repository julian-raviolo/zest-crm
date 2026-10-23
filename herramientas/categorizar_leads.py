#!/usr/bin/env python3
"""Completa la Categoría (A/B/C) de los Leads de EspoCRM leyendo la "Prioridad X" de la descripción.

No borra ni crea nada: solo actualiza el campo categoria de los leads que lo tienen vacío.
Uso:  ESPO_URL=https://crm.zest.uy ESPO_API_KEY=... python3 categorizar_leads.py [--aplicar]
Sin --aplicar solo muestra cuántos cambiaría.
"""
import base64, json, os, re, sys, urllib.request

URL = os.environ['ESPO_URL'].rstrip('/') + '/api/v1'
HEADERS = {'Content-Type': 'application/json'}
if os.environ.get('ESPO_API_KEY'):
    HEADERS['X-Api-Key'] = os.environ['ESPO_API_KEY']
else:  # solo para pruebas locales
    HEADERS['Espo-Authorization'] = base64.b64encode(os.environ['ESPO_BASIC'].encode()).decode()

def call(method, path, body=None):
    req = urllib.request.Request(URL + path, method=method, headers=HEADERS,
                                 data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)

leads, offset = [], 0
while True:
    page = call('GET', f'/Opportunity?select=id,name,categoria,description&maxSize=200&offset={offset}&orderBy=createdAt')
    leads += page['list']
    offset += 200
    if offset >= page['total']:
        break

grupos = {'A': [], 'B': [], 'C': []}
ya, sin = 0, 0
for l in leads:
    if l.get('categoria'):
        ya += 1
        continue
    m = re.search(r'Prioridad\s+([ABC])\b', l.get('description') or '')
    if m:
        grupos[m.group(1)].append(l['id'])
    else:
        sin += 1

print(f"Leads en el CRM: {len(leads)} | ya tenían categoría: {ya} | sin prioridad en la descripción: {sin}")
print('A cambiar:', {k: len(v) for k, v in grupos.items()})

if '--aplicar' in sys.argv:
    for cat, ids in grupos.items():
        for i in range(0, len(ids), 200):
            r = call('POST', '/MassAction', {'entityType': 'Opportunity', 'action': 'update',
                                             'params': {'ids': ids[i:i + 200]}, 'data': {'categoria': cat}})
            print(f"  {cat}: actualizados {r.get('count')}")
    print('Listo.')
