import * as XLSX from 'xlsx';

type ExcelData = Record<string, any>;

class ExcelImporter {
  private filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  async importData(): Promise<Record<string, any>[]> {
    try {
      const workbook = XLSX.readFile(this.filePath);
      const sheetName = workbook.SheetNames[0];
      // @ts-ignore
      const worksheet = workbook.Sheets?.[sheetName];
      if (!worksheet) {
        throw new Error(`Sheet ${sheetName} not found`);
      }
      return XLSX.utils.sheet_to_json(worksheet as any);
    } catch (error) {
      throw new Error(`Failed to import Excel data: ${error}`);
    }
  }

  async importDataFromBuffer(buffer: ArrayBuffer): Promise<Record<string, any>[]> {
    try {
      const workbook = XLSX.read(buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      // @ts-ignore
      const worksheet = workbook.Sheets?.[sheetName];
      if (!worksheet) {
        throw new Error(`Sheet ${sheetName} not found`);
      }
      return XLSX.utils.sheet_to_json(worksheet as any);
    } catch (error) {
      throw new Error(`Failed to import Excel data from buffer: ${error}`);
    }
  }
}

export default ExcelImporter;