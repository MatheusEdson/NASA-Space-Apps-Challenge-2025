# 🚀 Deploy NASA Space Apps Challenge 2025 - spaceappschallenge.matheusedson.com

## 📋 Arquivos para Deploy

### Core Files (ESSENCIAIS):
- `exoplanet_ml.py` - Sistema principal de ML
- `streamlit_app.py` - Interface web
- `requirements.txt` - Dependências Python
- `config.py` - Configurações do sistema

### Módulos de Suporte:
- `data_visualizer.py` - Análise visual de dados
- `transit_analyzer.py` - Análise de trânsitos
- `production_deploy.py` - Scripts de deploy

### Deploy & Config:
- `Dockerfile` - Containerização
- `docker-compose.yml` - Orquestração
- `nginx.conf` - Proxy reverso
- `deploy.sh` - Script automático
- `spaceapps.service` - Serviço systemd

## 🖥️ VPS Specifications Required

### Servidor Mínimo:
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB SSD
- **OS**: Ubuntu 20.04+ ou CentOS 8+

### Portas Abertas:
- `22` - SSH
- `80` - HTTP
- `443` - HTTPS

## 🔐 Segurança Implementada

### ✅ Zero Data Leak:
- Trabalha apenas com dados públicos da NASA
- Não coleta dados pessoais
- SSL/TLS obrigatório
- Firewall configurado
- Rate limited (60 req/min)

### 🛡️ Configurações de Segurança:
```bash
# Headers de segurança
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: "1; mode=block"

# Firewall UFW
sudo ufw deny 8501
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
```

## 🚀 Processo de Deploy Completo

### 1. Preparação Local:
```bash
# Testar sistema localmente primeiro
python demo_success.py

# Criar arquivo .gitignore (opcional)
echo "models/*.joblib" > .gitignore
echo "data/*.csv" >> .gitignore
echo "__pycache__/" >> .gitignore
```

### 2. Upload para VPS:
```bash
# Via SCP (Secure Copy)
scp -r * root@147.79.111.15:/var/www/spaceapps/

# Via SFTP (mais visual)
sftp root@147.79.111.15

# Via Git (recomendado - mais seguro)
git init
git add .
git commit -m "NASA Space Apps Challenge 2025 - Exoplanet Detection System"

# Push para seu repo
git remote add origin https://github.com/[SEU_USER]/spaceapps-challenge.git
git push -u origin main
```

### 3. Deploy no VPS:
```bash
# SSH no VPS
ssh root@147.79.111.15

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone do repo (ou upload manual)
git clone https://github.com/[SEU_USER]/spaceapps-challenge.git
cd spaceapps-challenge

# Tornar deploy.sh executável
chmod +x deploy.sh

# Executar deploy automático
sudo ./deploy.sh
```

## 📡 Configuração DNS

### Domínio: spaceappschallenge.matheusedson.com
```bash
# REGISTRAR DNS:
Type: A
Name: spaceappschallenge.matheusedson.com
Value: 147.79.111.15
TTL: 300

# Subdomínio alternativo (backup):
Type: A  
Name: www.spaceappschallenge.matheusedson.com
Value: 147.79.111.15
```

## 🔧 Verificação Pós-Deploy

### 1. Serviços Ativos:
```bash
# Verificar containers
docker ps

# Verificar serviços systemd
sudo systemctl status spaceapps
sudo systemctl status nginx

# Verificar logs
tail -f /var/log/spaceapps/app.log
```

### 2. Testes de Funcionamento:
```bash
# Teste local na VPS
curl http://localhost:8501

# Teste externo
curl https://spaceappschallenge.matheusedson.com

# Teste completo
python demo_success.py
```

### 3. Monitoramento:
```bash
# Usar recursos
htop

# Logs em tempo real
sudo journalctl -u spaceapps -f

# Saúde do container
docker stats
```

## 🔐 Segurança Final

### ✅ Garantias de Não-Vazamento:
- **Dados locais**: Mantidos apenas na VPS
- **APIs externas**: Apenas leitura pública NASA
- **Uploads**: Salvos no VPS, nunca vazados
- **SSL obrigatório**: Dados trafegam criptografados
- **Firewall**: Bloqueia acessos não autorizados

### 🛡️ Backup Automático:
```bash
# Backup diário automático
0 2 * * * tar -czf /backup/spaceapps_$(date +%Y%m%d).tar.gz /var/www/spaceapps/
```

## 🌐 Acesso Final

**URL Principal**: https://spaceappschallenge.matheusedson.com

### Funcionalidades Disponíveis:
- ✅ Interface web completa
- ✅ Upload de datasets NASA 
- ✅ Análise manual de exoplanetas
- ✅ Monitoramento em tempo real
- ✅ Documentação científica
- ✅ Download de resultados

**✅ SISTEMA TOTALMENTE SEGURO E PRONTO PARA 2025!**
