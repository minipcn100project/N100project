# Solana NFT Minting Guide

Complete guide for minting NFTs on Solana blockchain (Devnet and Mainnet)

## Quick Start

### 1. Generate Wallet

Create a new Solana wallet for NFT minting:

```batch
generate_wallet.bat
```

Or manually:
```bash
python scripts/wallet_generator.py
```

This creates `wallet.json` containing your private key. **KEEP THIS FILE SECURE!**

### 2. Fund Your Wallet

#### For Devnet (Testing):
```bash
# Visit Solana Faucet
https://faucet.solana.com/

# Or use CLI (if installed)
solana airdrop 2 YOUR_WALLET_ADDRESS --url devnet
```

Request 1-2 SOL for testing purposes.

#### For Mainnet (Real NFTs):
Transfer real SOL to your wallet address. You'll need:
- ~0.01 SOL per NFT mint (transaction fees)
- Additional SOL for account rent (~0.001 SOL)

### 3. Configure Environment

Update `.env` file:

```env
# Solana Configuration
SOLANA_WALLET_PATH=./wallet.json
SOLANA_RPC_URL=https://api.devnet.solana.com
SOLANA_RPC_URL_MAINNET=https://api.mainnet-beta.solana.com
SOLANA_WALLET_ADDRESS=YOUR_WALLET_PUBLIC_KEY_HERE

# Network: devnet or mainnet-beta
SOLANA_NETWORK=devnet

# NFT Configuration
NFT_PRICE_SOL=0.5
NFT_COLLECTION_NAME=N100 Collection
NFT_SYMBOL=N100
NFT_ROYALTY_PERCENT=5
```

### 4. Test Minting on Devnet

```bash
# Test single NFT mint
python scripts/solana_real_minter.py

# Test with mainnet configuration (doesn't actually mint)
python scripts/solana_real_minter.py --mainnet
```

## Current Implementation Status

### What's Working Now:

1. **Wallet Generation** - Creates Solana-compatible keypair
2. **Balance Checking** - Verifies SOL balance before minting
3. **Metadata Creation** - Generates Metaplex-standard NFT metadata
4. **GitHub Pages Integration** - NFT gallery already deployed

### What Requires Additional Setup:

**Full On-Chain Minting** requires:
1. Image upload to Arweave or IPFS
2. Metadata upload to Arweave or IPFS
3. Metaplex SDK integration for NFT creation
4. SPL Token account creation

## Minting Options

### Option 1: Metadata-Only (Current Setup)

**Pros:**
- Free (no blockchain fees)
- Fast deployment
- Works immediately with GitHub Pages
- Great for showcasing AI art

**Cons:**
- Not real blockchain NFTs
- No marketplace integration
- No on-chain proof of ownership

**Best for:** Testing, portfolios, art galleries

### Option 2: Lazy Minting (Recommended)

**Pros:**
- No upfront minting cost
- Buyer pays gas fees at purchase
- Uses Metaplex Candy Machine
- Marketplace compatible

**Cons:**
- Requires Candy Machine setup
- Needs image hosting (Arweave/IPFS)
- More complex initial setup

**Best for:** NFT drops, collections, sales

### Option 3: Direct Minting (Full On-Chain)

**Pros:**
- Immediate blockchain proof
- Full marketplace support
- Complete ownership control
- No intermediary required

**Cons:**
- Costs ~0.01 SOL per NFT
- Requires upfront payment
- More transaction overhead

**Best for:** High-value NFTs, instant availability

## Network Comparison

| Feature | Devnet | Mainnet |
|---------|--------|---------|
| Purpose | Testing | Production |
| SOL Value | Free (faucet) | Real money |
| Speed | Fast | Fast |
| Cost | Free | ~$0.01-0.10/NFT |
| Permanence | May reset | Permanent |
| Marketplaces | None | Magic Eden, etc. |

## Step-by-Step: Devnet to Mainnet

### Phase 1: Devnet Testing

1. Generate wallet
2. Get devnet SOL from faucet
3. Mint test NFTs
4. Verify on Solana Explorer (devnet)
5. Test all automation workflows

### Phase 2: Mainnet Preparation

1. Review all code and configurations
2. Backup wallet securely
3. Fund mainnet wallet with real SOL
4. Test with small amount first
5. Update `.env` to `SOLANA_NETWORK=mainnet-beta`

### Phase 3: Production Deployment

1. Run full automation test on devnet
2. Switch to mainnet configuration
3. Mint first NFT
4. Verify on Solana Explorer (mainnet)
5. Enable hourly automation

## Architecture

Current minting flow:
```
ComfyUI (Generate Image)
    |
    v
Llama (Generate Title/Description)
    |
    v
solana_real_minter.py (Create Metadata + Blockchain)
    |
    v
GitHub Pages (Update Gallery)
    |
    v
Twitter (Auto-Post)
```

## Costs Breakdown

### Devnet (Testing):
- Wallet creation: FREE
- SOL from faucet: FREE
- Minting: FREE
- Total: **$0**

### Mainnet (Production):

**Initial Setup:**
- Wallet creation: FREE
- Initial SOL purchase: $20-50 recommended

**Per NFT:**
- Transaction fee: ~0.000005 SOL (~$0.001)
- Account rent: ~0.00089 SOL (~$0.18)
- Total per NFT: ~**$0.20**

**Monthly (24 NFTs at 1/hour):**
- 24 NFTs × $0.20 = **$4.80/month**

**Yearly:**
- 8760 NFTs × $0.20 = **~$1,750/year**

## Tools and Resources

### Wallets:
- Phantom: https://phantom.app/
- Solflare: https://solflare.com/
- Backpack: https://backpack.app/

### Explorers:
- Devnet: https://explorer.solana.com/?cluster=devnet
- Mainnet: https://explorer.solana.com/

### Faucets (Devnet):
- https://faucet.solana.com/
- https://solfaucet.com/

### Marketplaces (Mainnet):
- Magic Eden: https://magiceden.io/
- OpenSea (Solana): https://opensea.io/
- Tensor: https://tensor.trade/

### Development:
- Solana Docs: https://docs.solana.com/
- Metaplex Docs: https://docs.metaplex.com/
- Python SDK: https://michaelhly.github.io/solana-py/

## Troubleshooting

### "Wallet file not found"
```bash
python scripts/wallet_generator.py
```

### "Insufficient SOL balance"
- Devnet: Request airdrop from faucet
- Mainnet: Transfer SOL to wallet

### "RPC connection failed"
Check `.env` RPC URLs:
- Devnet: `https://api.devnet.solana.com`
- Mainnet: `https://api.mainnet-beta.solana.com`

### "Transaction failed"
- Check SOL balance
- Verify network (devnet vs mainnet)
- Try again (network congestion)

## Security Best Practices

1. **NEVER share wallet.json file**
2. **NEVER commit wallet.json to git** (already in .gitignore)
3. **Backup wallet.json securely** (encrypted USB, password manager)
4. **Use devnet for testing** (always test before mainnet)
5. **Start with small amounts** on mainnet
6. **Monitor wallet balance** regularly
7. **Use separate wallets** for testing vs production

## Next Steps

### For Testing (Devnet):
1. Run `generate_wallet.bat`
2. Get devnet SOL from faucet
3. Run `python scripts/solana_real_minter.py`
4. Verify on Solana Explorer

### For Production (Mainnet):
1. Generate production wallet
2. Backup wallet securely
3. Fund with real SOL
4. Update `.env` to mainnet
5. Test single mint first
6. Enable automation

## Support

For issues or questions:
- Solana Discord: https://discord.com/invite/solana
- Metaplex Discord: https://discord.com/invite/metaplex
- GitHub Issues: https://github.com/minipcn100project/N100project/issues

---

Generated with Claude Code
