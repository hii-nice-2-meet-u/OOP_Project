FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir "mcp[cli]"

COPY BGC.py \
     BGC_MENU.py \
     BGC_PAYMENT.py \
     BGC_PERSON.py \
     BGC_PLAY_SESSION.py \
     BGC_RESERVATION.py \
     BGC_SYSTEM.py \
     ENUM_STATUS.py \
     demo__instance.py \
     demo_8_mcp.py \
     ./

EXPOSE 8000

CMD ["python", "demo_8_mcp.py"]
# รัน cmd ข้างล่างตอนเปิด Docker Desktop 
# docker run -p 8000:8000 ipao69/bgc-mcp:latest