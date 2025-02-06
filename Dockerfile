# Usa uma imagem base do Python
FROM python:3.10-slim

# Instala ffmpeg e outras dependências
RUN apt-get update && apt-get install -y ffmpeg

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta do Railway
EXPOSE 8080

# Comando para iniciar o servidor FastAPI com uvicorn
CMD uvicorn backend:app --host 0.0.0.0 --port ${PORT:-8080}
