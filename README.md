# DIL Connector GUI Deployment

Helm and Kustomize deployment manifests for the DIL Connector GUI.

The application image is:

```text
ghcr.io/data-space-lab/dil-connector-gui:latest
```

## Runtime

The GUI talks to the DIL Connector service inside the tenant vCluster:

```text
http://dil-connector.dil-connector.svc.cluster.local:8282
```

Catalogs advertise the public connector route with `CONNECTOR_PUBLIC_BASE_URL`.
When deployed through ManagementAPI, this is rendered from the tenant host:

```text
https://dil-connector.{tenant_host}
```

Keep `CONNECTOR_BASE_URL` internal for GUI-to-connector API calls, and set
`CONNECTOR_PUBLIC_BASE_URL` to the external route that other participants should
use in catalog `endpointURL` values.

Catalog identity/service metadata is deployment-specific. ManagementAPI should
render the participant ID for the tenant and pass it through Helm values:

```text
CATALOG_PARTICIPANT_ID=did:web:dil-connector.{tenant_host}
CATALOG_SERVICE_ID=dataservice:main
CATALOG_DATA_SERVICE_TYPE=dspace:connector
CATALOG_PUBLISHER={tenant}
CATALOG_HOMEPAGE=https://dil-connector-gui.{tenant_host}
```

The deployment expects a `ghcr-pull-secret` image pull secret in the
`dil-connector-gui` namespace. ManagementAPI should create that secret when
private image pull credentials are automated.

## ManagementAPI Catalog Entry

Use `application-catalog-entry.json` as the deployable application payload in
ManagementUI or `POST /applications`.

The catalog entry includes `helm_values` with tenant placeholders for
`CONNECTOR_PUBLIC_BASE_URL`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and
`CATALOG_PARTICIPANT_ID`.

The catalog entry intentionally defines routes through ManagementAPI instead of
including Gateway API resources in this repo. Tenant-local Argo CD can apply
these manifests without Gateway API CRDs, and ManagementAPI owns host gateway
routing.

## Manual Apply

```bash
kubectl apply -k .
```

For Helm:

```bash
helm upgrade --install dil-connector-gui . \
  --namespace dil-connector-gui \
  --create-namespace \
  --set connector.publicHost=dil-connector.example.org \
  --set connector.publicBaseUrl=https://dil-connector.example.org
```
