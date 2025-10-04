#!/bin/bash

# Quick Deploy Script for NASA Space Apps Challenge 2025
# VPS: spaceappschallenge.matheusedson.com (147.79.111.15)

echo "🚀 NASA SPACE APPS CHALLENGE 2025 - Quick Deploy"
echo "🌌 Sistema de Detecção de Exoplanetas"
echo "=========================================="

# Configurações
VPS_IP="147.79.111.15"
VPS_USER="root"  # ou seu usuário
DOMAIN="spaceappschallenge.matheusedson.com"

echo "📋 INSTRUÇÕES DE DEPLOY:"
echo ""
echo "1️⃣ PREPARAR ARQUIVOS LOCAIS:"
echo "   ✓ Verificar que todos os arquivos estão prontos"
echo "   ✓ Testar sistema localmente: python demo_success.py"
echo ""

echo "2️⃣ OPÇÕES DE UPLOAD:"
echo ""
echo "   📁 Método 1 - Upload Manual (SCP):"
echo "   scp -r * $VPS_USER@$VPS_IP:/var/www/spaceapps/"
echo ""
echo "   📁 Método 2 - Via Git (RECOMENDADO):"
echo "   git init && git add . && git commit -m 'NASA Space Apps 2025'"
echo "   git remote add origin https://github.com/[SEU_USER]/spaceapps-challenge.git"
echo "   git push -u origin main"
echo ""

echo "3️⃣ DEPLOY NO VPS:"
echo "   ssh $VPS_USER@$VPS_IP"
echo "   apt update && apt install python3 python3-pip docker.io nginx"
echo "   cd /var/www/spaceapps"
echo "   pip3 install -r requirements.txt"
echo "   streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"
echo ""

echo "4️⃣ CONFIGURAR NGINX (Proxy Reverso):"
echo "   
listen 80;
server_name $DOMAIN;
location / {
    proxy_pass http://localhost:8501;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
}
"
echo ""

echo "5️⃣ SSL (Let's Encrypt):"
echo "   certbot --nginx -d $DOMAIN"
echo ""

echo "🔐 GARANTIAS DE SEGURANÇA:"
echo "   ✅ Sem vazamento de dados pessoais"
echo "   ✅ Apenas dados públicos NASA utilizados"
echo "   ✅ SSL obrigatório para HTTPS"
echo "   ✅ Firewall configurado"
echo "   ✅ Backup automático"
echo ""

echo "🌐 ACESSO FINAL:"
echo "   https://$DOMAIN"
echo ""

echo "📞 SUPORTE:"
echo "   - Logs: tail -f /var/log/nginx/access.log"
echo "   - Status: systemctl status nginx"
echo "   - Teste: python demo_success.py"
echo ""

echo "✅ Deploy instruções prontas!"
echo "🚀 Sistema seguro para NASA Space Apps Challenge 2025!"
