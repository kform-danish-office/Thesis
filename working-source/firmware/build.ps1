param(
    [ValidateSet('F410', 'G071')]
    [string]$Target = 'F410',
    [string]$ArduinoCli = '',
    [string]$BuildDirectory = '',
    [switch]$Clean
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
if (!$ArduinoCli) {
    $cliCommand = Get-Command arduino-cli -ErrorAction SilentlyContinue
    if ($cliCommand) {
        $ArduinoCli = $cliCommand.Source
    } else {
        $ArduinoCli = Join-Path $env:ProgramFiles 'Arduino IDE\resources\app\lib\backend\resources\arduino-cli.exe'
    }
}
if (!(Test-Path -LiteralPath $ArduinoCli)) {
    throw 'Arduino CLI was not found. Pass its path with -ArduinoCli.'
}

$sketchDir = Join-Path $repoRoot "build-sketch\$Target\thesi_power_control"
$buildDir = if ($BuildDirectory) { [IO.Path]::GetFullPath($BuildDirectory) } else { Join-Path $repoRoot "arduino-build-$($Target.ToLowerInvariant())" }
New-Item -ItemType Directory -Path $sketchDir, $buildDir -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot 'thesi_power_control.ino') -Destination $sketchDir -Force

$compileArgs = @('compile', '--warnings', 'all', '--build-path', $buildDir)
if ($Clean) { $compileArgs += '--clean' }
if ($Target -eq 'F410') {
    $compileArgs += @('--fqbn', 'STMicroelectronics:stm32:GenF4:pnum=GENERIC_F410CBUX,usb=none,xserial=none,opt=oslto')
    # Sector 1 stores settings; vectors stay at zero, app code starts in sector 2.
    $linkerPath = (Join-Path $PSScriptRoot 'stm32f410.ld').Replace('\', '/')
    $compileArgs += @('--build-property', 'upload.maximum_size=98304')
    $compileArgs += @('--build-property', "compiler.c.elf.extra_flags=`"-Wl,--script=$linkerPath`"")
} else {
    $compileArgs += @('--fqbn', 'STMicroelectronics:stm32:Nucleo_64:pnum=NUCLEO_G071RB')
}
$compileArgs += $sketchDir
& $ArduinoCli @compileArgs
if ($LASTEXITCODE -ne 0) { throw "Arduino compilation failed ($LASTEXITCODE)." }
Write-Host "Firmware artifacts: $buildDir"
