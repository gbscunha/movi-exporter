# Introduction

This documentation contains the information necessary to develop your
own applications integrated with Wialon.

Only the POST method is used for the requests. The additional parameters
(params) are sent and returned as JSON. For all text parameters, the UTF-8
coding should be used.

It is recommended to use the DEC format as HEX is only
supported as a text format.

For Wialon Hosting, the https://hst-api.wialon.com/ host is used in the
requests (https://hst-api.wialon.us, https://hst-api.wialon.eu,
https://hst-api.wialon.org — depending on the data centre), for Wialon
Local — the URL monitoring site.

## Request template

A template of any request should be like this:

```http
https://{host}/wialon/ajax.html?sid=<text>&svc=<svc>&params={<params>}

       It is necessary to indicate Content-Type:application/x-www-form-urlencoded in the request header.
```

### Parameters

The following parameters must be used in a request:

| Name | Description |
| --- | --- |
| sid | The unique ID of the session. |
| svc | The name of the request. |
| params | The parameters for the request execution. |
| The following sections describe only the values of the parameters svc and | params. |
| The session identifier (sid) is a required parameter for all | requests. The exceptions are the requests from the token/login section and some requests from the Other methods section. |
| If there are no running requests, the default session duration is 5 minutes. | To maintain the session, you should use the constant sending of the avl_evts request, for example, every 2 seconds. |
| All numbers, including flags, must be in decimal system. |  |
