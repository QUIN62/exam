import requests

class classGet:
    def __init__(self, url):
        self.url = url

    def get_all_records(self):
        try:
            response = requests.get(f"{self.url}/GODS", timeout=5)
            response.raise_for_status()
            records = response.json()
            print("Datos obtenidos (todos los registros):", records)  # Mensaje de depuración
            return records
        except requests.Timeout:
            print("Error: La solicitud de todos los registros agotó el tiempo de espera.")
            return []
        except requests.RequestException as e:
            print(f"Error al obtener todos los registros: {e}")
            return []

    def get_record_by_id(self, record_id):
        try:
            response = requests.get(f"{self.url}/GODS/{record_id}", timeout=5)
            response.raise_for_status()
            record = response.json()
            print("Registro obtenido:", record)  # Mensaje de depuración
            return record
        except requests.Timeout:
            print(f"Error: La solicitud para el registro {record_id} agotó el tiempo de espera.")
            return None
        except requests.RequestException as e:
            print(f"Error al obtener el registro con id {record_id}: {e}")
            return None
