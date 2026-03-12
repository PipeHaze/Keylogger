import nmap
import os
import subprocess

# Diferentes formas de escribir la ruta - prueba una por una
RUTAS_NMAP = [
    r"C:\Program Files (x86)\Nmap\nmap.exe",  # ← USA ESTA PRIMERO
    
]

def encontrar_nmap_funcional():
    """Encuentra qué ruta de nmap funciona"""
    print("🔍 Buscando Nmap...")
    
    for ruta in RUTAS_NMAP:
        if os.path.exists(ruta):
            print(f"✅ Archivo encontrado: {ruta}")
            return ruta
    
    # Si no se encuentra, buscar en todo el sistema
    try:
        resultado = subprocess.run(['where', 'nmap'], capture_output=True, text=True, timeout=10)
        if resultado.returncode == 0:
            rutas = resultado.stdout.strip().split('\n')
            for ruta in rutas:
                ruta = ruta.strip()
                if os.path.exists(ruta):
                    print(f"✅ Nmap encontrado via 'where': {ruta}")
                    return ruta
    except Exception as e:
        print(f"❌ Error buscando nmap: {e}")
    
    return None

def verificar_instalacion_nmap():
    """Verifica si Nmap está instalado correctamente"""
    print("📋 Verificando instalación de Nmap...")
    
    # Verificar en el registro de Windows
    try:
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Nmap")
            installdir = winreg.QueryValueEx(key, "InstallDir")[0]
            ruta_nmap = os.path.join(installdir, "nmap.exe")
            if os.path.exists(ruta_nmap):
                print(f"✅ Nmap encontrado via registro: {ruta_nmap}")
                return ruta_nmap
        except:
            pass
    except ImportError:
        print("ℹ️  No se pudo verificar el registro de Windows")
    
    return None

# PROGRAMA PRINCIPAL
print("🚀 INICIANDO CONFIGURACIÓN NMAP")
print("=" * 50)

# Método 1: Buscar en rutas comunes
ruta_nmap = encontrar_nmap_funcional()

# Método 2: Buscar en registro de Windows
if not ruta_nmap:
    ruta_nmap = verificar_instalacion_nmap()

# Método 3: Pedir al usuario
if not ruta_nmap:
    print("\n❌ No se pudo encontrar Nmap automáticamente")
    print("💡 Por favor, busca manualmente nmap.exe:")
    print("1. Abre el Explorador de Archivos")
    print("2. Navega a C:\\Program Files (x86)\\Nmap\\")
    print("3. Busca el archivo 'nmap.exe'")
    print("4. Copia la ruta completa y pégala aquí")
    
    ruta_manual = input("📁 Ingresa la ruta completa a nmap.exe: ").strip()
    
    # Limpiar la ruta (quitar comillas si las tiene)
    ruta_manual = ruta_manual.replace('"', '')
    
    if os.path.exists(ruta_manual):
        ruta_nmap = ruta_manual
        print(f"✅ Ruta válida: {ruta_nmap}")
    else:
        print("❌ La ruta no existe. Verifica e intenta de nuevo.")
        exit()

try:
    print(f"\n⚙️  Configurando Nmap con: {ruta_nmap}")
    
    # Crear el scanner
    scanner = nmap.PortScanner()
    
    # Forzar la ruta de nmap
    scanner.nmap_path = ruta_nmap
    
    # Verificar que funciona obteniendo la versión
    print("🔍 Probando Nmap...")
    version_info = scanner.nmap_version()
    print(f"✅ Nmap configurado correctamente!")
    print(f"📋 Versión: {version_info}")
    
    # Ahora hacer el escaneo
    print("\n" + "=" * 50)
    ip = input("🎯 Ingresa IP a escanear (ej. 127.0.0.1, google.com): ").strip()
    
    if not ip:
        ip = "127.0.0.1"  # Localhost por defecto
    
    print(f"⏳ Escaneando {ip}...")
    
    # Escaneo simple de puertos comunes
    scanner.scan(ip, '22,80,443,3389', arguments='-sS --host-timeout 30s')
    
    hosts = scanner.all_hosts()
    
    if hosts:
        print(f"\n✅ Escaneo completado!")
        for host in hosts:
            print(f"📡 Host: {host}")
            print(f"   Estado: {scanner[host].state()}")
            
            # Mostrar puertos abiertos
            for protocolo in scanner[host].all_protocols():
                puertos = scanner[host][protocolo]
                abiertos = [str(puerto) for puerto, info in puertos.items() if info['state'] == 'open']
                
                if abiertos:
                    print(f"   🔓 Puertos {protocolo} abiertos: {', '.join(abiertos)}")
                else:
                    print(f"   🔒 No hay puertos {protocolo} abiertos")
    else:
        print("❌ No se encontraron hosts")
        
except nmap.nmap.PortScannerError as e:
    print(f"❌ Error de Nmap: {e}")
    print("\n🔧 SOLUCIONES:")
    print("1. Verifica que Nmap esté instalado correctamente")
    print("2. Ejecuta como Administrador")
    print("3. Verifica tu firewall/antivirus")
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")