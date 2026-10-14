# Existing-server reconnection observation

The parent live tool read through existing kubectl-home exec printed:

    READY True
    ORIGINAL_SERVER_LIVE 296241 True

The same read printed server_started.json pid296241 and an absent server
terminal, plus full_control_progress showing12 completed executors. That
command then wrote full_observation_disconnect.json with UTC 2026-10-14T05:29:10.526668+00:00.
A following actual client-Pod read found client_started absent before launching
the source-native client. Original server command/terminal receipts retain
pid296241. This is retained parent observation evidence, not a separately
archived raw earlier RPC stream or continuous-isolation proof. The exact
instant of controller failure was not timestamped.
