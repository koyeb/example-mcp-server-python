FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8080

CMD ["python", "-c", "from main import mcp; mcp.run(transport='streamable-http')"]
