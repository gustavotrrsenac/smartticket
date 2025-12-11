# Imagem base pequena com Python
FROM python:3.11-slim

# Evita buffers em logs
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY app.py .

# Expõe a porta usada pela app
EXPOSE 5000

# Comando de inicialização
CMD ["python", "app.py"]
