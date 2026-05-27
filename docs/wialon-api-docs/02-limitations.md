# Limitations

To ensure the effective operation of the Wialon system, take into account
the limitations listed below.

## Limits for Logins and Sessions

No more than 10 failed logins from one IP address in a minute.
No more than 120 successful logins from one IP address in a minute.

No more than 100 active sessions of one user from one IP address.

No more than active 1000 tokens per user.
No more than 1 password reset attempt in a minute.

If such limitations are exceeded, the IP address will be temporarily blocked.
It can cause difficulties to log in.

## Limits for Messages

No more than 15 million messages can be loaded into all user sessions.
No more than 15 million messages can be loaded by a user within 2
minutes.
No more than 500 thousand messages can be imported in a minute.
No more than 200 million messages can be loaded by a user within 1
hour.
No more than 50 message layers.
No more than 2 GB of messages on request.

After reaching the limit, the user can’t load or import messages within the
specified time period. It may cause difficulties in executing reports,
requesting tracks etc. In this case, clear tabs (Tracks, Messages, Reports) or
reload the page and try again.

## Limits for Reports

5 minutes of server time are dedicated to executing a report online.

5 minutes of server time are dedicated to executing a report by
notification.
10 minutes of server time are dedicated to executing a report by job.

400,000 is the maximum number of rows in a report with detalization.
A user can’t request more reports per hour than the system can execute
during an hour.
A timeout for continuous execution of one or more reports for one user
from one IP address is 10 minutes; reports cannot be requested for 10
minutes after exceeding this limit.

When the time limit is reached, the report execution will be skipped (no
results will be returned). In this case, reduce the report time interval,
amount of units or the requested data (tables, charts, etc.).

## Other Limits

No more than 3 resource-intensive requests can be processed
simultaneously during one session (e.g. message loading, report
execution etc.).
No more than 10 API requests can be processed simultaneously during
one session.

No more than 3 map tracings can be processed simultaneously during
one session.
No more than 10 avl_evts requests can be processed within 10 seconds
during one session.
No more than 30 core/check_unique requests can be processed within 1
minute.
200 seconds of server time are dedicated to rendering tiles from one IP.

120 seconds of server time are dedicated to rendering tiles from one IP
per user.
9007199254740991 is the maximum integer value that can be sent in a
parameter of the double type without distortion. To send larger values,
use parameters of the long type.
