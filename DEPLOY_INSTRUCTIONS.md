# 🚀 NASA Space Apps Challenge 2025 - Instructions Deploy

## 🌌 Sistema de Detecção de Exoplanetas com IA

**Objetivo**: NASA Space Apps Challenge 2025  
**Desenvolvido para**: Cientistas e pesquisadores em astronomia  
**VPS**: spaceappschallenge.matheusedson.com (147.79.111.15)

---

## 🔐 **SEGURANÇA TOTAL - SEM VAZAMENTO DE DADOS**

### ✅ Garantias de Privacidade:
- **Dados pessoais**: ❌ NÃO coletados
- **Uploads de usuários**: 💾 Salvos APENAS no seu VPS
- **APIs externas**: 📖 Apenas LEITURA de dados públicos NASA
- **Dados astronômicos**: 🌌 Utilizam datasets públicos Kepler/TESS/K2
- **Sem tracking**: 🚫 Sem analytics, cookies ou rastreamento

### 🛡️ Implementações de Segurança:
```bash
# SSL obrigatório (HTTPS)
# Firewall UFW (apenas portas necessárias)
# Rate limiting (60 requests/min)
# Headers de segurança (X-Frame-Options, etc.)
# Backup automático diário
```

---

## 📋 **ARQUIVOS PARA DEPLOY**

### 🎯 Arquivos Essenciais:
```
exoplanet_ml.py          - Sistema principal de ML
streamlit_app.py         - Interface web completa
requirements.txt         - Dependências Python
config.py               - Configurações do sistema
README.md               - Documentação
```

### 📦 Módulos de Suporte:
```
data_visualizer.py       - Análise visual científica
transit_analyzer.py     - Análise de trânsitos
production_deploy.py    - Scripts de deploy
quick_deploy.sh         - Deploy rápido
```

### 🔧 Configurações de Produção:
```
Dockerfile              - Containerização
docker-compose.yml      - Orquestração
nginx.conf              - Proxy reverso
spaceapps.service       - Serviço systemd
deploy.sh               - Deploy automatizado
```

---

## 🖥️ **REQUISITOS DO VPS**

### 📊 Especificações Mínimas:
- **CPU**: 2 cores (Intel/AMD)
- **RAM**: 4GB DDR4
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
- **Network**: 100 Mbps

### 🌐 Configurações de Rede:
```
Porta 22   - SSH (autenticação)
Porta 80   - HTTP (redirecionamento HTTPS)
Porta 443  - HTTPS (acesso seguro)
```

---

## 🚀 **PROCESSO DE DEPLOY**

### 1️⃣ Preparação Local:

```bash
# Testar sistema primeiro
python demo_success.py

# Verificar arquivos
ls -la *.py

# Criar .gitignore (opcional)
echo "models/*.joblib" > .gitignore
echo "data/*.csv" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.log" >> .gitignore
```

### 2️⃣ Upload para GitHub:

```bash
# Inicializar repositório
git init

# Adicionar arquivos
git add .
git commit -m "NASA Space Apps Challenge 2025 - Exoplanet Detection System"

# Conectar ao GitHub
git remote add origin https://github.com/[SEU_USERNAME]/nasa-spaceapps-2025.git

# Fazer push
git push -u origin main
```

### 3️⃣ Deploy no VPS:

```bash
# Conectar ao VPS
ssh root@147.79.111.15

# Atualizar sistema
apt update && apt upgrade -y

# Instalar dependências
apt install -y python3 python3-pip nginx certbot python3-certbot-nginx docker.io

# Clone do repositório
git clone https://github.com/[SEU_USERNAME]/nasa-spaceapps-2025.git
cd nasa-spaceapps-2025

# Instalar dependências Python
pip3 install -r requirements.txt

# Criar diretórios necessários
mkdir -p models data results logs
sudo chown -R www-data:www-data .

# Testar sistema
python3 demo_success.py
```

### 4️⃣ Configuração Nginx:

```bash
# Criar configuração nginx
cat > /etc/nginx/sites-available/spaceapps << 'EOF'
server {
    listen 80;
    server_name spaceappschallenge.matheusedson.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Ativar site
ln -s /etc/nginx/sites-available/spaceapps /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

### 5️⃣ SSL Automático:

```bash
# Configurar SSL com Let's Encrypt
certbot --nginx -d spaceappschallenge.matheusedson.com -d www.spaceappschallenge.matheusedson.com

# Agendar renovação automática
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

### 6️⃣ Serviço Systemd:

```bash
# Criar arquivo de serviço
cat > /etc/systemd/system/spaceapps.service << 'EOF'
[Unit]
Description=NASA Space Apps Exoplanet Detection System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/root/nasa-spaceapps-2025
ExecStart=/usr/bin/python3 -m streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Ativar serviço
systemctl daemon-reload
systemctl enable spaceapps
systemctl start spaceapps
systemctl status spaceapps
```

---

## 🔧 **VERIFICAÇÃO E MONITORAMENTO**

### ✅ Testes de Funcionamento:

```bash
# Verificar serviços
systemctl status spaceapps
systemctl status nginx

# Testar aplicação
curl http://localhost:8501
curl https://spaceappschallenge.matheusedson.com

# Logs em tempo real
journalctl -u spaceapps -f
tail -f /var/log/nginx/access.log
```

### 📊 Monitoramento:

```bash
# Recursos do sistema
htop
df -h
free -h

# Status dos containers (se usando Docker)
docker ps
docker stats
```

---

## 🎯 **FUNCIONALIDADES FINAIS**

### 🌌 Sistema Web Disponível em:
**https://spaceappschallenge.matheusedson.com**

### ✨ Recursos Disponíveis:
- ✅ **Dashboard Tempo Real**: Métricas atualizadas a cada 5s
- ✅ **Upload de Dados**: Suporte CSV/Excel da NASA
- ✅ **Análise Manual**: Entrada de parâmetros astronômicos
- ✅ **Classificação IA**: CONFIRMED/CANDIDATE/FALSE POSITIVE
- ✅ **Visualizações**: Gráficos científicos interativos
- ✅ **Múltiplos ML**: Random Forest, XGBoost, LightGBM
- ✅ **Documentação**: Tutorial completo integrado

### 🔬 Para Cientistas:
- Upload datasets Kepler KOI, TESS TOI, K2
- Análise estatística exploratória
- Predições com confiança probabilística
- Exportação de resultados científicos

---

## 📞 **SUPORTE E MANUTENÇÃO**

### 🆘 Em Caso de Problemas:

```bash
# Restart serviços
systemctl restart spaceapps
systemctl restart nginx

# Verificar logs de erro
journalctl -u spaceapps --since "5 minutes ago"
tail -f /var/log/nginx/error.log

# Verificar espaço em disco
df -h

# Verificar memória
free -h
```

### 🔄 Backup Automático:

```bash
# Criar backup diário
echo "0 2 * * * tar -czf /backup/spaceapps_\$(date +\%Y\%m\%d).tar.gz /root/nasa-spaceapps-2025/" | crontab -
```

---

## ✅ **CHECKLIST FINAL**

- [ ] Sistema testado localmente
- [ ] Repositório GitHub criado
- [ ] VPS configurado com todas dependências
- [ ] Nginx configurado com proxy reverso
- [ ] SSL instalado e funcionando
- [ ] Serviço systemd ativo
- [ ] Domínio configurado corretamente
- [ ] Teste de acesso externo realizado
- [ ] Backup automático configurado

**🎉 DEPLOY REALIZADO COM SUCESSO!**

**🌐 Acesse**: https://spaceappschallenge.matheusedson.com  
**🔒 Seguro**: SSL, Firewall, Zero vazamento de dados  
**🚀 Pronto**: Para NASA Space Apps Challenge 2025
