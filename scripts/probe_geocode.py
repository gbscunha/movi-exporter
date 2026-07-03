"""Sonda de geocodificação (gis_geocode) — rodar com token real.

Confirma: (1) o login retorna gis_sid + gis_geocode? (2) o serviço está
habilitado (retorna endereço) ou dá error=7 (Access denied)? (3) formato real
da resposta.

Uso: PYTHONPATH=. python scripts/probe_geocode.py [--account 1|2]
"""

import argparse
import json
import sys

import requests

from src.clients.wialon_client import WialonClient
from src.core.config import settings

# Coordenada real de um veículo da frota (região Niterói/RJ), vista nos exports.
TEST_COORDS = [{"lon": -43.359657, "lat": -22.818147}]

# Flags do doc: endereço completo (rua, casa, cidade, região, país).
FLAGS_FULL = 1255211008


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--account", type=int, choices=[1, 2], default=1)
    ap.add_argument("--provider", default="osm", help="osm|google|here|yandex|...")
    args = ap.parse_args()

    token = settings.WIALON_TOKEN if args.account == 1 else settings.WIALON_TOKEN_2
    if not token:
        print(f"❌ Token da conta {args.account} não configurado.")
        return 1

    client = WialonClient(token=token)
    login = client.authenticate()

    print("\n=== 1) Campos GIS no login ===")
    for key in ("gis_sid", "gis_geocode", "gis_search", "gis_render", "gis_routing"):
        print(f"   {key:14} = {login.get(key)!r}")
    print(f"   (client.gis_sid          = {client.gis_sid!r})")
    print(f"   (client.gis_geocode_url  = {client.gis_geocode_url!r})")

    if not client.gis_geocode_url or not client.gis_sid:
        print("\n⚠️  Login NÃO trouxe gis_geocode/gis_sid — sem como geocodificar.")
        client.logout()
        return 0

    print(f"\n=== 2) Chamada de teste ao gis_geocode (provider={args.provider}) ===")
    print(f"   coords = {TEST_COORDS}")
    try:
        resp = client._session.get(
            client.gis_geocode_url,
            params={
                "coords": json.dumps(TEST_COORDS),
                "flags": FLAGS_FULL,
                "gis_sid": client.gis_sid,
                "search_provider": args.provider,
                "lang": "pt",
            },
            timeout=60,
        )
        print(f"   HTTP {resp.status_code}")
        try:
            data = resp.json()
        except Exception:
            data = resp.text
        print(f"   Resposta bruta: {data!r}")

        print("\n=== 3) Veredito ===")
        if isinstance(data, dict) and "error" in data:
            code = data.get("error")
            if code == 7:
                print("🚧 error=7 (Access denied) — serviço AINDA NÃO habilitado na conta.")
            else:
                print(f"⚠️  error={code} — ver documentação da API.")
        elif isinstance(data, list) and data:
            print(f"✅ HABILITADO! Endereço retornado: {data[0]!r}")
        else:
            print(f"❓ Resposta inesperada: {data!r}")
    except requests.RequestException as e:
        print(f"❌ Erro de rede: {e}")
    finally:
        client.logout()

    return 0


if __name__ == "__main__":
    sys.exit(main())
