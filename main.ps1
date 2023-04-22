param(
  [string]$language = "English",
  [switch]$remove_subs_dir
)

$folders = Get-ChildItem -Path ./Subs -Directory
$subs_to_move = @()

foreach ($f in $folders) {
  $subs = Get-ChildItem -Path $f.FullName -File | Where-Object {$_.Name -like "*$language*.srt"}

  $sizes = @($subs | ForEach-Object { $_.Length })
  $mean = ($sizes | Measure-Object -Average).Average

  if ($sizes.Count -gt 2) {
    # if there are more than 2 subtitles in the same language, the first is only foreign dialogues,
    # the last is audio description for deaf persons.
    # The ones in the middle are most likely to be a transcription of only the dialogues.
    # By doing the closest to the mean, it is ensured to pick the right one
    $idx = [array]::IndexOf($sizes, ($sizes | Sort-Object { [math]::Abs($_ - $mean) })[0])
    $subs_to_move += $subs[$idx].FullName
    continue
  }

  if ($sizes.Count -eq 2) {
    # if there are only two files, there are to scenarios:
    $hola = $sizes | Measure-Object -StandardDeviation
    $std = $hola.StandardDeviation
    $cv = $std / $mean
    if ($cv -gt 0.5) {
      # the first being foreign language transcription and normal transcription.
      # This happens when the STD is high (one file has a small size and the other a big size).
      # Picking the bigger size one.
      $idx = [array]::IndexOf($sizes, ($sizes | Sort-Object -Descending { [math]::Abs($_ - $mean) })[0])
      $subs_to_move += $subs[$idx].FullName
    } else {
      # the second being normal transcription and audio description for deaf person.
      # both files have similar size, and thus a lower std. Picking the smaller size one
      $idx = [array]::IndexOf($sizes, ($sizes | Sort-Object { [math]::Abs($_ - $mean) })[0])
      $subs_to_move += $subs[$idx].FullName
    }
    continue
  }

  if ($sizes.Count -eq 1) {
    $subs_to_move += $subs.FullName
    continue
  }
}

foreach ($sub in $subs_to_move) {
  $parent = (get-item $sub).Directory.BaseName
  $suffix = [System.IO.Path]::GetExtension($sub)
  Copy-Item $sub -Destination "./$parent$suffix"
}

if ($remove_subs_dir) {
  Remove-Item -Path ./Subs -Recurse
}