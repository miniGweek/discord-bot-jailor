param([string]$Tag,
    [switch]$NoPush)
$CurrentErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Stop"

# Script current location
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptsFolder = (Split-Path $ScriptPath -Parent)
$DockerFilePath = "$ScriptsFolder\docker\Dockerfile"
$AppDir = "$(Split-Path -Parent -Path $ScriptsFolder)\app"

try {
    $Repository = "minigweek/discord-bot-jailor"
    Write-Host "Repository = $Repository"
    $ImageVersion = "$Repository`:$Tag"
    Write-Host "Versioned Image with tag = $ImageVersion"
    $ImageLatest = "$Repository`:latest"
    Write-Host "Image with latest tag  = $ImageLatest"

    docker build -t $ImageVersion $AppDir -f $DockerFilePath
    Write-Host "Done building image as $ImageVersion. Beginning tagging"
    docker tag $ImageVersion $ImageLatest
    Write-Host "Done tagging image $ImageVersion as $ImageLatest"
    if ($NoPush.IsPresent -ne $true) {
        docker push $ImageVersion
        Write-Host "Done pushing image $ImageVersion"
        docker push $ImageLatest
        Write-Host "Done pushing image $ImageLatest"
    }
}
catch {
    Write-Error $PSItem
}
finally {
    $ErrorActionPreference = $CurrentErrorActionPreference
}