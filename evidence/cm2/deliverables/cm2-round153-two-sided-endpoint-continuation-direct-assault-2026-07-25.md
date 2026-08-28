# CM2 Round153 — direct assault record

Date: 2026-07-25

The independent verifier rejected all ten fully re-signed semantic attacks:

```text
delete_row
survive_bridge
invent_event
disconnect_atlas
erase_axis_terminal
close_upper
close_D02
authorize_D03
promote_gate5
promote_CM2
```

It also rejected all four strict parser attacks:

```text
duplicate JSON key
UTF-8 BOM
non-object top level
NaN constant
```

Final result: `10/10` semantic attacks rejected and `4/4` strict
JSON/encoding attacks rejected.
