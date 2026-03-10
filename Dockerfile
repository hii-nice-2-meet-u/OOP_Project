FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir "mcp[cli]"

COPY BGC.py .
COPY BGC_MENU.py .
COPY BGC_PAYMENT.py .
COPY BGC_PERSON.py .
COPY BGC_PLAY_SESSION.py .
COPY BGC_RESERVATION.py .
COPY BGC_SYSTEM.py .
COPY ENUM_STATUS.py .
COPY _Project_instance.py .
COPY _Project_mcp.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "_Project_mcp.py"]

# รัน docker
# docker build -t bgc-mcp .
# docker run -it bgc-mcp
# config claude
# {
#   "mcpServers": {
#     "BoardGameCafe": {
#       "command": "docker",
#       "args": ["run", "-i", "--rm", "bgc-mcp"]
#     }
#   }
# }