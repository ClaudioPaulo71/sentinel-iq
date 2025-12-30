# Dockerfile Multistage para máxima performance (Padrão Sênior)

# Etapa 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Etapa 2: Runtime (Imagem final mais leve)
FROM python:3.11-slim

WORKDIR /app

# Copiar bibliotecas instaladas da etapa anterior
COPY --from=builder /root/.local /root/.local
COPY . .

# Garantir que os binários do python estejam no PATH
ENV PATH=/root/.local/bin:$PATH

# Expor portas para o FastAPI (8000) e Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Comando para rodar ambos (Para teste simplificado usamos o Streamlit que chama o código)
# Nota: Em produção real usaríamos Docker Compose para separar os dois.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]