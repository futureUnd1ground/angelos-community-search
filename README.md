# Community Search for AngelOS

Search approved Community Store plugins through the native launcher (Mod+Space), in heaven and hell. Use a plugin name directly, or `market` / `market dog`. Results show available and installed versions; Enter opens the corresponding Community Store card. Settings provide shortcuts to Market and ZIP publication. There is no background polling; the catalog is read on first search.

## Install

Requires Community Store 0.9.1+. Drop `community-search-v1.0.0.zip` in Community Store's ZIP field, click “Установить ZIP”, then search `market` in “Выполнить…”. Enable Community Search in AngelOS plugin settings if it was previously disabled.

## Publish your plugin

Search “Опубликовать ZIP” or `market publish`, press Enter, select your plugin ZIP and click “Опубликовать ZIP в Market”. GitHub CLI (`gh auth login --web`) supplies authentication. Community Store publishes a public source snapshot and immutable-version ZIP release, then creates a registry PR targeting main with pending status. Moderator approval is required before other users see it in Market. Git and gh must be installed. Failure messages remain in the page; identical ZIPs reuse their release/PR when retried.

The ZIP must contain one manifest.json at its root or in one plugin folder, a stable lowercase id, name, version (1.0.0), description and real declared entry points. Optional repository must be your public GitHub repository; otherwise a repository named angelos-<id> is created under your account. Use a new version for changed bytes. Include author, license, category, tags, dependencies and permissions for review.

Networking: HTTPS GET of the configured Community Store registry through its validated Python reader. No installation/removal takes place when selecting a search result. Publishing only happens after the explicit publication button.

License: MIT.
