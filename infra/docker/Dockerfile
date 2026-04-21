FROM python:3.13.13-slim

WORKDIR /backend

# Devemos copiar o requirements antes, de acordo com a documentação
# A razão é possibilitar que o Docker utilize os requirements do cache se o arquivo não mudar, porque caso contrário um erro no sistema
# invalidaria toda aquela camada da estrutura, e forçaria o Docker a demorar mais rodando o requirements.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]