"""
SmartBin SI - Admin Interface API
API complète pour la supervision du système de tri intelligent
"""

from flask import Flask, jsonify, request, render_template
from pathlib import Path
import subprocess
import json
import sys
import os
import socket
from datetime import datetime
import psutil

app = Flask(__name__, static_folder='static', template_folder='static')

# Chemins de base
REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / 'src'
DATA_DIR = SRC_DIR / 'data'

# ============================================
# HELPER FUNCTIONS
# ============================================

def run_python_subprocess(code, cwd=None):
    """Exécute du code Python dans un subprocess isolé"""
    try:
        result = subprocess.run(
            [sys.executable, '-c', code],
            cwd=str(cwd or SRC_DIR),
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return {'success': True, 'data': result.stdout.strip()}
        else:
            return {'success': False, 'error': result.stderr}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_waste_classifier_data(method_name, *args):
    """Récupère des données de waste_classifier"""
    code = f"""
import sys
sys.path.insert(0, '.')
import waste_classifier
import json
try:
    waste_classifier.init_database()
    result = waste_classifier.{method_name}({', '.join(repr(a) for a in args)})
    waste_classifier.cleanup()
    print(json.dumps(result, default=str))
except Exception as e:
    import traceback
    print(json.dumps({{'error': str(e), 'traceback': traceback.format_exc()}}))
"""
    result = run_python_subprocess(code)
    if result['success']:
        try:
            return json.loads(result['data'])
        except:
            return {'error': f"Failed to parse: {result['data']}"}
    return result

# ============================================
# ROUTES - SYSTÈME
# ============================================

@app.route('/api/system/info')
def system_info():
    """Informations système complètes"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
        
        ram = psutil.virtual_memory()
        
        disk = psutil.disk_usage('/')
        
        boot_time = psutil.boot_time()
        import time
        uptime_seconds = int(time.time() - boot_time)
        uptime_str = format_uptime(uptime_seconds)
        
        return jsonify({
            'success': True,
            'system': {
                'hostname': socket.gethostname(),
                'os': os.name,
                'platform': sys.platform
            },
            'cpu': {
                'usage_percent': cpu_percent,
                'cores': cpu_count,
                'frequency_ghz': round(cpu_freq / 1000, 2)
            },
            'ram': {
                'used_gb': round(ram.used / (1024**3), 2),
                'total_gb': round(ram.total / (1024**3), 2),
                'percent': ram.percent
            },
            'disk': {
                'free_gb': round(disk.free / (1024**3), 2),
                'total_gb': round(disk.total / (1024**3), 2),
                'percent': disk.percent
            },
            'uptime': uptime_str,
            'uptime_seconds': uptime_seconds,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gpu/info')
def gpu_info():
    """Informations GPU NVIDIA"""
    try:
        try:
            from pynvml import nvmlInit, nvmlDeviceGetCount, nvmlDeviceGetHandleByIndex, \
                              nvmlDeviceGetName, nvmlDeviceGetTemperature, nvmlDeviceGetMemoryInfo
            nvmlInit()
            device_count = nvmlDeviceGetCount()
        except:
            return jsonify({'success': True, 'gpu': None, 'message': 'NVIDIA GPU not detected'})
        
        if device_count == 0:
            return jsonify({'success': True, 'gpu': None})
        
        device = nvmlDeviceGetHandleByIndex(0)
        name = nvmlDeviceGetName(device).decode('utf-8')
        temp = nvmlDeviceGetTemperature(device, 0)
        mem_info = nvmlDeviceGetMemoryInfo(device)
        
        return jsonify({
            'success': True,
            'gpu': {
                'name': name,
                'temperature_celsius': temp,
                'memory_used_gb': round(mem_info.used / (1024**3), 2),
                'memory_total_gb': round(mem_info.total / (1024**3), 2),
                'memory_percent': round((mem_info.used / mem_info.total) * 100, 1)
            }
        })
    except Exception as e:
        return jsonify({'success': True, 'gpu': None, 'message': str(e)})

# ============================================
# ROUTES - BACS
# ============================================

@app.route('/api/bins/status')
def bins_status():
    """État actuel de tous les bacs"""
    result = get_waste_classifier_data('get_bin_status')
    if 'error' not in result:
        # Formater les données
        bins_dict = {}
        for bin_data in result:
            color = bin_data[0]
            fill_level = bin_data[1]
            item_count = bin_data[2]
            last_emptied = bin_data[3]
            capacity_liters = bin_data[4]
            
            bins_dict[color] = {
                'color': color,
                'fill_percent': fill_level,
                'item_count': item_count,
                'last_emptied': last_emptied,
                'capacity_liters': capacity_liters
            }
        return jsonify({'success': True, 'bins': bins_dict})
    return jsonify(result), 500

@app.route('/api/bins/history')
def bins_history():
    """Historique des détections"""
    limit = request.args.get('limit', 50, type=int)
    result = get_waste_classifier_data('get_detection_history', limit)
    if 'error' not in result:
        return jsonify({'success': True, 'history': result, 'count': len(result)})
    return jsonify(result), 500

@app.route('/api/bins/empty/<color>', methods=['POST'])
def empty_bin(color):
    """Vider un bac"""
    code = f"""
import sys
sys.path.insert(0, '.')
import waste_classifier
try:
    waste_classifier.init_database()
    waste_classifier.empty_bin('{color}')
    waste_classifier.cleanup()
    print('{{"success": true, "message": "Bac {{}} vidé"}}'.format('{color}'))
except Exception as e:
    print('{{"error": "' + str(e).replace('"', '\\\\"') + '"}}')
"""
    result = run_python_subprocess(code)
    if result['success']:
        return jsonify(json.loads(result['data']))
    return jsonify(result), 500

# ============================================
# ROUTES - DÉTECTIONS
# ============================================

@app.route('/api/detections/count')
def detections_count():
    """Nombre total de détections"""
    result = get_waste_classifier_data('get_total_detections')
    return jsonify({'success': True, 'count': result if isinstance(result, int) else 0})

@app.route('/api/detections/by-bin')
def detections_by_bin():
    """Détections regroupées par bac"""
    result = get_waste_classifier_data('get_detections_by_bin')
    if 'error' not in result:
        return jsonify({'success': True, 'data': result})
    return jsonify(result), 500

# ============================================
# ROUTES - CONFIGURATION
# ============================================

@app.route('/api/config/read')
def read_config():
    """Lire la configuration"""
    try:
        cfg_path = SRC_DIR / 'config.py'
        with open(cfg_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'success': True, 'content': content, 'path': str(cfg_path)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config/save', methods=['POST'])
def save_config():
    """Sauvegarder la configuration"""
    try:
        data = request.get_json() or {}
        content = data.get('content', '')
        cfg_path = SRC_DIR / 'config.py'
        with open(cfg_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True, 'message': 'Configuration sauvegardée', 'path': str(cfg_path)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/config/validate', methods=['POST'])
def validate_config():
    """Valider la syntaxe de la configuration"""
    try:
        data = request.get_json() or {}
        content = data.get('content', '')
        compile(content, '<config>', 'exec')
        return jsonify({'success': True, 'message': 'Configuration valide'})
    except SyntaxError as e:
        return jsonify({'success': False, 'error': f'Erreur syntaxe: {e.msg} ligne {e.lineno}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ============================================
# ROUTES - ÉQUIPEMENTS
# ============================================

@app.route('/api/equipment/camera')
def camera_status():
    """État de la caméra"""
    code = """
import cv2
import json
try:
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        cap.release()
        if ret:
            print(json.dumps({'connected': True, 'source': 0}))
        else:
            print(json.dumps({'connected': False, 'error': 'Impossible de capturer'}))
    else:
        print(json.dumps({'connected': False, 'error': 'Caméra non accessible'}))
except Exception as e:
    print(json.dumps({'connected': False, 'error': str(e)}))
"""
    result = run_python_subprocess(code)
    if result['success']:
        data = json.loads(result['data'])
        return jsonify({'success': True, 'camera': data})
    return jsonify({'success': True, 'camera': {'connected': False, 'error': 'Vérification échouée'}})

@app.route('/api/equipment/arduino')
def arduino_status():
    """État d'Arduino"""
    code = """
import json
try:
    import serial
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    arduino_found = False
    arduino_port = None
    for port in ports:
        if 'CH340' in port.description or 'Arduino' in port.description or 'USB' in port.description:
            arduino_found = True
            arduino_port = port.device
            break
    print(json.dumps({'connected': arduino_found, 'port': arduino_port, 'ports_found': [p.device for p in ports]}))
except Exception as e:
    print(json.dumps({'connected': False, 'error': str(e)}))
"""
    result = run_python_subprocess(code)
    if result['success']:
        data = json.loads(result['data'])
        return jsonify({'success': True, 'arduino': data})
    return jsonify({'success': True, 'arduino': {'connected': False}})

# ============================================
# ROUTES - INTERFACE
# ============================================

@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

@app.route('/api/image/<path:image_path>')
def serve_image(image_path):
    """Servir une image de détection"""
    from flask import send_file
    try:
        # Sécurité : s'assurer que le chemin est dans le répertoire autorisé
        full_path = DATA_DIR / image_path
        
        # Vérifier que le chemin existe et qu'il ne sort pas du répertoire
        if not full_path.exists():
            return jsonify({'error': 'Image not found'}), 404
        
        # Vérifier que le chemin résolu est bien dans data/
        if not str(full_path.resolve()).startswith(str(DATA_DIR.resolve())):
            return jsonify({'error': 'Access denied'}), 403
        
        return send_file(full_path, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# HELPER
# ============================================

def format_uptime(seconds):
    """Formater les secondes en jours/heures/minutes"""
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    return f"{days}j {hours}h {minutes}m"

# ============================================
# MAIN
# ============================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
