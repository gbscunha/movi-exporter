# API reference (overview)

## API reference

This section describes the Wialon API methods. To use a method, send a
request with the required data and parameters. The section provides the
structure of requests and responses for each method.

## login

Gurtam team has created a more secure way of authorization similar to
oAuth. The previous core/login way of authorization was valid untill 01 Oct
2015. All clients who implemented their own login forms or demo access
links should change them to correspond to the new authorization way.

For now, two forms exist: an extended and a simplified one.

### Extended form

The extended form is generally useful for mobile and other apps.

```http
http://<host>/login.html

http://<host>/login.html?client_id=...&access_type=...&activation_time=...&duration=...&lang=...&flags=...&user=...&redirect_uri=...
&response_type=...&css_url=...
```

All the parameters are optional.

Name           Description                                 Default

Name of the app/site/client for which       Site name
client_id
you want to generate a token.               (title).

access_ty
token flags                                 0x100
pe

activation     Token activation time. UTC time in
0
_time          seconds: 0 - now.

Token duration in seconds. Set to 0 for
2592000
unlimited duration.
duration                                                   (30 days
If the token is not used for 100 days, it
in seconds).
is automatically deleted.

lang           Language (en, ru, etc.).

flags          See below.                                  0

user           Username. Will be in the login field.

redirect_ur      URL to redirect and forward                   login.html
i                authorization results.                        itself

response_        The response will contain the token
Token.
type             (token) or AuthHash (hash).

URL to CSS-file with the specified styles
css_url
for login_simple.html.

### Flags

| Flag | Description |
| --- | --- |
| Return user_name in the response. | 0x1 |
| Return in the response: |  |
| client_id, |  |
| access_type (if response_type=token), | activation_time, 0x2 duration, flags, |
| response_type, | svc_error. |
| Return all the parameters from the request excluding the | reserved ones (client_id, response_type, access_type, 0x4 activation_time, duration, flags, login, passw, redirect_uri, p, app, sign, hash, remote_hash). |
| After successful authorization, a redirect to redirect_uri occurs, and the | following GET-parameters are transferred: |
| access_token (72-symbol token which may be used for authorization in | future); user_name (authorized username, if 0x1 flag was stated before token generation). |
| In case of an authorization error, a redirect occurs to the login form itself, | the specified error is shown and the following GET-parameters are transferred: |
| svc_error (error code); | client_id; access_type; activation_time; duration; flags. |
| After getting a 72-symbol token, you may use it in your authorization apps: |  |

```http
svc=token/login&params={"token":"<access_token>","operateAs":"<optional_sub_user>"}

     The number of tokens per user is limited to one thousand.
```

### Simplified form

The form is used for simple embedding into sites via iframe to quickly
access one or more monitoring sites after authorization. By default, a link
to the monitoring site will be created. Also, you may add links to other sites
(using cms_url, lite_url, mobile_url, demo_url).

```http
http://<host>/login_simple.html

http://<host>/login_simple.html?lang=...&cms_url=...&cms_title=...
&lite_url=...&mobile_url=...&demo_title=...&demo_url=...&title=...
&css_url=...
```

All the parameters are optional.

| Name | Description |
| --- | --- |
| lang | Language (en, ru, etc.). |
| URL to a CMS Manager site (for example, | cms_url         http://cms.wialon.com ). If stated, it will be added to the list of quick jump sites. |
| cms_title | Link title for CMS Manager. |
| lite_url | URL to a Wialon Hosting Lite site (for example, |

```http
http://lite.wialon.com ).
```

lite_title      Link title for Wialon Hosting Lite.

mobile_u        URL to a Wialon Mobile site (for example,
rl              http://m.wialon.com ).

mobile_ti
Link title for Wialon Mobile.
tle

title           Link title for the monitoring site.

URL for demo access (for example,
demo_url

```http
http://hosting.wialon.com/?token= <token>).
```

demo_titl
Link title for demo access.
e

URL to a CSS file with the specified styles for
css_url
login_simple.html.
