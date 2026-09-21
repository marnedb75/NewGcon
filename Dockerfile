# Usa uma imagem oficial do Python leve baseada em Debian (Alpine/Slim)
FROM python:3.11-slim

# Evita que o Python escreva arquivos .pyc no disco e força o log em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para compilação/conexão
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos e instala as dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código-fonte da aplicação para dentro do container
COPY . /app/

# Expõe a porta 5000 (onde a aplicação roda)
EXPOSE 5000

# Comando padrão para rodar a aplicação via Gunicorn em produção/container
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]