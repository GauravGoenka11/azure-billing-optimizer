Azure Billing Cost Optimizer

## Overview
This project provides a serverless solution to reduce costs in a read-heavy Azure Cosmos DB billing system by archiving older data to Blob Storage.

## Features
- Scheduled archival of old records
- Seamless fallback access
- No changes to existing API contracts

## Setup
1. Set up Cosmos DB and Blob Storage
2. Deploy Azure Functions using VS Code or Azure CLI
3. Schedule the Archiver function (Timer Trigger)

## Deployment Script
Run `scripts/setup_blob.sh` to create the archive blob container:

```bash
az storage container create --name billing-archive --account-name <account-name> --au
