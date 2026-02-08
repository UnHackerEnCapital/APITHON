import asyncio
import json
import re
import urllib.parse
import threading
import time
import os
import socket
import platform
from flask import Flask, request, jsonify
from playwright.async_api import async_playwright
from curl_cffi import requests

# --- CONFIGURACIÓN E IDENTIDAD ---
ASCII_ART = r"""
    ┌──────────────────────────────────────────────────────────────────────────┐
    │  _______  _______  ___  _______  __   __  _______  __    _               │
    │ |   _   ||       ||   ||       ||  | |  ||       ||  |  | |              │
    │ |  |_|  ||    _  ||   ||_     _||  |_|  ||   _   ||   |_| |              │
    │ |       ||   |_| ||   |  |   |  |       ||  | |  ||       |              │
    │ |       ||    ___||   |  |   |  |       ||  |_|  ||  _    |              │
    │ |   _   ||   |    |   |  |   |  |   _   ||       || | |   |              │
    │ |__| |__||___|    |___|  |___|  |__| |__||_______||_|  |__|              │
    │                                                                          │
    │  >> UNHACKERENCAPITAL | PROTOCOL ANALYSIS | GATEWAY POC v3.0 <<          │
    └──────────────────────────────────────────────────────────────────────────┘
"""
app = Flask(__name__)
API_KEY_GATEWAY = "UnHackerEnCapital"

SESS = {
    "auth_cookie": None, 
    "internal_context": None, 
    "session_id": None, 
    "build_id": None, 
    "status_ready": False, 
    "target_url": ""
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_lan_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# --- MOTOR DE INTERCEPTACIÓN Y VALIDACIÓN HUMANA ---
async def sincronizar_tunel(url_input):
    if not url_input.startswith("http"):
        url_input = "https://" + url_input
    SESS["target_url"] = url_input

    async with async_playwright() as p:
        print(f"\n[*] Estableciendo túnel en: {SESS['target_url']}")
        print("[*] Iniciando validación automatizada...")
        
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        async def protocol_sniffer(request):
            if "StreamGenerate" in request.url:
                post_data = request.post_data
                if post_data:
                    decoded = urllib.parse.unquote(post_data)
                    ctx_match = re.search(r'(![a-zA-Z0-9_\-]{100,})', decoded)
                    sid_match = re.search(r'f.sid=([^&]+)', request.url)
                    bl_match = re.search(r'bl=([^&]+)', request.url)
                    
                    if ctx_match and sid_match:
                        SESS["internal_context"] = ctx_match.group(1)
                        SESS["session_id"] = sid_match.group(1)
                        SESS["build_id"] = bl_match.group(1)
                        cookies = await context.cookies()
                        SESS["auth_cookie"] = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                        SESS["status_ready"] = True

        page.on("request", protocol_sniffer)
        await page.goto(SESS["target_url"])

        try:
            input_selector = "div[contenteditable='true'], textarea, input"
            await page.wait_for_selector(input_selector, timeout=15000)
            print("[+] Interfaz detectada. Enviando validación ('.')")
            await page.fill(input_selector, ".")
            await page.keyboard.press("Enter")
        except Exception:
            print("[!] Advertencia: No se pudo automatizar el envío. Hágalo manualmente.")

        while not SESS["status_ready"]:
            await asyncio.sleep(0.5)
        
        print("[+] PROTOCOLO CAPTURADO: Estructura de sesión sincronizada.")
        await browser.close()

# --- LÓGICA DE COMUNICACIÓN ---
def ejecutar_request_protocolo(user_query):
    base_domain = urllib.parse.urlparse(SESS["target_url"]).netloc
    backend_endpoint = (
        f"https://{base_domain}/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
        f"?bl={SESS['build_id']}&f.sid={SESS['session_id']}&hl=es-419&_reqid=2202684&rt=c"
    )
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36",
        "Cookie": SESS["auth_cookie"],
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-Same-Domain": "1",
        "Origin": f"https://{base_domain}",
        "Referer": f"https://{base_domain}/"
    }
    
    inner_structure = [[user_query, 0, None, None, None, None, 0], ["es-419"], ["", "", "", None, None, None, None, None, None, ""], SESS["internal_context"], "eb594bcd367d878b1514dd3b7c68bb91"]
    payload = {"f.req": json.dumps([None, json.dumps(inner_structure)]), "at": ""}
    
    try:
        r = requests.post(backend_endpoint, headers=headers, data=payload, impersonate="chrome120")
        patterns = re.findall(r'rc_[a-z0-9]+.*?\[\\"(.*?)\\"\]', r.text)
        if patterns:
            return patterns[-1].replace('\\\\n', '\n').replace('\\n', '\n').replace('\\"', '"')
        return "Aviso: Flujo de datos vacío."
    except Exception as e:
        return f"Error en el túnel: {str(e)}"

# --- MODO 1: GATEWAY & TUTORIAL ---
@app.route('/v1/chat/completions', methods=['POST'])
def apithon_gateway():
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {API_KEY_GATEWAY}":
        return jsonify({"error": "Unauthorized"}), 401
    user_input = request.json.get("messages", [{}])[-1].get("content", "")
    output_text = ejecutar_request_protocolo(user_input)
    return jsonify({"choices": [{"message": {"role": "assistant", "content": output_text}}], "model": "apithon-v3"})

def mostrar_tutorial(host_ip):
    es_windows = platform.system() == "Windows"
    print("\n" + "="*65)
    print("      📖 GUÍA DE USO - MODO PASARELA (GATEWAY)")
    print("="*65)
    print(f"[*] API KEY: {API_KEY_GATEWAY}")
    print(f"[*] ENDPOINT: http://{host_ip}:5000/v1/chat/completions")
    
    if es_windows:
        print("\n[>] COMANDO PARA POWERSHELL:")
        print(f'curl.exe http://{host_ip}:5000/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer {API_KEY_GATEWAY}" -d "{{\\"messages\\": [{{\\"role\\": \\"user\\", \\"content\\": \\"Hola Pepe, me dijo HackerEnCapital que te manda un saludo\\"}}]}}"')
        
        print("\n[>] COMANDO PARA CMD:")
        print(f'curl http://{host_ip}:5000/v1/chat/completions -H "Content-Type: application/json" -H "Authorization: Bearer {API_KEY_GATEWAY}" -d "{{\\"messages\\": [{{\\"role\\": \\"user\\", \\"content\\": \\"Hola Pepe, me dijo HackerEnCapital que te manda un saludo \\"}}]}}"')
    else:
        print("\n[>] COMANDO PARA LINUX (BASH):")
        print(f"curl http://{host_ip}:5000/v1/chat/completions \\")
        print(f"  -H 'Content-Type: application/json' \\")
        print(f"  -H 'Authorization: Bearer {API_KEY_GATEWAY}' \\")
        print(f"  -d '{{\"messages\": [{{\"role\": \"user\", \"content\": \"Hola Pepe, me dijo HackerEnCapital que te manda un saludo\"}}]}}'")
    print("="*65)

def run_gateway_service(bind_all=False):
    host = "0.0.0.0" if bind_all else "127.0.0.1"
    display_ip = get_lan_ip() if bind_all else "127.0.0.1"
    mostrar_tutorial(display_ip)
    app.run(host=host, port=5000, debug=False, use_reloader=False)

# --- MODO 2: ANALIZADOR DIRECTO ---
def run_interactive_shell():
    print("\n[+] MODO CHAT LLM ACTIVADO. Escriba 'salir' para finalizar.")
    while True:
        user_input = input("\n👤 Analista: ")
        if user_input.lower() in ['salir', 'exit']: break
        print("📡 Response: ", end="", flush=True)
        print(ejecutar_request_protocolo(user_input))

# --- FLUJO PRINCIPAL ---
def main():
    clear_screen()
    print(ASCII_ART)
    
    target = input("[?] Ingrese la URL del objetivo (ej: app.serviciollm.com): ")
    asyncio.run(sincronizar_tunel(target))

    if SESS["status_ready"]:
        while True:
            print("\n[ Seleccione Entorno ]")
            print("1. Modo Pasarela (Gateway / API Key + Tutorial)")
            print("2. Modo Chat Directo")
            
            opcion = input("\n> Opción: ")

            if opcion == "1":
                while True:
                    print("\n[ Configuración de Red ]")
                    print("L. Localhost (Solo este equipo)")
                    print("N. LAN (Disponible en toda tu red local)")
                    red_opcion = input("> Alcance (L/N): ").upper()
                    
                    if red_opcion == "L":
                        threading.Thread(target=run_gateway_service, args=(False,), daemon=True).start()
                        break
                    elif red_opcion == "N":
                        threading.Thread(target=run_gateway_service, args=(True,), daemon=True).start()
                        break
                    else:
                        print("[!] Ingrese L o N.")
                
                print("\n[MANTENIENDO PASARELA... Ctrl+C para cerrar]")
                while True: time.sleep(1)
            elif opcion == "2":
                run_interactive_shell()
                break
            else:
                print("[!] Opción inválida. Ingrese 1 o 2.")
    else:
        print("[-] Fallo en la sincronización.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Proceso finalizado.")