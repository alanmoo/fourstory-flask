I've got 20k+ checkins on FourSquare (Swarm) and want a better way to filter through them than the iOS app provides.

This is very much a WIP, and an excuse to work some very stale python muscles, as well as leverage GCP.

URLs:

`/history/date/{date-as-YYYY-MM-DD}`: Show checkins from a specific date


Next top priority:
Move the Datbase from the docker container to an actual GCP service, since, you know, databases shouldn't be ephemeral

