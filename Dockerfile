FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY tests/ tests/

CMD ["pytest", "-sv", "--html=test-results/report.html", "--self-contained-html", "--no-video"]
