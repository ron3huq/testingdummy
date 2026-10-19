# dt200 black-screen follow-up

The user reports that installing the first Arsenal/Lille dt200 probe led to a black screen; restoring the original dt200 restored normal game startup. The old probe has been withdrawn on chat-downloads. This establishes a device failure associated with that probe, not a successful menu-source test.

## Newly supplied gateway files

Retrieved the latest work.rar and outputs.rar. Both were extracted without executing archive contents. Compared 7,359 members against the SHA-256-verified public APK baseline: 7,353 match and six differ. The changed files are ml_competition_registry.json and ml_schedule_113/116/119/122/476.json. All 52 work/ files match the original. The SQLite seed also matches the original and passes read-only PRAGMA quick_check. No database was changed or uploaded to GitHub.

Checked the user-supplied registry, reverse mappings and schedules for all 24 competitions. No duplicate membership, reverse-map mismatch, foreign-team fixture, self-match, repeated team in a round or missing even-league participant was found. Ligue 1 has 18 teams, 34 rounds and each of its 306 directed pairings exactly once. It retains Lyon (181), unlike the later Dortmund discussion in the pasted transcript. These uploaded files must not be treated as an unseen V7 patch with all later requested modifications.

livedata.rar still exceeds the 32 MiB transfer limit. The actual supplied dt870 and gateway-root release-manifest.json remain unavailable for comparison. Separate small copies were requested.

## Defect found in the old probe

The first probe changed encrypted WESYS payloads but retained stale CRC metadata for CategoryTeamList.bin and CompetitionEntry.bin. Our first validator checked decompression, logical records and preservation outside the two table allocations; it did not check member CRC fields. That omission was an error in the generated probe.

The CRI field named CRC does not use standard zlib.crc32. The native CRI TOC validator uses the recurrence h = h * 0x301 + byte, modulo 2^32, followed by a bitwise complement and the native zero special case. The TOC seed is 0xdeadbeef, GTOC seed 0x00beef00; member CRC seed is the stored member length. The formula matches all 3,110 members and both directory checksums in the original dt200. The old probe fails exactly the two modified members, while its unchanged TOC and GTOC still pass.

This is a concrete, corrected integrity defect consistent with the failure. It does not prove, without a device trace, that no other startup condition is involved.

## Native component validation

Located the actual Android WESYS xorshift decoding code at VA 0x8212c48 and native zlib entry points at 0x6917d9c, 0x6917eb0 and 0x6919fcc in the verified libUE4.so. Executed these pure-memory routines in an ARM64 CPU emulator with bounded instruction counts and restricted allocation/memory callbacks. Neither Android system services nor application entry points were run.

Both original and probe tables return Z_STREAM_END, consume all compressed input, fill the expected output and exactly match the Python-decoded bytes. This narrows the problem beyond merely saying that Python zlib accepts them; it does not validate the complete loader or game.

The corrected probe changes the two member CRC values in TOC and then the dependent TocCrc in the CPK header. Payload bytes are unchanged from the old probe. Its 3,110 member checksums, TOC and GTOC all pass. The actual native criCpkAnalyzer_CheckTocCrc32 routine at VA 0x8bc60ac was also executed with CRC checks enabled: it accepts both original and corrected TOCs and rejects an intentionally wrong expected checksum. Verification was preserved, not disabled.

Corrected dt200 SHA-256:
a37c2b81de7bb2172f2549d155bdd1e717f09efc4f8d50feba07ec390967cfe6

Original dt200 SHA-256:
088bb2e661cfcd8a1110c40402a461dac0c37eecdbce72ce692d505a77050954

## Status and next checks

The new CRCFIX artifact is a corrected, device-untested menu-source probe, still only Arsenal (101) swapped with Lille (213) in two direct competition memberships. It is not a complete Super League patch. The old failed probe must not be reapplied. A fresh device run must separately establish startup and picker behavior before implementing the complete mapping. No DEX, native binary, player tables, server logic, registry, schedules or save is included as a modification.

The downloaded archive and raw file are published on the already-authorized chat-downloads branch with separate status and recovery instructions. No user save, full outputs archive or secret-bearing configuration was published.
