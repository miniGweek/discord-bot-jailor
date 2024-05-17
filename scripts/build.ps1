param([string]$tag,
    [switch]$NoPush)
$CurrentErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Stop"
# script current location
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptsFolder = (Split-Path $ScriptPath -Parent)
$DockerFilePath = "$ScriptsFolder\docker\Dockerfile"
$AppDir = "$(Split-Path -Parent -Path $ScriptsFolder)\app"

try {
    $repository = "minigweek/discord-bot-jailor"
    Write-Host "Repository = $repository"
    $imageVersion = "$repository`:$tag"
    Write-Host "Versioned Image with tag = $imageVersion"
    $imageLatest = "$repository`:latest"
    Write-Host "Image with latest tag  = $imageLatest"

    docker build -t $imageVersion $AppDir -f $DockerFilePath
    Write-Host "Done building image as $imageVersion. Beginning tagging"
    docker tag $imageVersion $imageLatest
    Write-Host "Done tagging image $imageVersion as $imageLatest"
    if ($NoPush.IsPresent -ne $true) {
        docker push $imageVersion
        Write-Host "Done pushing image $imageVersion"
        docker push $imageLatest
        Write-Host "Done pushing image $imageLatest"
    }
}
catch {
    Write-Error $PSItem
}
finally {
    $ErrorActionPreference = $CurrentErrorActionPreference
}