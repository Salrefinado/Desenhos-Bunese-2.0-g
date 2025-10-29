import os
from flask import Flask, jsonify, render_template, request, abort

app = Flask(__name__)

# Define o diretório base para as imagens
IMAGE_DIR = os.path.join(app.static_folder, 'images')

@app.route('/')
def index():
    """Serve a página principal da aplicação."""
    return render_template('index.html')

@app.route('/get-groups')
def get_groups():
    """Lista os diretórios principais (grupos) em static/images."""
    try:
        groups = [d for d in os.listdir(IMAGE_DIR) 
                  if os.path.isdir(os.path.join(IMAGE_DIR, d))]
        return jsonify(groups)
    except FileNotFoundError:
        return jsonify({"error": "Diretório de imagens não encontrado"}), 404

@app.route('/get-subfolders')
def get_subfolders():
    """Lista as subpastas dentro de um grupo específico."""
    group = request.args.get('group')
    if not group:
        return jsonify({"error": "Parâmetro 'group' ausente"}), 400

    group_path = os.path.join(IMAGE_DIR, group)
    if not os.path.isdir(group_path):
        return jsonify({"error": "Grupo não encontrado"}), 404

    try:
        subfolders = [d for d in os.listdir(group_path)
                      if os.path.isdir(os.path.join(group_path, d))]
        return jsonify(subfolders)
    except FileNotFoundError:
        return jsonify({"error": "Diretório do grupo não encontrado"}), 404

@app.route('/get-images')
def get_images():
    """Lista os arquivos .png dentro de uma subpasta."""
    group = request.args.get('group')
    subfolder = request.args.get('subfolder')

    if not group or not subfolder:
        return jsonify({"error": "Parâmetros 'group' ou 'subfolder' ausentes"}), 400

    image_path = os.path.join(IMAGE_DIR, group, subfolder)
    if not os.path.isdir(image_path):
        return jsonify({"error": "Caminho não encontrado"}), 404

    try:
        images = [f for f in os.listdir(image_path)
                  if os.path.isfile(os.path.join(image_path, f)) and f.lower().endswith('.png')]
        return jsonify(images)
    except FileNotFoundError:
        return jsonify({"error": "Diretório de imagens não encontrado"}), 404


if __name__ == '__main__':
    # Lê a porta do ambiente (para produção) ou usa 5000 como padrão (para desenvolvimento)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)