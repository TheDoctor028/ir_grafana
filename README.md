# IRacing Grafana

## Description
This project is a Grafana dashboard for iRacing telemetry data. 
It uses the iRacing SDK to get the telemetry data and sends it to Prometheus. 
The Grafana dashboard reads the data from the Prometheus database and displays it.


## Requirements
- Python 3.7
- Pip
- Docker

## Installation

### 1. Clone the repository

### 2. Install the requirements
```bash
pip install -r requirements.txt
```

### 3. Create configuration file
This should be the same lvl as the `main.py` file. (Will be changed in the future)
```bash
cp config.example.yaml config.yaml
```

### 5. Start the required services
```bash
docker-compose up
```

### 6. Start the python script
```bash
python main.py
```

You will find the Grafana dashboard at `http://localhost:3000` and the Prometheus gw at `http://localhost:9091`
