import { z } from 'zod';

// Define the schema for the invoice body based on the provided JSON schema
export const PurchaseInvoiceSchema = z.object({
  document: z.object({
    id: z.number(),
  }),
  date: z.string(),
  supplier: z.object({
    identification: z.string(),
    branch_office: z.number().optional(),
  }),
  cost_center: z.number(),
  provider_invoice: z.object({
    prefix: z.string(),
    number: z.string(),
  }),
  currency: z.object({
    code: z.string(),
    exchange_rate: z.number(),
  }).optional(),
  observations: z.string().optional(),
  discount_type: z.string().optional(),
  supplier_by_item: z.boolean().optional(),
  tax_included: z.boolean().optional(),
  items: z.array(z.any()), // Assuming items can be any for now; can be refined later
  payments: z.array(z.any()), // Assuming payments can be any for now; can be refined later
});

// Infer the TypeScript type from the Zod schema
export type PurchaseInvoice = z.infer<typeof PurchaseInvoiceSchema>;

// Validation function
export function validatePurchaseInvoice(data: unknown): PurchaseInvoice {
  return PurchaseInvoiceSchema.parse(data);
}
