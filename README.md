# DIL Connector GUI Deployment

Kustomize deployment manifests for the DIL Connector GUI.

The application image is:

```text
ghcr.io/data-space-lab/dil-connector-gui:latest
```

## Runtime

The GUI talks to the DIL Connector service inside the tenant vCluster:

```text
http://dil-connector.dil-connector.svc.cluster.local:8282
```

Catalogs advertise the public connector route with `CONNECTOR_PUBLIC_BASE_URL`:

```text
https://connector.dil.collab-cloud.eu
```

Keep `CONNECTOR_BASE_URL` internal for GUI-to-connector API calls, and set
`CONNECTOR_PUBLIC_BASE_URL` to the external route that other participants should
use in catalog `endpointURL` values.

The deployment expects a `ghcr-pull-secret` image pull secret in the
`dil-connector-gui` namespace. ManagementAPI should create that secret when
private image pull credentials are automated.

## ManagementAPI Catalog Entry

Use `application-catalog-entry.json` as the deployable application payload in
ManagementUI or `POST /applications`.

The catalog entry intentionally defines routes through ManagementAPI instead of
including Gateway API resources in this repo. Tenant-local Argo CD can apply
these manifests without Gateway API CRDs, and ManagementAPI owns host gateway
routing.

## Manual Apply

```bash
kubectl apply -k .
```
