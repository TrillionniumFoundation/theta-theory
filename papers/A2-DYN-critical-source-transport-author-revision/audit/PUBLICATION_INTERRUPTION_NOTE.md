# Interrupted publication call and resumed state

The first prepared GitHub blob-upload call did not return a verified remote result and was interrupted. An exact GET of the intended workflow blob subsequently returned 404. After the user selected the GitHub plugin again, a pending prepared call was rejected because the tool catalog had changed. This was a catalog refresh error, not a successful source publication or an automatic-approval policy rejection.

The refreshed GitHub tool then created the exact intended workflow blob, 34745bb3a225516e1d101519f87c08e42e45e85c. The complete public branch census after resumption still had 1296 heads, byte-identical to the initial census. The frozen local source-preservation checker was rerun successfully. None of these object-upload observations is described as a created revision branch, a completed commit push, or CI; those actions receive their own receipts.
