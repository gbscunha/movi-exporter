# Wialon for Developers — API Documentation

Documentação oficial da API Wialon, convertida do PDF de 939 páginas para Markdown.
Host base de produção (Wialon Hosting): `https://hst-api.wialon.com/`.

## Padrão de requisição

```http
POST https://hst-api.wialon.com/wialon/ajax.html?sid=<text>&svc=<svc>&params={<params>}
Content-Type: application/x-www-form-urlencoded
```

Apenas o método **POST** é utilizado. Os parâmetros adicionais (`params`) são enviados e
retornados em JSON. Para todos os parâmetros de texto, usar codificação UTF-8.

## Conceitos e referência geral

- [Introduction](./01-introduction.md)
- [Limitations](./02-limitations.md)
- [Data format](./03-data-format.md)
- [Messages](./04-messages.md)
- [Units](./05-units.md)
- [Resources](./06-resources.md)
- [Retranslators](./07-retranslators.md)
- [Routes](./08-routes.md)
- [Time](./09-time.md)
- [Daylight saving time](./10-daylight-saving-time.md)
- [Time zones](./11-time-zones.md)
- [Example of obtaining the “tz” parameter](./12-tz-example.md)
- [Tokens](./13-tokens.md)
- [Unit groups](./14-unit-groups.md)
- [Users](./15-users.md)
- [Error codes](./16-error-codes.md)

## API reference (por serviço)

- [Overview](./api-reference/00-overview.md)
- [`account`](./api-reference/account.md) — 25 método(s)
- [`core`](./api-reference/core.md) — 26 método(s)
- [`events`](./api-reference/events.md) — 6 método(s)
- [`exchange`](./api-reference/exchange.md) — 10 método(s)
- [`file`](./api-reference/file.md) — 8 método(s)
- [`item`](./api-reference/item.md) — 13 método(s)
- [`messages`](./api-reference/messages.md) — 7 método(s)
- [`order`](./api-reference/order.md) — 13 método(s)
- [`render`](./api-reference/render.md) — 11 método(s)
- [`report`](./api-reference/report.md) — 20 método(s)
- [`resource`](./api-reference/resource.md) — 40 método(s)
- [`retranslator`](./api-reference/retranslator.md) — 5 método(s)
- [`route`](./api-reference/route.md) — 9 método(s)
- [`token`](./api-reference/token.md) — 3 método(s)
- [`unit`](./api-reference/unit.md) — 64 método(s)
- [`unit_group`](./api-reference/unit_group.md) — 1 método(s)
- [`user`](./api-reference/user.md) — 30 método(s)

## Padrões adicionais

- [Item search](./18-item-search.md)
- [Event management](./19-event-management.md)
