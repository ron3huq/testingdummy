# Findings and limits

The user reported v16 still black on four exact cards and a new loss of both jersey names and numbers. UI names work. CSM receiving was disabled on three checked private components; the private-mesh duplicate detector found zero candidates. These interventions did not fix the phone rendering.

## Proven jersey resource mistake

V16 `noodle_shirt_key_hook` replaced the first FString of config passed to actor virtual 0x860 (0x39c0420) with the player's shirt name. That string is not the name text. Caller 0x39d15ec..0x39d1640 copies it into resource virtual 0x668 = 0x391e53c. That function constructs a Texture2D path under `/Game/Assets/character/Uniform/LowTextures/` from the supplied string. Resource 0x391e864 calls FSoftObjectPath::SetPath 0x45b58b0 and resolves/loads that path. Replacing it with `XUAN SON` therefore requests a nonexistent font atlas. Both names and digits depend on that resource. V17 passes the original config and original key through untouched.

Actual displayed text is stored by char setter 0x39bc570 / std::string setter 0x39bc5ac into actor+0x16e0, copied by 0x391e42c into glyph actor+0x278, read by text renderer 0x391efe4. The text setter hooks remain scoped by exact full Card ID, using the user's requested title case. The native renderer and graphics resources are not emulated by the tests.

## Country evidence

The repository's pinned CPK contains Country.bin (318432 decoded bytes, 214 rows of 1488 bytes) and Player.bin (9681200 decoded bytes, 400 bytes per row). Country names at row+148 identify Vietnam (internal38, flag resource231) and Portugal (internal228, flag resource49). These two numbering systems are not interchangeable.

Original wire getter 0x8257850 reads `(uint32(wire+0x28)>>9)&0x1ff`. The original importer calls it at0x824c5d0, looks up the Country record via0x8257878, then calls native setter0x8257598 at0x824c62c. That setter writes uint16 at runtime record+0x198. V17 calls this setter only after decoding and validating the complete typed player identity. This is separate from the 147 ability parameters and from team membership.

Real source record checks execute the original getter for Ronaldo228, Messi144, Mbappe208, Kane204 and two Vietnamese records38. The CPK hash, file offsets, WESYS decoder and country-row evidence are included. No original tables or owned/save database are modified.

## Four black faces: unresolved, controlled next observation

The normal v17 container is byte-identical to v16, including all approved good faces and card art. The comparison binary changes one profile selection: the four failing card IDs resolve to ND06 instead of NF01/NF27/NFJR/NDHD. All other runtime logic and container bytes are identical. This uses an existing head/material/texture set reported working by the user and avoids inventing another lighting/material intervention.

If the comparison renders correctly, investigation narrows to the changed asset set and its material interaction, rather than a universal inability to display heads on those cards. If it remains black, the corresponding actor/render path needs further inspection. The comparison itself does not prove a final correction; the intended four faces are deliberately replaced temporarily. Phone observation is required before concluding which branch is supported.

## Rebuild

Use the restored environment/dependencies described by v16 source-and-research; its absolute workspace paths are not portable automatically. `prepare_country_sources.py` restores two research tables from the pinned CPK already in this repository. Original libUE4.so with SHA3da06a... remains required. `build_native.sh`, `prepare_deploy.py`, `validate_native.py`, `validate_install.py`, `validate_runtime.py`, `build_comparison.py`, `package_v17.py` reproduce these changes. `prepare_v16_baseline.py` restores unchanged container files from the SHA-pinned v16 ZIP before staging. Dependencies: Python3.12, ziglang0.13, unicorn, pyelftools. No renderer is supplied by this toolchain.
