import { Command } from 'commander';
import { createInvoices } from './createInvoices';

const program = new Command();

program
  .name('siigo-invoice-cli')
  .description('CLI tool to create Siigo invoices from Excel files')
  .version('1.0.0')
  .option('-u, --username <username>', 'Siigo username')
  .option('-k, --access-key <key>', 'Siigo access key')
  .option('-p, --partner-id <id>', 'Siigo partner ID')
  .option('-f, --file-path <path>', 'Path to Excel file')
  .parse();

const options = program.opts();

async function main() {
  console.log('🚀 Siigo Invoice CLI - Starting invoice creation process...');
  await createInvoices(options);
}

main().catch(error => {
  console.error('❌ CLI Error:', error);
  process.exit(1);
});