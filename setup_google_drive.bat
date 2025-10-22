@echo off
echo ======================================================================
echo   Google Drive Setup for VSCode
echo ======================================================================
echo.

REM Install VSCode Google Drive extension
echo [1/3] Installing Google Drive VSCode Extension...
code --install-extension ms-vscode.google-drive
echo.

REM Install rclone for advanced sync
echo [2/3] Installing rclone...
powershell -Command "Invoke-WebRequest -Uri 'https://downloads.rclone.org/rclone-current-windows-amd64.zip' -OutFile '%USERPROFILE%\Downloads\rclone.zip'"
powershell -Command "Expand-Archive -Path '%USERPROFILE%\Downloads\rclone.zip' -DestinationPath '%USERPROFILE%\Downloads\' -Force"
move "%USERPROFILE%\Downloads\rclone-*-windows-amd64\rclone.exe" "%USERPROFILE%\rclone.exe"
echo.

REM Setup rclone config
echo [3/3] Setting up rclone for Google Drive...
echo.
echo Next steps:
echo 1. Run: rclone config
echo 2. Choose "n" for new remote
echo 3. Name it "gdrive"
echo 4. Choose "drive" for Google Drive
echo 5. Follow OAuth instructions
echo.

pause

REM Launch rclone config
"%USERPROFILE%\rclone.exe" config

echo.
echo ======================================================================
echo   Setup Complete!
echo ======================================================================
echo.
echo To sync your project to Google Drive:
echo   rclone sync "C:\Users\autop\project\nft-automation-project" gdrive:N100NFT-Backup -P
echo.
pause
