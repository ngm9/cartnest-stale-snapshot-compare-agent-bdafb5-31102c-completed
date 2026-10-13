# CartNest Product Comparison Agent — Stale Snapshot Incident

## Task Overview
CartNest's storefront comparison assistant answers shopper questions like "compare these three SKUs" by calling a read-only product-details tool that reads price and availability from a PostgreSQL snapshot cache refreshed by a background job. Support is reporting that customers are confidently told items are in stock at a given price, only to find the item unavailable or differently priced at checkout, and some comparisons attribute the wrong numbers to the wrong product. The repository installs, seeds fresh, stale, and missing snapshot rows, and passes its readiness probe, but the agent currently treats aging and absent cache data as trustworthy fact. This matters because false-confident availability and pricing directly erodes customer trust and inflates support load.

## Objectives
- Ensure the assistant never presents cache data that is past its freshness window as if it were current, confirmed fact.
- Ensure each requested SKU's price and availability stay correctly attributed to that SKU, even when some lookups age out or return nothing.
- Ensure snapshot rows that are missing or stale are represented to the model in a structured, honest way rather than silently dropped or defaulted.
- Ensure the final comparison clearly conveys uncertainty or absence for any SKU the cache cannot vouch for.
- Keep the fix contained, readable, and production-safe without changing the tool's read-only nature.

## Helpful Tips
- Review how the tool decides whether a cached snapshot is recent enough to trust, and compare that against the timestamps in the seeded rows.
- Analyze the shape of the value the tool returns for fresh, aged, and absent SKUs, and how the orchestrator consumes it.
- Think about what happens to the SKU-to-result correspondence when one lookup in the batch produces nothing useful.
- Explore the invariant tests and fixtures to see the behavior expected of a fresh, a stale, and a missing SKU.
- Consider what the model can honestly say if the tool tells it clearly that a data point is stale or unavailable.

## How to Verify
> [!NOTE]
> Copy `.env.example` to `.env` and set your provider key. The invariant tests run offline and need no key; only the end-to-end run does.

- Run the readiness probe and confirm the environment reports `ready` before making any change.
- Run the invariant suite and confirm the stale, missing, and attribution checks move from failing to passing after your fix.
- Inspect a tool result for a stale SKU and confirm it is flagged as not-fresh rather than looking identical to a current one.
- Confirm that a batch containing a missing SKU still returns exactly one result per requested SKU, each mapped to the correct SKU.
- Observe the synthesized comparison and confirm stale or absent SKUs are described with appropriate uncertainty instead of confident in-stock/price claims.
- Re-run the checks a second time and confirm the behavior is consistent, not dependent on row ordering.
