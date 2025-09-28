import requests
import json
from datetime import datetime
import os

class SiigoAPI:
    def __init__(self, username, access_key, partner_id):
        """
        Inicializar el cliente de Siigo API
        
        Args:
            username (str): Usuario de Siigo
            access_key (str): Clave de acceso de Siigo
            partner_id (str): ID del partner de Siigo
        """
        self.username = username
        self.access_key = access_key
        self.partner_id = partner_id
        self.base_url = "https://api.siigo.com/v1"
        self.token = None
        self.token_expires = None
        
    def authenticate(self):
        """
        Autenticar con la API de Siigo y obtener token de acceso
        """
        auth_url = f"{self.base_url}/auth"
        
        headers = {
            "Content-Type": "application/json",
            "Partner-Id": self.partner_id
        }
        
        payload = {
            "username": self.username,
            "access_key": self.access_key
        }
        
        try:
            response = requests.post(auth_url, headers=headers, json=payload)
            response.raise_for_status()
            
            auth_data = response.json()
            self.token = auth_data["access_token"]
            print("✅ Autenticación exitosa")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de autenticación: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta del servidor: {e.response.text}")
            return False
    
    def get_headers(self):
        """
        Obtener headers para las peticiones autenticadas
        """
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "Partner-Id": self.partner_id
        }
    
    def get_customers(self):
        """
        Obtener lista de clientes/proveedores
        """
        url = f"{self.base_url}/customers"
        headers = self.get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error obteniendo clientes: {e}")
            return None
    
    def get_products(self):
        """
        Obtener lista de productos
        """
        url = f"{self.base_url}/products"
        headers = self.get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error obteniendo productos: {e}")
            return None
    
    def create_purchase_invoice(self, invoice_data):
        """
        Crear una factura de compra
        
        Args:
            invoice_data (dict): Datos de la factura
        """
        url = f"{self.base_url}/purchase-invoices"
        headers = self.get_headers()
        
        try:
            response = requests.post(url, headers=headers, json=invoice_data)
            response.raise_for_status()
            
            result = response.json()
            print("✅ Factura de compra creada exitosamente")
            print(f"ID de la factura: {result.get('id', 'N/A')}")
            print(f"Número: {result.get('number', 'N/A')}")
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error creando factura: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta del servidor: {e.response.text}")
            return None

def create_sample_invoice():
    """
    Crear una factura de ejemplo
    """
    # Obtener fecha actual
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    invoice_data = {
        "document": {
            "id": 24  # ID del tipo de documento (Factura de compra)
        },
        "date": current_date,
        "customer": {
            "identification": "900123456",  # NIT del proveedor
            "branch_office": 0
        },
        "cost_center": 235,  # ID del centro de costos (opcional)
        "currency": {
            "code": "COP"
        },
        "total": 238000,  # Total de la factura
        "observations": "Factura de compra generada automáticamente",
        "items": [
            {
                "code": "Item01",  # Código del producto/servicio
                "description": "Producto de prueba",
                "quantity": 2,
                "price": 100000,
                "discount": 0,
                "taxes": [
                    {
                        "id": 13156,  # ID del impuesto IVA 19%
                        "value": 38000  # Valor del impuesto
                    }
                ]
            }
        ],
        "payments": [
            {
                "id": 5936,  # ID del medio de pago
                "value": 238000,
                "due_date": current_date
            }
        ]
    }
    
    return invoice_data

def main():
    """
    Función principal
    """
    # Configuración - Reemplaza con tus credenciales reales
    USERNAME = "tu_usuario@empresa.com"
    ACCESS_KEY = "tu_access_key_aqui"
    PARTNER_ID = "tu_partner_id_aqui"
    
    # También puedes usar variables de entorno para mayor seguridad
    # USERNAME = os.getenv('SIIGO_USERNAME', 'tu_usuario@empresa.com')
    # ACCESS_KEY = os.getenv('SIIGO_ACCESS_KEY', 'tu_access_key')
    # PARTNER_ID = os.getenv('SIIGO_PARTNER_ID', 'tu_partner_id')
    
    print("🚀 Iniciando creación de factura de compra en Siigo...")
    
    # Crear instancia del cliente
    siigo = SiigoAPI(USERNAME, ACCESS_KEY, PARTNER_ID)
    
    # Autenticar
    if not siigo.authenticate():
        print("❌ No se pudo autenticar. Verifica tus credenciales.")
        return
    
    # Crear datos de la factura
    invoice_data = create_sample_invoice()
    
    print("\n📄 Datos de la factura:")
    print(json.dumps(invoice_data, indent=2, ensure_ascii=False))
    
    # Crear la factura
    print("\n📤 Enviando factura a Siigo...")
    result = siigo.create_purchase_invoice(invoice_data)
    
    if result:
        print("\n✅ ¡Factura creada exitosamente!")
        print(f"Resultado: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print("\n❌ No se pudo crear la factura")

def example_with_real_data():
    """
    Ejemplo de cómo usar el script con datos reales
    """
    print("\n" + "="*50)
    print("EJEMPLO DE USO CON DATOS REALES")
    print("="*50)
    
    # Configurar credenciales
    siigo = SiigoAPI(
        username="tu_usuario@empresa.com",
        access_key="tu_access_key",
        partner_id="tu_partner_id"
    )
    
    # Autenticar
    if siigo.authenticate():
        # Obtener clientes para usar IDs reales
        print("\n📋 Obteniendo lista de proveedores...")
        customers = siigo.get_customers()
        if customers:
            print(f"Encontrados {len(customers)} proveedores")
            # Mostrar los primeros 3 proveedores como ejemplo
            for i, customer in enumerate(customers[:3]):
                print(f"  {i+1}. {customer.get('name', 'N/A')} - NIT: {customer.get('identification', 'N/A')}")
        
        # Obtener productos para usar códigos reales
        print("\n📦 Obteniendo lista de productos...")
        products = siigo.get_products()
        if products:
            print(f"Encontrados {len(products)} productos")
            # Mostrar los primeros 3 productos como ejemplo
            for i, product in enumerate(products[:3]):
                print(f"  {i+1}. {product.get('name', 'N/A')} - Código: {product.get('code', 'N/A')}")

if __name__ == "__main__":
    # Ejecutar función principal
    main()
    
    # Descomentar la siguiente línea para ver ejemplo con datos reales
    # example_with_real_data()
