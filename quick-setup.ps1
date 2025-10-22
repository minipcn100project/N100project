# N100 NFT Automation - Quick Setup Script
# 이 스크립트를 PowerShell 관리자 권한으로 실행하세요

Write-Host "🚀 N100 NFT Automation Quick Setup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"
$projectPath = "C:\Users\autop\project\nft-automation-project"

# 1. Ollama 설치 확인 및 설치
Write-Host "1️⃣ Checking Ollama..." -ForegroundColor Yellow
$ollamaPath = "C:\Users\autop\AppData\Local\Programs\Ollama\ollama.exe"
if (Test-Path $ollamaPath) {
    Write-Host "   ✅ Ollama already installed" -ForegroundColor Green
} else {
    Write-Host "   📥 Installing Ollama..." -ForegroundColor Yellow
    $installerPath = "C:\Users\autop\Downloads\OllamaSetup.exe"
    if (Test-Path $installerPath) {
        Start-Process -FilePath $installerPath -Args "/S" -Wait
        Write-Host "   ✅ Ollama installed" -ForegroundColor Green
    } else {
        Write-Host "   ❌ OllamaSetup.exe not found in Downloads" -ForegroundColor Red
        Write-Host "   Please download from: https://ollama.com/download" -ForegroundColor Yellow
    }
}

# 2. Ollama 실행 확인
Write-Host ""
Write-Host "2️⃣ Starting Ollama service..." -ForegroundColor Yellow
$ollamaProcess = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if ($null -eq $ollamaProcess) {
    if (Test-Path $ollamaPath) {
        Start-Process -FilePath $ollamaPath -Args "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3
        Write-Host "   ✅ Ollama service started" -ForegroundColor Green
    }
} else {
    Write-Host "   ✅ Ollama service already running" -ForegroundColor Green
}

# 3. Llama 모델 다운로드
Write-Host ""
Write-Host "3️⃣ Downloading Llama 3.2 3B model..." -ForegroundColor Yellow
if (Test-Path $ollamaPath) {
    $env:Path = "C:\Users\autop\AppData\Local\Programs\Ollama;" + $env:Path
    $modelCheck = & $ollamaPath list 2>&1 | Select-String "llama3.2:3b"
    if ($modelCheck) {
        Write-Host "   ✅ Llama 3.2 3B already downloaded" -ForegroundColor Green
    } else {
        Write-Host "   📥 Downloading model (this may take 5-10 minutes)..." -ForegroundColor Yellow
        & $ollamaPath pull llama3.2:3b
        Write-Host "   ✅ Llama 3.2 3B downloaded" -ForegroundColor Green
    }
}

# 4. Python 설치 확인
Write-Host ""
Write-Host "4️⃣ Checking Python..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if ($null -eq $pythonCmd) {
    Write-Host "   📥 Installing Python..." -ForegroundColor Yellow
    $pythonInstaller = "C:\Users\autop\Downloads\python-installer.exe"
    if (Test-Path $pythonInstaller) {
        Start-Process -FilePath $pythonInstaller -Args "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait
        Write-Host "   ✅ Python installed - Please restart PowerShell and run this script again" -ForegroundColor Green
        Write-Host "   ⚠️  Close this window and open a NEW PowerShell window" -ForegroundColor Yellow
        exit
    } else {
        Write-Host "   ❌ python-installer.exe not found in Downloads" -ForegroundColor Red
        Write-Host "   Please download from: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit
    }
} else {
    $pythonVersion = & python --version 2>&1
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
}

# 5. Python 패키지 설치
Write-Host ""
Write-Host "5️⃣ Installing Python packages..." -ForegroundColor Yellow
Set-Location $projectPath
& python -m pip install --upgrade pip --quiet
& pip install -r requirements.txt --quiet
Write-Host "   ✅ Python packages installed" -ForegroundColor Green

# 6. Playwright 브라우저 설치
Write-Host ""
Write-Host "6️⃣ Installing Playwright browser..." -ForegroundColor Yellow
& playwright install chromium
Write-Host "   ✅ Playwright chromium installed" -ForegroundColor Green

# 7. Solana CLI 다운로드 및 설치
Write-Host ""
Write-Host "7️⃣ Installing Solana CLI..." -ForegroundColor Yellow
$solanaCmd = Get-Command solana -ErrorAction SilentlyContinue
if ($null -eq $solanaCmd) {
    Write-Host "   📥 Downloading Solana CLI..." -ForegroundColor Yellow
    $tempDir = "C:\solana-install-tmp"
    New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

    try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
        $url = "https://github.com/solana-labs/solana/releases/download/v1.17.0/solana-release-x86_64-pc-windows-msvc.tar.bz2"
        $output = "$tempDir\solana.tar.bz2"

        # Use WebClient as fallback
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($url, $output)

        Write-Host "   ✅ Downloaded, extracting..." -ForegroundColor Yellow
        # Extract using 7-Zip if available, otherwise manual extraction needed
        if (Test-Path "C:\Program Files\7-Zip\7z.exe") {
            & "C:\Program Files\7-Zip\7z.exe" x $output -o"$tempDir" -y
            & "C:\Program Files\7-Zip\7z.exe" x "$tempDir\solana-release.tar" -o"$tempDir" -y

            # Add to PATH
            $solanaPath = "$tempDir\solana-release\bin"
            $env:Path = "$solanaPath;" + $env:Path
            [Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::Machine)

            Write-Host "   ✅ Solana CLI installed" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  7-Zip not found. Please install Solana manually:" -ForegroundColor Yellow
            Write-Host "      1. Download: https://github.com/solana-labs/solana/releases" -ForegroundColor Yellow
            Write-Host "      2. Extract and add to PATH" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ⚠️  Could not download Solana CLI automatically" -ForegroundColor Yellow
        Write-Host "   Manual installation: https://docs.solana.com/cli/install-solana-cli-tools" -ForegroundColor Yellow
    }
} else {
    $solanaVersion = & solana --version 2>&1
    Write-Host "   ✅ $solanaVersion" -ForegroundColor Green
}

# 8. Solana 지갑 생성
Write-Host ""
Write-Host "8️⃣ Creating Solana wallet..." -ForegroundColor Yellow
$walletPath = "$projectPath\wallet.json"
if (Test-Path $walletPath) {
    Write-Host "   ✅ Wallet already exists" -ForegroundColor Green
} else {
    $solanaCmd = Get-Command solana -ErrorAction SilentlyContinue
    if ($null -ne $solanaCmd) {
        # Set to devnet
        & solana config set --url https://api.devnet.solana.com

        # Generate wallet
        Write-Host "   🔑 Generating wallet (press Enter for no passphrase)..." -ForegroundColor Yellow
        & solana-keygen new --outfile $walletPath --no-bip39-passphrase

        Write-Host "   💰 Requesting airdrop..." -ForegroundColor Yellow
        & solana airdrop 2

        $balance = & solana balance
        Write-Host "   ✅ Wallet created with balance: $balance" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Solana CLI not available, skipping wallet creation" -ForegroundColor Yellow
    }
}

# 9. ComfyUI 워크플로우 복사
Write-Host ""
Write-Host "9️⃣ Copying ComfyUI workflows..." -ForegroundColor Yellow
$workflowSource = "C:\StabilityMatrix\Data\Packages\ComfyUI\user\default\workflows"
$workflowDest = "$projectPath\config\workflows"

New-Item -ItemType Directory -Force -Path $workflowDest | Out-Null

if (Test-Path $workflowSource) {
    Copy-Item "$workflowSource\sd15_*.json" $workflowDest -ErrorAction SilentlyContinue
    $copiedFiles = Get-ChildItem "$workflowDest\sd15_*.json"
    if ($copiedFiles.Count -gt 0) {
        Write-Host "   ✅ Copied $($copiedFiles.Count) workflow files" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  No workflow files found to copy" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  ComfyUI workflows not found at $workflowSource" -ForegroundColor Yellow
}

# 10. 최종 확인
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🧪 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Start ComfyUI from Stability Matrix" -ForegroundColor White
Write-Host "   2. Run test: python main.py --test" -ForegroundColor White
Write-Host "   3. Start automation: python main.py" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - Full guide: AUTO_SETUP_STATUS.md" -ForegroundColor White
Write-Host "   - Korean guide: COMPLETE_SETUP_GUIDE_KR.md" -ForegroundColor White
Write-Host ""
