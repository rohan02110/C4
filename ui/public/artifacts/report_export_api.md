# VYUHA Administrative Gateway — Report Export Service API

## Endpoint: `/api/v1/reports/<id>/export`
**Method:** `GET`  
**Required Authorization:** `Bearer <JWT_TOKEN>` (Must contain claim `role: "admin"`)

### Parameters:
- `id` (int): Report Identifier (e.g. `101`)
- `source_url` (string, optional): Remote source URL to fetch report header templates.

### Anti-SSRF Perimeter Filter:
The gateway incorporates an egress validation parser to restrict internal pivot attacks:
- **Disallowed Hosts:** `127.0.0.1`, `localhost`, `0.0.0.0`
- **Disallowed Subnets:** RFC 1918 Private Ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)
- **Internal Domains:** Any resolution matching `.internal` is restricted by default.

*Note for Penetration Testers:* Standard string-matching filters can be circumvented via alternative IP representations (e.g. integer or hex notation) or external redirection chains pointing to internal vault service `http://drona.internal:8080/`.
