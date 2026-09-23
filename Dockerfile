FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
ENV MPLBACKEND=Agg
# Batch job: runs RFM segmentation and writes segmentation_report.md + PNGs
CMD ["python", "segmentation.py"]
