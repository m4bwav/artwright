#!/usr/bin/env bash
# Scaffold (runs only with `claude plugin eval --scaffold`). Written by evals/fixtures/make_fixtures.py
# --emit-scaffold; synthetic images drawn in code, museum images fetched and hash-checked.
set -euo pipefail
mkdir -p evals/fixtures/out/renders
base64 -d > evals/fixtures/out/flag.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAFoAAAA8CAYAAADmBa1FAAAAq0lEQVR4nO3QQRHCAAAEsSrpGxEV
ixzk1AG4YK8zecRAjs/5+j7Nfd+Pc9RpoofVaaKHiRYtOleniR4mWrToXJ0mepho0aJzdZroYaJF
i87VaaKHiRYtOleniR4mWrToXJ0mepho0aJz5/V+HNGiRefqNNHDRIsWnavTRA8TLVp0rk4TPUy0
aNG5Ok30MNGiRefqNNHDRIsWnavTRA8TLVp0rk4TPUz09Z/oHxQfINl79C0DAAAAAElFTkSuQmCC
B64
base64 -d > evals/fixtures/out/renders/render_01.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACJUlEQVR4nO3YsU0EQRAEwA8AE5MQ
MAiElDBJEAOTEEgBJAL4FxqWveuulsbkb3q2LC4XEREREREREZE/yv3dw9e1Wf33q5Peb5z0A6X3
Gyf9QOn9xkk/UHq/cdIPlN5vnPQDpfcbJ/1A6f3GST9Qer/LtMDby+PVWf33+i1O+oHS+42TfqD0
fuOkHyi93zjpB0rvN076gdL7jZN+oPR+46QfKL3fONOCq+fWfmfff/f7AwDAuQ949v13vz8AAJz7
gGfff/f7AwDAuQ949v13vz8AAMwOmP5Aq++z+/0BAAAAAAAAAAAAAAAAAAAAyAJw9Adon+VAADj2
AFA+AJQPAOUDQPkAUD4AlM/h/0+wGtDH5/vVOfrvT++3/IEBAAAAAAAAAAAAAAAAAAAAAOAXAFYf
aPr7R98PAAAAAAAAAAAAAAAAAAAAAAD+E8CtBV6fn8zGWQ4EgGMPAOUDQPkAUD4AlA8A5QNA+QBQ
PgCUDwDlA0D5AFA+AJQPAOUDQPksBwBI+QMDAAAAAAAAAAAAAAAAAAAAAMA/Arj1++3f3/3+AADQ
/QC7v7/7/QEAoPsBdn9/9/sDAED3A+z+/u73ByAdwOqC0wOs/v7R91sO5OgFAQAAAAAAAAAAAAAA
AAAAADgVgGkB+wFgPwDsB4D9ALAfAPYDwH4A2O/vAEwL7l7QfuUF7FdewH7lBexXXsB+5QXsV17A
fuUF7CciIiIiIiIicvnJN96F6ldoAXlhAAAAAElFTkSuQmCC
B64
base64 -d > evals/fixtures/out/renders/render_02.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACLElEQVR4nO3YsU0EQQwF0CmAkPBK
IKAQWiKkwQsIKYEWICHeRRpZ9u1/X3J4Y6/9oltLREREREREROSfeX66/RxV9fvp/Vd3uheQ3n91
p3sB6f1Xd7oXkN5/dad7Aen9V3e6F5Def3WnewHp/Vd3uheQ3n/3/e0B7u8vh7W7wLP30/uXAwFg
dn8AwvsDEN4fgPD+AIT3ByC8PwDh/ccD6F5QdXXPDwAAAAAAAAAAAAAAAAAAAAAAkwBUL2j3/enz
AQAAAAAAAAAAAAAAAAAAAADAIwFQtQVAeAEQXgCEFwDhBUB4ARBeAIRXPICv78/Dmv4+AMMPBAAA
AAAAAAAAAAAAAAAAAMAoAOkFQHgBEF4AhBcA4QVAeAEQXgCEVzmAXSBn9fH2Gl27+ys/MAAAAAAA
AAAAAAAAAAAAAABRABxwdpUDAWB2ARBeAIQXAOEFQHgBEF4AhFf8/wTV/ad/X/mBAZj9fd33BwCA
2Qua/j4Aww80/fu67w8AALMXNP19AIYfaPr3XR7A2fvp/bvvDwAA2Qfo7t99fwAAyD5Ad//u+wMA
QPYBuvt33x+AqwPo/sDq/o8+fzmQ7g8AAAAAAAAAAAAAAAAAAAAAIApA9e+vPh8A4fMBED4fAOHz
ARA+HwDh8wEQPh8A4fNtA9gFsjtg9e+vPl950hc8fb7ypC94+nzlSV/w9PnKk77g6fOVJ33B0+cr
T/qCp89XnvQFT59PRERERERERGT95RdpMy1AmSYavQAAAABJRU5ErkJggg==
B64
base64 -d > evals/fixtures/out/renders/render_03.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAB9UlEQVR4nO3SsVEEMRAEwA8AE5MQ
MAiElDBJEAOTEEgBMrijatHv6LanaszX60Z9u4mIiIiIiIiI/DGPD08/R119fnrT9y2ne4D0pu9b
TvcA6U3ft5zuAdKbvm853QOkN33fcroHSG/6vuV0D5De9H3L6R4gven7li/w8fZ82OqAZ+end/X3
LwcCAAAAAAAAAAAAAAAAAAAAAAB3BDC9AAwvAMMLwPACMLwADC8AwwvA8G4PoNpugKvvt3ofAAAA
AAAAAAAAAAAAAAAAAADYCYACoAAoAAqAAqAAKAC6D4DVgL6+Pw979v9nPTt/9QMCAAAAAAAAAAAA
AAAAAAAAAMBOAHRtARheAIYXgOEFYHgBGF4AhheA4W0H8P76oo0FYHgBGF4AhheA4QVgeAEYXgCG
F4DiQFf/PgAAAAAAAAAAAAAAAAAAAAAA+M/sPmB62x8YAAAAAAAAAAAAAAAAAAAAgFEA0h949f12
/34Aws8HIPyBdv9+AMLPByD8gXb/fgDCzwcg/IF2/34Aws+/PID0Abu7el8AwgtAwCMAAAAAAAAA
AAAAAAAAAFcCcPb/6fcDAAAAAAAAAAAAAAAAAAAAAIB7AqgCqf6+2tXft/p+7Q+8+oLdA6ffDwAA
AAAAAAAAAAAAAAAAIAyAiIiIiIiIiGyTX15Xs16jbQk1AAAAAElFTkSuQmCC
B64
base64 -d > evals/fixtures/out/renders/render_04.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAB80lEQVR4nO3SsVEFMQwEUBdASEgJ
BBRCS4Q0SEBICbQAHdzA+JuV0NuZTU/y6a0lIiIiIiIiIvLD3N89fF01Pf900+87Pb/8ggCEk14Q
gHDSCwIQTnpBAMJJLwhAOOkFAQgnvSAA4QXeXh4vu/uA3fmnm37fcSDpBQEAAAAAAAAAAAAAAAAA
AABoBWD3AekDV38fAMWb/n8AAAAAAAAAAAAAAAAAAADNAFQHkt4fAAAAAAAAAAAAAAAAAAAAAAAq
Aah+wHRP/18AiheAAkcAAAAAAAAAAAAAAAAAAP4SyG4/Pt8vW/375Q8MAAAAAAAAAAAAAAAAAAAA
wCgA6QNrGAgAtQvA8AIwvAAMLwDDC8DwAjC8cQCvz09bPf39dNP/DwAAAAAAAAAAAAAAAAAAAAAA
KgFQABQABUABUAAUAAVAAVAAFAAFQAFQABQABUABuPUP+u/vAwAAAAAAAAAAAAAAAAAAAACAW2b3
B3Y/0On94wcGAAAAAAAAAAAAAAAAAAAAAIBfJH3g7vNX93Q/QHr+6p7uB0jPX93T/QDp+at7uh8g
PX91T/cDpOev7ul+gPT81T3dD5Cev6Yn/QPT88cnfYD0/PFJHyA9f3zSB0jPH5/0AdLzxyd9gPT8
8UkfID1/fNIHSM8XEREREREREVk3yjfQMRuxTm4JngAAAABJRU5ErkJggg==
B64
base64 -d > evals/fixtures/out/renders/render_05.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAACAklEQVR4nO3SsVEDUQwEUBdASEgJ
BBRCSw5pkICQEmgBOrA9YzSr9b2d2fROX3qnk4iIiIiIiIjIjXl+evm91PT/p5t+3/T/1w8IQDjp
AQEIJz0gAOGkBwQgnPSAAISTHhCAcNIDAhAe4PP8erHTB7j2/+mm3zcOBIDd7wMAAAAAAAAAAAAA
AAAAAPhnAPcCmX7g9IG2zzd+YAB2z5e+PwAAPPaCt8+Xvj8AADz2grfPl74/AAA89oK3zxc/8LUH
Ti8wDWD7+wAAAAAAAAAAAAAAAAAAAAAAYBMABUABUAAUAAVAAVAAFIBb+/3zdbHbvw/A8gMBAAAA
AAAAAAAAAAAAAAAcDEAayHaA6fePHxgAAAAAAAAAAAAAAAAAAACAQwG4NsDH+1u00/O1vx+A5d8H
YPmB2t8PwPLvA7D8QO3vB2D59wFYfqD29wOw/PsAKAAKgAKgACgACoACoAAoAAqAAqAAKAAKgAKg
hwOQ/v/2+QAAAAAAAAAAAAAAAAAAAAAAoAlAeoHpAwEAAAAAAAAAAAAAAAAAAAAAwCYA9wJJL2C6
6fnHDwzA7vnT9wcAgO4Fts+fvj8AAHQvsH3+9P0BAKB7ge3zn9rTvoD2+eNpX2D7/PG0L7B9/nja
F9g+fzztC2yfP572BbbPH0/7Atvnj6d9ge3zi4iIiIiIiMhx8gceYz0xKpjmlAAAAABJRU5ErkJg
gg==
B64
base64 -d > evals/fixtures/out/renders/render_06.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAB/0lEQVR4nO3Su1EFQQwEwAsAE5MQ
MAiElDBJEAOTEEgBMnhnHMvMPvVUybyPRn0cIiIiIiIiIiJ/lMeHp59bk36+/f+O3ZMuCIBw0gUB
EE66IADCSRcEQDjpggAIJ10QAOGkCwJgcc4W+Hh7vjnp59v/rx5Ie0EAAAAAAAAAAAAAAAAAAAAA
/GvOFrg6Vw+8GsjVOXYPAAAAAAAAAAAAAAAAAAAAAHcFIH2g1Qdo3y99fwAA6C4IAAAAAAAAAAAA
AAAAAGg7cLrg9AHrgaQXSB+wfT8AyifdHwAAAAAAAAAAAAAAAPQBuDpf35835+z/z+bs/en9AQAA
AAAAAAAAAAAAAAAAAABgJwBXD3Tv7weg/EAAAAAAAAAAAAAAAAAAAADDALy/viyd9Pfb/w8AAAAA
AAAAAAAAAAAAAAAAAHYCkC4wfSAAAAAAAAAAAAAAAAAAAAAAAJgEwABgADAAGAAMAAYAA4DpAdAO
ZPX32/dbfmAAuvdL3x8AALoLan8/AOUHat8vfX8AAOguqP39AJQfqH2/9P3rAaye9H7p+wMAQHdB
AAAAAAAAAAAAAAAAAMBuB04XNH3/8QVM3398AdP3H1/A9P3HFzB9//EFTN9/fAHT9x9fwPT9Lxe0
epYvaH8F2F8B9leA/RVgfwXYXwH2V4D9RURERERERGS//AKrlL7mdnVEuAAAAABJRU5ErkJggg==
B64
base64 -d > evals/fixtures/out/sprite_clean.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAA40lEQVR4nO3VsRECMQxEURdASEgJ
BBRCS4Q0SEBICbQA8SWInZU8GP2dUXScrX0BNwYhhHzIfnd4rTwAAACAV/h2OS49MggAADQHiECi
mV3o574CAACwOIBbSF2wGlgGAQAAAKwLXaDq+wAAAAAt7oKP530z2b9PLwwAAM0B1MLVf2ru+eVf
AQAA+DOACOR6Pm0mep496j5yYQAAaA4wu9BsMAAAAAAAAAAA4Pu4IOr72ffJhQEAoDlAtID63AXI
3gcAAADwALILV58PAAAAaAARiHpg9H71+XJhAAAAgBAy2uQNOmujbX/VGcoAAAAASUVORK5CYII=
B64
base64 -d > evals/fixtures/out/sprite_fake.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABhElEQVR4nO2XMU4DQQxF9wCUlGmC
EE1SpEVCoqHMQeipUUTBkai5AwWi4ghcATRSisxoZe+PvcBmn6VfrDzeHb+Z9Xi6DsMwzLDzs8X3
xLUDAAAAcHzCb4/rSevh7lIDAgAAzByAB8TTHyT0v04BAABg4gCiCanAVBUAoxZBAAAAACEAUUBq
ggAAAAByAWQD+fx6r+SN/3h5qsaX519NGAAAmDkANWGvqKnABiQkFc3RTwEAAODEAHhAnrebSp4/
W9v1VfW98mz5008BAADgxAGUgEOVFx6qb0KWP1v3N6vqe+XZ8l8vL16bnG5DKz41yTsCAAAAAAAA
MHMAUh8wZAJKvHfOq/FyH5C9I9R4r9NLX3EAAECrAerdIApgs1hKvX+r9LuA6o8CaOXd/sK3QwAA
wJ6wVxP6JhzpA0oNsGpCq7ZGjN4JRlc8e0eETwUAAEDrA9rxarynnnO8UvGn9gHejmgVjR8gc8X2
SR0dDwAA+AmY/3g0foDMf7b4I/EY1s3bfgD55hQqTUpLVQAAAABJRU5ErkJggg==
B64
base64 -d > evals/fixtures/out/street.png <<'B64'
iVBORw0KGgoAAAANSUhEUgAAAIAAAABgCAYAAADVenpJAAACAUlEQVR4nO3YUUYEYBSA0X8BiSSS
SNpHkkhiJHpORCLGMMqQSETLiEQkIhLtICISERHRLu5sItc1zvv39r2d9nLZje+H03i/OYy/54v4
uj+Jt+t+/D6dx+fdcbxe9eLn8Sw+bgcxim1/Yy72V6die3Esep3Z2FuZjMHWQnTXZ2J3eSKONufj
YG06dpbGR7JtFadkthWnZLat4pTMtuKUzLZVnJLZVpyS2baKUzLbilMy21ZxSmZbcUpm2ypOyWwr
TslsW8UpmW3FKZltqzgls604JbNtFadkthWnZLat4pTMtuKUzLZVnIKCUTAKRsEoGAWjYBSMglEw
CkbBKBgFo2AUjIJRMApGwSgYBaNgFIyCUTAKRsEoGAWjYBSMglEwCkbBKBgFo2AUjIJRMApGwSgY
BaNgFIyCUTAKRsEoGAWjYBSMglEwCkbBKBgFo2AUjIJRMApGwSgYBaNgFFxxCgpGwSgYBaNgFIyC
UTAKRsEoGAWjYBSMglEwCkbBKBgFo2AUjIJRMApGwSgYBaNgFIyCUTAKRsEoGAWjYBSMglEwCkbB
KBgFo2AUjIJRMApGwSgYBaNgFIyCUTAKRsEoGAWjYBSMglEwCkbBKBgFo2AUjIJRMAouOAUFo2AU
jIJRMApGwSgYBaNgFIyCUTAKRsEoGAWjYBSMglEwCu78HwUPAXGWWxstAMmKAAAAAElFTkSuQmCC
B64
mkdir -p evals/fixtures/out/judged-clear
cat > evals/fixtures/out/judged-clear/matches.jsonl <<'JSONL'
{"pair": "3fd6018c8d4d", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "3fd6018c8d4d", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "ae69fd75cb92", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "ae69fd75cb92", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "9889f7714d5c", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "9889f7714d5c", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "ba63983ef9d6", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "ba63983ef9d6", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "5eb4de92dcb3", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "5eb4de92dcb3", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "e04610ed0cea", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "e04610ed0cea", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "0c2935d1e1cb", "order": "1", "pick": "1", "winner": "a", "winner_sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
{"pair": "0c2935d1e1cb", "order": "2", "pick": "2", "winner": "a", "winner_sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c", "confidence": "medium", "criteria": ["read"], "judge": null, "at": "2026-10-22T12:00:00"}
JSONL
mkdir -p evals/fixtures/out/judged-clear
cat > evals/fixtures/out/judged-clear/pairs.jsonl <<'JSONL'
{"pair": "3fd6018c8d4d", "a": {"file": "evals/fixtures/out/renders/render_01.png", "sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c"}, "b": {"file": "evals/fixtures/out/renders/render_02.png", "sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
{"pair": "ae69fd75cb92", "a": {"file": "evals/fixtures/out/renders/render_01.png", "sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c"}, "b": {"file": "evals/fixtures/out/renders/render_03.png", "sha256": "f152d4d30a807dc9d6b4ed2fe8ad398d2fe16c7e8db4e96c0c3b45505beb5307"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
{"pair": "9889f7714d5c", "a": {"file": "evals/fixtures/out/renders/render_01.png", "sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c"}, "b": {"file": "evals/fixtures/out/renders/render_04.png", "sha256": "54c42262e6f22f48bd7b335e086f7d5c28b429f2f06304165a183ef5859f9076"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
{"pair": "ba63983ef9d6", "a": {"file": "evals/fixtures/out/renders/render_01.png", "sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c"}, "b": {"file": "evals/fixtures/out/renders/render_05.png", "sha256": "de7a520efb2755cf0a1e4fc1fd609486c5c53245af24707766e418ff08b25f01"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
{"pair": "5eb4de92dcb3", "a": {"file": "evals/fixtures/out/renders/render_01.png", "sha256": "ac5a74ccdad076e85bba80cfe2a8afea9d534f127f5713510efe669c6e6b142c"}, "b": {"file": "evals/fixtures/out/renders/render_06.png", "sha256": "915398e9a5bf7e9d7d5711cf88452344e2b3bcce9498099d1917ad68d4421c57"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
{"pair": "e04610ed0cea", "a": {"file": "evals/fixtures/out/renders/render_02.png", "sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c"}, "b": {"file": "evals/fixtures/out/renders/render_03.png", "sha256": "f152d4d30a807dc9d6b4ed2fe8ad398d2fe16c7e8db4e96c0c3b45505beb5307"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
{"pair": "0c2935d1e1cb", "a": {"file": "evals/fixtures/out/renders/render_02.png", "sha256": "45e4fd9fdefddde507ecf3a6ce54d8a371c9fdac1015b2f2305a65ade9f8149c"}, "b": {"file": "evals/fixtures/out/renders/render_04.png", "sha256": "54c42262e6f22f48bd7b335e086f7d5c28b429f2f06304165a183ef5859f9076"}, "orders": {"1": ["a", "b"], "2": ["b", "a"]}, "at": "2026-10-22T12:00:00"}
JSONL
