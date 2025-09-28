import ExcelImporter from './siigo-api/excelImporter';
import { mapExcelDataToInvoices, validatePurchaseInvoice } from './siigo-api/invoiceMapper';
import ApiRequester from './siigo-api/apiRequester';
import prompts from 'prompts';

export async function createInvoices(options: any = {}) {
  try {
    // Step 1: Get credentials from env vars, flags, or prompts
    const username = options.username || process.env.SIIGO_USERNAME;
    const accessKey = options.accessKey || process.env.SIIGO_ACCESS_KEY;
    const partnerId = options.partnerId || process.env.SIIGO_PARTNER_ID;
    const filePath = options.filePath || process.env.EXCEL_FILE_PATH;

    let credentials: any = {};

    if (username && accessKey && partnerId && filePath) {
      credentials = { username, accessKey, partnerId, filePath };
    } else {
      const promptsNeeded: any[] = [];
      if (!username) promptsNeeded.push({
        type: 'text',
        name: 'username',
        message: 'Enter your Siigo username:',
        validate: (value: string) => value ? true : 'Username is required',
      });
      if (!accessKey) promptsNeeded.push({
        type: 'password',
        name: 'accessKey',
        message: 'Enter your Siigo access key:',
        validate: (value: string) => value ? true : 'Access key is required',
      });
      if (!partnerId) promptsNeeded.push({
        type: 'text',
        name: 'partnerId',
        message: 'Enter your Siigo partner ID:',
        validate: (value: string) => value ? true : 'Partner ID is required',
      });
      if (!filePath) promptsNeeded.push({
        type: 'text',
        name: 'filePath',
        message: 'Enter the path to your Excel file:',
        validate: (value: string) => value ? true : 'File path is required',
      });

      const prompted = await prompts(promptsNeeded);
      credentials = { username, accessKey, partnerId, filePath, ...prompted };
    }

    const siigoConfig = {
      baseURL: 'https://api.siigo.com',
      apiBaseURL: 'https://api.siigo.com/v1',
      username: credentials.username,
      accessKey: credentials.accessKey,
      partnerId: credentials.partnerId,
    };

    // Step 2: Import Excel data
    const importer = new ExcelImporter(credentials.filePath);
    const excelData = await importer.importData();
    console.log(`Imported ${excelData.length} rows from Excel.`);

    // Step 2: Map and validate invoices
    const invoices = mapExcelDataToInvoices(excelData);
    const validInvoices: any[] = [];
    const invalidInvoices: any[] = [];

    for (let i = 0; i < invoices.length; i++) {
      try {
        const validated = validatePurchaseInvoice(invoices[i]);
        validInvoices.push({ index: i + 1, data: validated });
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.log(`❌ Validation failed for row ${i + 1}: ${errorMessage}`);
        invalidInvoices.push({ index: i + 1, error: errorMessage });
      }
    }

    console.log(`Valid invoices: ${validInvoices.length}`);
    console.log(`Invalid invoices: ${invalidInvoices.length}`);

    if (invalidInvoices.length > 0) {
      console.log('Invalid invoices:');
      invalidInvoices.forEach(inv => console.log(`Row ${inv.index}: ${inv.error}`));
    }

    if (validInvoices.length === 0) {
      console.log('No valid invoices to create.');
      return;
    }

    // Step 3: Prompt user for number of invoices to create
    const response = await prompts({
      type: 'number',
      name: 'count',
      message: `How many invoices do you want to create? (1-${validInvoices.length})`,
      validate: value => value > 0 && value <= validInvoices.length ? true : `Please enter a number between 1 and ${validInvoices.length}`,
    });

    const count = response.count;
    if (!count) {
      console.log('No number selected. Exiting.');
      return;
    }

    // Step 4: Initialize API requester and authenticate
    const apiRequester = new ApiRequester(siigoConfig);
    await apiRequester.authenticate();

    // Step 5: Create selected invoices
    const selectedInvoices = validInvoices.slice(0, count);
    console.log(`Creating ${count} invoices...`);

    for (const inv of selectedInvoices) {
      console.log(JSON.stringify(inv, null, 2))
      try {
        const result = await apiRequester.createPurchaseInvoice(inv.data);
        console.log(`✅ Created invoice for row ${inv.index}: ${JSON.stringify(result)}`);
      } catch (error) {
        console.error(error)
        console.error(`❌ Failed to create invoice for row ${inv.index}: ${error instanceof Error ? error.message : String(error)}`);
      }
    }

    console.log('Process completed.');

  } catch (error) {
    console.error('Error:', error instanceof Error ? error.message : String(error));
  }
}

