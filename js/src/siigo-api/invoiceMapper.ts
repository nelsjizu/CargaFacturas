import type { PurchaseInvoice } from './invoiceTypes';
import { validatePurchaseInvoice } from './invoiceTypes';


const ID_TIPO_COMPROBANTE = 5341;
const MOCK_PRODUCT = "PROD0001";
const COST_CENTER = 286


// Mapping function to transform Excel row data to PurchaseInvoice based on the actual Excel structure
export function mapExcelRowToInvoice(excelRow: Record<string, any>): PurchaseInvoice {
  return {
    document: {
      id: ID_TIPO_COMPROBANTE,
    },
    // date: excelRow["Fecha Emisión"],
    date: "2025-11-17",
    supplier: {
      identification: excelRow["NIT Emisor"],
      // branch_office might not be directly available; set to undefined or derive if possible
    },
    cost_center: COST_CENTER, // Not directly available; set based on your business logic
    provider_invoice: {
      prefix: excelRow["Prefijo"] || "NA",
      number: excelRow["Folio"],
    },
    observations: `CUFE: ${excelRow["CUFE/CUDE"]}`, // Using CUFE as observations
    items: buildItems(excelRow), // Construct items from tax and total fields
    payments: buildPayments(excelRow), // Construct payments from payment method fields
  };
}

// Helper function to build items array (simplified; adjust based on actual item structure)
function buildItems(excelRow: Record<string, any>): any[] {
  return [{
    type: "Product",
    code: MOCK_PRODUCT, // Placeholder; replace with actual item code
    quantity: 1,
    price: excelRow[" Total "],
    discount: 0,
    taxes: [
      { id: 2866, name: "IVA", percent: 19, base: (excelRow[" Total "] - excelRow[" IVA "]), value: excelRow[" IVA "] }, // Assuming 19% IVA
    ],
  }];
}

// Helper function to build payments array
function buildPayments(excelRow: Record<string, any>): any[] {
  return [{
    id: 1225, // Payment method ID
    value: excelRow[" Total "],
    // due_date: excelRow["Fecha Emisión"],
    due_date: "2025-11-17",
    // Add other payment details if available
  }];
}

// Function to map an array of Excel rows to an array of PurchaseInvoices
export function mapExcelDataToInvoices(excelData: Record<string, any>[]): PurchaseInvoice[] {
  return excelData.map(mapExcelRowToInvoice);
}

// Export the validation function
export { validatePurchaseInvoice };
