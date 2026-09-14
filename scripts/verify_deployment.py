#!/usr/bin/env python3
"""
Parivar Restaurant — Deployment Verification Script
Tests backend health, CORS preflight headers, and API endpoints against live deployments.

Usage:
    python scripts/verify_deployment.py
    python scripts/verify_deployment.py --backend https://api.parivar.restaurant --frontend https://parivar.restaurant
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

def check_backend_health(backend_url: str) -> bool:
    url = backend_url.rstrip("/") + "/"
    print(f"\n[1/3] Testing Backend Health: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Parivar-Deployment-Check/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read().decode("utf-8")
            status = resp.status
            print(f"      Status: {status}")
            print(f"      Response: {data.strip()[:120]}")
            if status == 200:
                print("      ✅ Backend root endpoint is healthy.")
                return True
            else:
                print(f"      ❌ Unexpected status: {status}")
                return False
    except Exception as e:
        print(f"      ❌ Connection failed: {e}")
        return False

def check_cors_preflight(backend_url: str, frontend_url: str) -> bool:
    origin = frontend_url.rstrip("/")
    url = backend_url.rstrip("/") + "/api/v1/menu/"
    print(f"\n[2/3] Testing CORS Preflight: {url}")
    print(f"      Origin: {origin}")
    try:
        req = urllib.request.Request(
            url,
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization,content-type",
                "User-Agent": "Parivar-Deployment-Check/1.0",
            },
            method="OPTIONS"
        )
        with urllib.request.urlopen(req, timeout=45) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            allow_origin = headers.get("access-control-allow-origin", "")
            allow_creds = headers.get("access-control-allow-credentials", "")
            print(f"      Status: {resp.status}")
            print(f"      Access-Control-Allow-Origin: {allow_origin}")
            print(f"      Access-Control-Allow-Credentials: {allow_creds}")
            if allow_origin == origin or allow_origin == "*":
                print("      ✅ CORS is properly configured for the frontend origin.")
                return True
            else:
                print(f"      ❌ Disallowed CORS origin! Expected '{origin}', got '{allow_origin}'.")
                return False
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()}
        allow_origin = headers.get("access-control-allow-origin", "")
        print(f"      HTTP Error: {e.code}")
        print(f"      Access-Control-Allow-Origin: {allow_origin}")
        return False
    except Exception as e:
        print(f"      ❌ CORS check failed: {e}")
        return False

def check_menu_api(backend_url: str) -> bool:
    url = backend_url.rstrip("/") + "/api/v1/menu/"
    print(f"\n[3/3] Testing Menu API Endpoint: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Parivar-Deployment-Check/1.0"})
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = resp.read().decode("utf-8")
            status = resp.status
            items = json.loads(data)
            print(f"      Status: {status}")
            print(f"      Loaded {len(items)} menu items successfully.")
            if status == 200 and len(items) > 0:
                print("      ✅ Menu endpoint is live and returning database items.")
                return True
            else:
                print("      ⚠️ Menu endpoint returned empty or non-200.")
                return False
    except Exception as e:
        print(f"      ❌ Menu API check failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Verify Parivar Restaurant Deployments")
    parser.add_argument("--backend", default="https://parivar-restaurant-final.onrender.com",
                        help="Backend URL (e.g., https://api.parivar.restaurant or https://parivar-restaurant-final.onrender.com)")
    parser.add_argument("--frontend", default="https://parivar-restaurant-final.vercel.app",
                        help="Frontend URL (e.g., https://parivar.restaurant or https://parivar-restaurant-final.vercel.app)")
    args = parser.parse_args()

    print("==================================================")
    print("  Parivar Restaurant — Deployment Verification")
    print("==================================================")
    print(f"Backend Target : {args.backend}")
    print(f"Frontend Target: {args.frontend}")

    results = [
        check_backend_health(args.backend),
        check_cors_preflight(args.backend, args.frontend),
        check_menu_api(args.backend)
    ]

    print("\n==================================================")
    if all(results):
        print("  🎉 ALL CHECKS PASSED: Deployment is fully healthy!")
    else:
        print("  ⚠️ SOME CHECKS FAILED. Review output above.")
    print("==================================================")
    sys.exit(0 if all(results) else 1)

if __name__ == "__main__":
    main()
