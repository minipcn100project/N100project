/**
 * Rarible Auto-Listing Script
 * Automatically list NFTs on Rarible (shows on OpenSea, LooksRare, X2Y2 too!)
 */

require('dotenv').config();
const { createRaribleSdk } = require("@rarible/sdk");
const { EthereumWallet } = require("@rarible/sdk-wallet");
const { ethers } = require("ethers");
const { toAddress, toBigNumber, toItemId } = require("@rarible/types");

// Configuration
const CONFIG = {
    CONTRACT_ADDRESS: "0xf5420c3E42bb575a2c15434278655c837ca3783E",
    POLYGON_RPC: process.env.POLYGON_RPC_URL || "https://polygon-rpc.com/",
    PRIVATE_KEY: process.env.PRIVATE_KEY,
    RARIBLE_API_KEY: process.env.RARIBLE_API_KEY,
    NFT_PRICE_USD: parseFloat(process.env.NFT_PRICE || "10"),
    MATIC_USD_PRICE: 0.90, // Update if needed
};

/**
 * Initialize Rarible SDK
 */
async function initializeRarible() {
    console.log("======================================================================");
    console.log("RARIBLE AUTO-LISTING SCRIPT");
    console.log("======================================================================");
    console.log();

    // Create provider
    const provider = new ethers.providers.JsonRpcProvider(CONFIG.POLYGON_RPC);

    // Create wallet
    const wallet = new ethers.Wallet(CONFIG.PRIVATE_KEY, provider);
    console.log(`[INFO] Wallet: ${wallet.address}`);

    // Create Ethereum Wallet for Rarible
    const ethereumWallet = new EthereumWallet(wallet);

    // Initialize Rarible SDK
    const sdk = createRaribleSdk(ethereumWallet, "polygon", {
        apiKey: CONFIG.RARIBLE_API_KEY
    });

    console.log("[OK] Rarible SDK initialized");
    console.log();

    return { sdk, wallet };
}

/**
 * List NFT on Rarible
 * @param {object} sdk - Rarible SDK instance
 * @param {number} tokenId - NFT Token ID
 * @param {number} priceUSD - Price in USD
 */
async function listNFT(sdk, tokenId, priceUSD = CONFIG.NFT_PRICE_USD) {
    try {
        console.log("======================================================================");
        console.log(`LISTING NFT #${tokenId} ON RARIBLE`);
        console.log("======================================================================");
        console.log();

        // Calculate price in MATIC
        const priceMAT IC = priceUSD / CONFIG.MATIC_USD_PRICE;
        const priceWei = ethers.utils.parseEther(priceMAT IC.toFixed(6)).toString();

        console.log(`[INFO] Price: $${priceUSD} USD`);
        console.log(`[INFO] Price: ${priceMAT IC.toFixed(4)} MATIC`);
        console.log(`[INFO] Token ID: ${tokenId}`);
        console.log();

        // Create item ID
        const itemId = toItemId(`POLYGON:${CONFIG.CONTRACT_ADDRESS}:${tokenId}`);
        console.log(`[INFO] Item ID: ${itemId}`);

        // Prepare sell order
        console.log("[1/3] Preparing sell order...");

        const sellRequest = {
            itemId: itemId,
            amount: 1,
            price: priceWei,
            currency: toAddress("POLYGON:0x0000000000000000000000000000000000001010"), // MATIC
            expirationDate: undefined, // No expiration
        };

        // Execute listing
        console.log("[2/3] Sending listing transaction...");
        const listingResult = await sdk.order.sell(sellRequest);

        console.log("[3/3] Listing successful!");
        console.log();

        console.log("======================================================================");
        console.log("SUCCESS! NFT LISTED ON MULTIPLE MARKETPLACES");
        console.log("======================================================================");
        console.log();
        console.log(`Token ID: ${tokenId}`);
        console.log(`Price: $${priceUSD} USD (${priceMAT IC.toFixed(4)} MATIC)`);
        console.log();
        console.log("Marketplace Links:");
        console.log(`Rarible:   https://rarible.com/token/polygon/${CONFIG.CONTRACT_ADDRESS}:${tokenId}`);
        console.log(`OpenSea:   https://opensea.io/assets/matic/${CONFIG.CONTRACT_ADDRESS}/${tokenId}`);
        console.log(`LooksRare: https://looksrare.org/collections/${CONFIG.CONTRACT_ADDRESS}/${tokenId}`);
        console.log();
        console.log("Note: May take 5-10 minutes to appear on OpenSea");
        console.log("======================================================================");
        console.log();

        return {
            success: true,
            tokenId,
            priceUSD,
            priceMAT IC,
            raribleUrl: `https://rarible.com/token/polygon/${CONFIG.CONTRACT_ADDRESS}:${tokenId}`,
            openseaUrl: `https://opensea.io/assets/matic/${CONFIG.CONTRACT_ADDRESS}/${tokenId}`,
        };

    } catch (error) {
        console.error();
        console.error("======================================================================");
        console.error("ERROR: LISTING FAILED");
        console.error("======================================================================");
        console.error(`Token ID: ${tokenId}`);
        console.error(`Error: ${error.message}`);
        console.error();

        if (error.message.includes("already listed")) {
            console.error("This NFT may already be listed. Check Rarible:");
            console.error(`https://rarible.com/token/polygon/${CONFIG.CONTRACT_ADDRESS}:${tokenId}`);
        } else if (error.message.includes("not approved")) {
            console.error("NFT contract may need to approve Rarible Exchange.");
            console.error("Run: setApprovalForAll(Rarible Exchange Address, true)");
        }

        console.error("======================================================================");
        console.error();

        return {
            success: false,
            tokenId,
            error: error.message
        };
    }
}

/**
 * Check if NFT is already listed
 */
async function checkListing(sdk, tokenId) {
    try {
        const itemId = toItemId(`POLYGON:${CONFIG.CONTRACT_ADDRESS}:${tokenId}`);
        const orders = await sdk.apis.order.getSellOrdersByItem({ itemId });

        if (orders.orders && orders.orders.length > 0) {
            console.log(`[INFO] NFT #${tokenId} is already listed`);
            return true;
        }
        return false;
    } catch (error) {
        console.log(`[INFO] NFT #${tokenId} not yet listed`);
        return false;
    }
}

/**
 * Batch list multiple NFTs
 */
async function batchList(sdk, tokenIds, priceUSD = CONFIG.NFT_PRICE_USD) {
    console.log("======================================================================");
    console.log(`BATCH LISTING ${tokenIds.length} NFTs`);
    console.log("======================================================================");
    console.log();

    const results = [];

    for (const tokenId of tokenIds) {
        // Check if already listed
        const isListed = await checkListing(sdk, tokenId);

        if (isListed) {
            console.log(`[SKIP] NFT #${tokenId} already listed`);
            results.push({ tokenId, skipped: true });
            continue;
        }

        // List NFT
        const result = await listNFT(sdk, tokenId, priceUSD);
        results.push(result);

        // Wait 3 seconds between listings
        if (tokenId !== tokenIds[tokenIds.length - 1]) {
            console.log("[INFO] Waiting 3 seconds before next listing...");
            await new Promise(resolve => setTimeout(resolve, 3000));
        }
    }

    console.log();
    console.log("======================================================================");
    console.log("BATCH LISTING COMPLETE");
    console.log("======================================================================");
    console.log(`Total: ${tokenIds.length}`);
    console.log(`Listed: ${results.filter(r => r.success).length}`);
    console.log(`Skipped: ${results.filter(r => r.skipped).length}`);
    console.log(`Failed: ${results.filter(r => !r.success && !r.skipped).length}`);
    console.log("======================================================================");

    return results;
}

/**
 * Main function
 */
async function main() {
    // Get command line arguments
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log();
        console.log("======================================================================");
        console.log("RARIBLE AUTO-LISTING SCRIPT");
        console.log("======================================================================");
        console.log();
        console.log("Usage:");
        console.log("  node rarible_auto_list.js <tokenId>           - List single NFT");
        console.log("  node rarible_auto_list.js <tokenId> <price>   - List with custom price");
        console.log("  node rarible_auto_list.js 1,2,3               - Batch list NFTs");
        console.log("  node rarible_auto_list.js all                 - List all unminted NFTs");
        console.log();
        console.log("Examples:");
        console.log("  node rarible_auto_list.js 1");
        console.log("  node rarible_auto_list.js 1 15");
        console.log("  node rarible_auto_list.js 1,2,3,4,5");
        console.log();
        console.log("======================================================================");
        process.exit(0);
    }

    // Initialize SDK
    const { sdk } = await initializeRarible();

    const [tokenArg, priceArg] = args;
    const priceUSD = priceArg ? parseFloat(priceArg) : CONFIG.NFT_PRICE_USD;

    // Single token
    if (!tokenArg.includes(',') && tokenArg !== 'all') {
        const tokenId = parseInt(tokenArg);
        await listNFT(sdk, tokenId, priceUSD);
    }
    // Batch tokens
    else if (tokenArg.includes(',')) {
        const tokenIds = tokenArg.split(',').map(id => parseInt(id.trim()));
        await batchList(sdk, tokenIds, priceUSD);
    }
    // All tokens (read from counter)
    else if (tokenArg === 'all') {
        const fs = require('fs');
        const path = require('path');

        try {
            const counterPath = path.join(__dirname, '..', 'nft_counter.txt');
            const totalNFTs = parseInt(fs.readFileSync(counterPath, 'utf8').trim());

            // List all from 0 to totalNFTs-1 (or 1 to totalNFTs depending on your indexing)
            const tokenIds = Array.from({ length: totalNFTs }, (_, i) => i + 1); // Token IDs start from 1
            await batchList(sdk, tokenIds, priceUSD);
        } catch (error) {
            console.error(`[ERROR] Could not read nft_counter.txt: ${error.message}`);
        }
    }
}

// Run if called directly
if (require.main === module) {
    main().catch(error => {
        console.error("Fatal error:", error);
        process.exit(1);
    });
}

module.exports = { listNFT, batchList, checkListing };
