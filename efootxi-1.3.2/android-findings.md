# Android efootxi 1.3.2: Select Team investigation

This report supersedes guesses based only on the iOS reference and pasted transcript. Device execution remains unverified.

## Inputs and provenance

Two uploaded archives were retrieved and extracted: efootxi-1.3.2.rar (51 entries) and chaquopy_resourcebootstrap_ue4game_dexopt.rar (221 entries). gateway-release.rar and kotlin_lib_metainf_res.rar could not be transferred because each exceeds the download tool's 32 MiB limit; they have not been inspected directly.

The uploaded resource-bootstrap configuration names https://github.com/maxlzyver/efootxi/releases/download/resources-311010101-v1/ and the update channel. The public repository contains documentation only; application source is maintained privately. Retrieved the public v1.3.2 APK as a baseline. Its SHA-256 is 7fe3ca7f935cee91ff870a786abc43b948a94575e2d0d72e54bb35ece75af057, matching the GitHub release asset digest. classes7.dex, classes8.dex, AndroidManifest.xml, assets/chaquopy/app.imy and assets/resource-bootstrap/manifest.json match uploaded files byte for byte. This proves those components match; it does not establish that an inaccessible user gateway archive or prior V7 modifications match the baseline.

## Actual Android server code

Extracted work/tools/my_league.py and gate_logic.py from assets/gateway-release in the APK.

- my_league.root_view returns a neutral selection state (team_id=0, league_compe_unit_id=65535, league_team_id_list=[]) when no season exists. With an existing season, its list comes from that season's ranking. The Android source explicitly describes native client picker construction. The reference iOS handler is different and should not be substituted.
- my_league.select consumes select_team_id and select_compe_unit_id, validates team_to_competition and schedule membership, then starts/resumes a season. It cannot by itself make a team appear in the native picker before selection.
- Existing season data retains schedule_v2. Changing source schedule JSON does not necessarily alter an existing season.
- Captured 106_gate_CMD_GET_USEABLE_TEAM_LIST_resp.txt decodes to 963 IDs, use_league_category=ALL. Both Arsenal (101) and Lille (213) are present. The 539-ID EUROPEAN_LEAGUE response in the iOS reference is a different capture.

## Storage and bootstrap behavior, from uploaded DEX disassembly

EmbeddedGateway.ensureStarted uses Context.getFilesDir()/embedded-gateway, not getExternalFilesDir(). It compares installed-release.txt to release-manifest.release_id and copies packaged release members on a release change, preserving an existing local-club.sqlite3. This is only one stage of startup.

GatewayGuard.prepare is another stage: when installed-release.txt exists, it checks support-file presence/length; existing files of matching length pass this particular check without being rehashed. Missing or differently sized files are recopied from APK assets into .repairing files and verified against the release manifest's expected byte count and SHA-256 before renaming. Its explicit failure text is 本地支持文件校验失败, matching the transcript's failure. Thus changing release_id alone is not a complete explanation or fix; copied/installed paths, manifest contents and repair behavior all matter. Do not disable verification.

ResourceBootstrap.Coordinator.createInstaller also uses getFilesDir() for downloaded resources. ResourceInstaller includes file lengths, SHA-256 verification and verification receipts. The app's ResourceDocumentsProvider exposes internal data and external data as different roots; virtual document IDs named files resolve to getFilesDir(). Visual directory labels in a file manager must not be assumed to be physical Android/data paths.

## Base database and live database

The APK directly contains assets/dt200_mobile_all.cpk (4,355,584 bytes), separate from gateway-release/livedata/dt870_mobile_and.cpk (7,323,280 bytes). Both contain CategoryTeamList.bin and CompetitionEntry.bin with the old 18-team Ligue 1 membership.

Decoded Android CategoryTeamList has 31,020 bytes (2,585 12-byte records); CompetitionEntry has 8,628 bytes (719 12-byte records). These differ from the iOS reference. Each target table is WESYS-wrapped; the existing encrypted version is supported by the parser and the probe preserves it. Arsenal is ID 101, Manchester United is ID 100; they must not be confused.

The native library has references to base dt200 and live dt870. Recovered a native GetTeamList binding/call chain (for one of several menu classes) through 0x3faa648 -> 0x308c98c -> 0x737e05c, which reads native in-memory region/league/team lists. This is static evidence of client-side lists, not a captured runtime trace proving which database populated the My League picker. The active dt200-versus-dt870 precedence for this specific screen remains to be demonstrated on device.

## What pc0000 actually contains

The APK's assets/pc0000_mobile_and.pak is a ZIP container, 523,235,524 bytes, with 15 entries. It is not directly a standalone Unreal PAK. Inside are Idsphone.pak, pakchunk0-Android_ETC2.pak, assets/pc0101_mobile_and.pak, assets/pc7000_mobile_and.pak and related IoStore files.

Read all four nested PAK indexes (225, 3,901, 0, 227 entries respectively). AES decoding of encrypted primary indexes was verified against stored SHA-1 digests. Read four nonempty IoStore directory indexes (227, 1,509, 2,001, 321 entries). global.utoc lacks a directory index and is not covered by the directory parser. No nested PAK entry path identified a pesdb/dt200 team database. One IoStore path is DT_TeamSelectTags.uasset (effect data by path); this name alone does not establish team membership storage. The large movie containers should not be patched merely because of their names.

Tool used for PAK indexing: repak v0.2.3, downloaded from trumank/repak and verified against its published SHA-256 before execution. Existing repository tools parsed CPK and WESYS. No application native binary or Android Python entry point was executed.

## Concrete diagnostic artifact

../efootxi-1.3.2-select-team-dt200-probe.zip contains:

- test/assets/dt200_mobile_all.cpk: swap Arsenal (101) and Lille (213) only in direct English League (113) and Ligue 1 (122) memberships in the two tables above.
- restore/assets/dt200_mobile_all.cpk: original baseline.
- HUONG_DAN.txt: Vietnamese instructions, exact-input SHA-256 guard, rollback and interpretation.
- validation.json: exact changed records and hashes.

The test CPK keeps its original size; every byte outside the two existing table allocations is identical. Four decoded records change in total. Each modified encrypted WESYS table was decoded again and compared to the intended result. Both leagues retain their counts (20 and 18), contain no duplicate teams, and have the intended swapped memberships in both tables. ZIP CRC validation passed.

Ordinary zlib output exceeded the original table allocations, so no oversized or truncated payload was written. Zopfli produced compatible zlib streams within both allocations. TOC offsets/sizes and all other CPK members remain unchanged.

Original dt200 SHA-256:
088bb2e661cfcd8a1110c40402a461dac0c37eecdbce72ce692d505a77050954

Probe dt200 SHA-256:
dd22d6cc3a0870efb12350023de8793ef786c72c19467ec500eb9aac533d2a8e

This is a menu-source probe, not a playable or full Super League patch. It deliberately leaves registry, schedules, native library, DEX, player data and saves untouched. Do not confirm the diagnostic selection or create a season with it. Use a copy of the current APK and preserve signing compatibility. Apply only if its dt200 matches the exact original hash, and restore after testing. If the input differs, inspect that version instead of replacing it blindly.

## Remaining device check and final implementation

Check whether a fresh process shows Arsenal in Ligue 1 instead of Lille. A positive result demonstrates that the changed dt200 membership affects this picker and supports a full targeted patch. A negative result requires verification that the installed APK contains the probe hash, followed by the actual runtime lookup/override path; it does not automatically prove hardcoding in libUE4.so.

Once the active source is established, apply the desired 18-team mapping consistently to that source and the actual installed V7 server state: registry in both directions, donor competitions, schedules, and serialized responses. Preserve unrelated Argentine/Colombian changes. Validate selection acceptance, a new season, a real match and restart. Old-season migration is separate and needs a backup. The inaccessible uploaded gateway archive and the exact previous V7 payload have not been compared, so no claim of preserving their unknown content has been made.

No tracked files in /workspace/testingdummy or user saves were changed. Full Android runtime success is not yet established.
