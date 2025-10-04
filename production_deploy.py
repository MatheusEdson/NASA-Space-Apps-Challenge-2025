"""
Script para deployment em produção
Configurações específicas para hospedagem no VPS
"""

import subprocess
import os
import json
from pathlib import Path

def create_production_config():
    """Cria configurações específicas para produção"""
    
    print("Configurando sistema para produção...")
    
    # Configurações do Streamlit para produção
    streamlit_config = """
[server]
port = 8501
address = "0.0.0.0"
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans seri"

[browser]
gatherUsageStats = false
    """
    
    # Criar diretório de configuração
    config_dir = Path.home() / ".streamlit"
    config_dir.mkdir(exist_ok=True)
    
    # Salvar configuração
    with open(config_dir / "config.toml", "w") as f:
        f.write(streamlit_config)
    
    print("✅ Configuração Streamlit salva!")
    
    return True

def create_systemd_service():
    """Cria arquivo de serviço systemd para Linux"""
    
    service_content = """[Unit]
Description=NASA Space Apps Exoplanet Detection System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/spaceapps
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 -m streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
    
    with open("spaceapps.service", "w") as f:
        f.write(service_content)
    
    print("✅ Arquivo de serviço systemd criado!")
    
    return True

def create_docker_config():
    """Cria configuração Docker para deploy"""
    
    dockerfile_content = """FROM python:3.10-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p models data results logs

# Expor porta
EXPOSE 8501

# Comando para executar
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
"""
    
    dockerignore_content = """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
*.joblib
*.pkl
"""
    
    docker_compose_content = """version: '3.8'

services:
  spaceapps:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./models:/app/models
      - ./data:/app/data
      - ./results:/app/results
      - ./logs:/app/logs
    restart: unless-stopped
    container_name: spaceapps-challenge

# Nginx reverse proxy (opcional)
services:
  reverse-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - spaceapps
    restart: unless-stopped
"""
    
    # Salvar arquivos
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    with open(".dockerignore", "w") as f:
        f.write(dockerignore_content)
    
    with open("docker-come.yml", "w") as f:
        f.write(docker_compose_content)
    
    print("✅ Configuração Docker criada!")
    return True

def create_nginx_config():
    """Cria configuração Nginx para proxy reverso"""
    
    nginx_config = '''events {
    worker_connections 1024;
}

http {
    upstream spaceapps {
        server spaceapps:8501;
    }

    server {
        listen 80;
        server_name spaceappschallenge.matheusedson.com;

        location / {
            proxy_pass http://spaceapps;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            
            # Security headers
            add_header X-Frame-Options DENY;
            add_header X-Content-Type-Options nosniff;
            add_header X-XSS-Protection "1; mode=block";
        }
    }

    # HTTPS (certificado Let's Encrypt)
    server {
        listen 443 ssl http2;
        server_name spaceappschallenge.matheusedson.com;

        ssl_certificate /etc/ssl/certs/fullchain.pem;
        ssl_certificate_key /etc/ssl/certs/privkey.pem;

        location / {
            proxy_pass http://spaceapps;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}'''
    
    with open("nginx.conf", "w") as f:
        f.write(nginx_config)
    
    print("✅ Configuração Nginx criada!")
    return True

def create_security_config():
    """Cria configurações de segurança"""
    
    security_config = {
        "rate_limiting": {
            "enabled": True,
            "max_requests_per_minute": 60,
            "max_upload_size_mb": 50,
            "blocked_countries": [],
            "allowed_ips": []
        },
        "ssl": {
            "enabled": True,
            "certificate_path": "/etc/ssl/certs/",
            "auto_renew": True
        },
        "logging": {
            "access_logs": True,
            "error_logs": True,
            "log_level": "INFO",
            "retention_days": 30
        },
        "backup": {
            "enabled": True,
            "interval_hours": 24,
            "retention_days": 7,
            "path": "/backup/spaceapps"
        }
    }
    
    with open("security_config.json", "w") as f:
        json.dump(security_config, f, indent=2)
    
    print("✅ Configurações de segurança criadas!")
    return True

def create_deploy_script():
    """Cria script de deploy automatizado"""
    
    deploy_script = '''#!/bin/bash

# Script de deploy para produção
# VPS: spaceappschallenge.matheusedson.com

echo "🚀 Iniciando deploy do NASA Space Apps Challenge..."

# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3 python3-pip nginx certbot python3-certbot-nginx docker.io docker-come

# Configurar firewall
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw --force enable

# Configurar certificado SSL
sudo certbot --nginx -d spaceappschallenge.matheusedson.com

# Clonar repositório (se necessário)
# git clone <seu-repo> /var/www/spaceapps

# Restaurar permissões
sudo chown -R www-data:www-data /var/www/spaceapps

# Configurar serviço systemd
sudo cp spaceapps.service /etc/systemd/system/
sudo systemctl enable spaceapps
sudo systemctl start spaceapps

# Configurar Nginx
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl reload nginx

echo "✅ Deploy concluído!"
echo "🌐 Acesse: https://spaceappschallenge.matheusedson.com"

# Status dos serviços
echo "📊 Status dos serviços:"
sudo systemctl status spaceapps
sudo systemctl status nginx
'''
    
    with open("deploy.sh", "w") as f:
        f.write(deploy_script)
    
    # Tornar executável
    os.chmod("deploy.sh", 0o755)
    
    print("✅ Script de deploy criado!")
    return True

def main():
    """Função principal de configuração"""
    
    print("🌌 CONFIGURAÇÃO PARA DEPLOY EM PRODUÇÃO")
    print("=" * 50)
    
    # Criar configurações
    create_production_config()
    create_systemd_service()
    create_docker_config()
    create_nginx_config()
    create_security_config()
    create_deploy_script()
    
    print("\n✅ TODAS AS CONFIGURAÇÕES CRIADAS!")
    print("\n📋 Arquivos gerados:")
    print("  • Dockerfile")
    print("  • docker-compose.yml")
    print("  • nginx.conf")
    print("  • spaceapps.service")
    print("  • deploy.sh")
    print("  • security_config.json")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("1. Upload dos arquivos para o VPS")
    print("2. Execute: chmod +x deploy.sh")
    print("3. Execute: sudo ./deploy.sh")
    print("4. Configure domínio: spaceappschallenge.matheusedson.com")
    print("5. Acesse: https://spaceappschallenge.matheusedson.com")
    
    print("\n🌐 Sistema pronto para hospedagem!")

if __name__ == "__main__":
    main()
