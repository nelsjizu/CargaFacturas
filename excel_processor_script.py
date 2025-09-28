import pandas as pd
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class ExcelProcessor:
    def __init__(self, excel_file_path: str):
        self.excel_file_path = excel_file_path
        self.dataframe = None
        self.columns = []
        self.total_rows = 0
        self.current_row = 0
        
    def load_excel(self) -> bool:
        try:
            print(f"📊 Cargando archivo: {self.excel_file_path}")
            self.dataframe = pd.read_excel(self.excel_file_path)
            self.columns = list(self.dataframe.columns)
            self.total_rows = len(self.dataframe)
            
            print(f"✅ Archivo cargado exitosamente")
            print(f"📋 Columnas encontradas ({len(self.columns)}): {self.columns}")
            print(f"📄 Total de registros: {self.total_rows}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo {self.excel_file_path}")
            return False
        except Exception as e:
            print(f"❌ Error cargando Excel: {e}")
            return False
    
    def get_column_info(self) -> Dict[str, Any]:
        if self.dataframe is None:
            return {}
        
        column_info = {}
        
        for column in self.columns:
            column_data = self.dataframe[column]
            
            column_info[column] = {
                'type': str(column_data.dtype),
                'non_null_count': column_data.count(),
                'null_count': column_data.isnull().sum(),
                'unique_values': column_data.nunique(),
                'sample_values': column_data.dropna().head(3).tolist()
            }
        
        return column_info
    
    def show_column_analysis(self):
        if self.dataframe is None:
            print("❌ No hay datos cargados")
            return
        
        column_info = self.get_column_info()
        
        for i, (column, info) in enumerate(column_info.items(), 1):
            print(f"\n{i}. Columna: '{column}'")
            print(f"   Tipo: {info['type']}")
            print(f"   Registros con datos: {info['non_null_count']}")
            print(f"   Registros vacíos: {info['null_count']}")
            print(f"   Valores únicos: {info['unique_values']}")
            print(f"   Ejemplos: {info['sample_values']}")
    
    def get_record(self, index: int) -> Optional[Dict[str, Any]]:
        if self.dataframe is None:
            return None
        
        if index < 0 or index >= self.total_rows:
            return None
        
        row_series = self.dataframe.iloc[index]
        record = {}
        for column in self.columns:
            value = row_series[column]
            if pd.isna(value):
                record[column] = None
            else:
                record[column] = value
        
        return record
    
    def process_all_records(self, process_function):
        if self.dataframe is None:
            print("❌ No hay datos cargados")
            return
        
        print(f"\n🔄 Iniciando procesamiento de {self.total_rows} registros...")
        
        results = []
        successful_count = 0
        failed_count = 0
        
        for index in range(self.total_rows):
            self.current_row = index + 1
            
            print(f"\n📄 Procesando registro {self.current_row}/{self.total_rows}")
            record = self.get_record(index)
            
            if record is None:
                print(f"   ❌ Error obteniendo registro {index}")
                failed_count += 1
                continue
            
            try:
                result = process_function(index, record)
                
                if result and result.get('success', False):
                    successful_count += 1
                    print(f"   ✅ Procesado exitosamente")
                else:
                    failed_count += 1
                    error_msg = result.get('error', 'Error desconocido') if result else 'Sin resultado'
                    print(f"   ❌ Error: {error_msg}")
                
                results.append({
                    'index': index,
                    'row_number': self.current_row,
                    'result': result,
                    'record_sample': {k: v for k, v in list(record.items())[:3]}  # Muestra de los primeros 3 campos
                })
                
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Excepción: {str(e)}")
                results.append({
                    'index': index,
                    'row_number': self.current_row,
                    'result': {'success': False, 'error': str(e)},
                    'record_sample': {k: v for k, v in list(record.items())[:3]}
                })
        
        print("\n" + "="*60)
        print("RESUMEN DE PROCESAMIENTO")
        print("="*60)
        print(f"✅ Registros procesados exitosamente: {successful_count}")
        print(f"❌ Registros con errores: {failed_count}")
        print(f"📊 Total procesados: {self.total_rows}")
        
        return results
    
    def export_records_to_json(self, output_file: str = None):
        if self.dataframe is None:
            print("❌ No hay datos cargados")
            return
        
        if output_file is None:
            base_name = os.path.splitext(self.excel_file_path)[0]
            output_file = f"{base_name}_export.json"
        
        try:
            records = []
            for index in range(self.total_rows):
                record = self.get_record(index)
                if record:
                    records.append({
                        'row_number': index + 1,
                        'data': record
                    })
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"📁 Registros exportados a: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exportando a JSON: {e}")

def example_process_function(index: int, record: Dict[str, Any]) -> Dict[str, Any]:
    try:
        required_fields = []
        
        missing_fields = [field for field in required_fields if not record.get(field)]
        
        if missing_fields:
            return {
                'success': False,
                'error': f'Faltan campos obligatorios: {missing_fields}'
            }
        
        processed_data = {}
        for key, value in record.items():
            if value is not None:
                if isinstance(value, str):
                    processed_data[key] = value.strip()
                else:
                    processed_data[key] = value
        
        return {
            'success': True,
            'processed_fields': len(processed_data),
            'processed_data': processed_data
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    excel_file = 'facturas_ejemplo.xlsx'
    processor = ExcelProcessor(excel_file)
    
    if not processor.load_excel():
        return
    
    processor.show_column_analysis()   
    
    first_record = processor.get_record(0)
    print ("CUFE Primer Registro !!!")
    print ({processor.get_record(0).get('CUFE/CUDE')})
    if first_record:
        print("📄 Primer registro:")
        for key, value in first_record.items():
            print(f"   {key}: {value}")
    
    last_record = processor.get_record(processor.total_rows - 1)
    print ("CUFE Ultimo Registro !!!")
    print ({processor.get_record(processor.total_rows - 1).get('CUFE/CUDE')})
    if last_record:
        print(f"\n📄 Último registro (fila {processor.total_rows}):")
        for key, value in last_record.items():
            print(f"   {key}: {value}")
        
    processor.export_records_to_json()

def custom_processing_example():    
    excel_file = 'datos_ejemplo.xlsx'
    processor = ExcelProcessor(excel_file)
    
    if processor.load_excel():
        # Función personalizada para procesar empleados
        def process_employee(index: int, record: Dict[str, Any]) -> Dict[str, Any]:
            try:
                nombre = record.get('Nombre', '')
                salario = record.get('Salario', 0)
                activo = record.get('Activo', False)
                
                # Calcular bonificación
                bonificacion = salario * 0.1 if activo else 0
                
                # Clasificar por salario
                if salario >= 6000000:
                    categoria = 'Alto'
                elif salario >= 5000000:
                    categoria = 'Medio'
                else:
                    categoria = 'Básico'
                
                return {
                    'success': True,
                    'nombre': nombre,
                    'salario_original': salario,
                    'bonificacion': bonificacion,
                    'salario_total': salario + bonificacion,
                    'categoria': categoria,
                    'activo': activo
                }
                
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        
        # Procesar con función personalizada
        results = processor.process_all_records(process_employee)
        
        # Mostrar resultados exitosos
        print("\n📊 RESULTADOS DEL PROCESAMIENTO:")
        for result in results:
            if result['result'].get('success', False):
                data = result['result']
                print(f"   👤 {data['nombre']}: ${data['salario_total']:,} ({data['categoria']})")

if __name__ == "__main__":
    # Ejecutar ejemplo principal
    main()
    
    # Descomentar para ver ejemplo personalizado
    # custom_processing_example()
