CREATE TABLE IF NOT EXISTS product_snapshots (
    sku TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
    currency TEXT NOT NULL DEFAULT 'USD',
    in_stock BOOLEAN NOT NULL,
    fulfillment_center TEXT NOT NULL,
    fetched_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_product_snapshots_fetched_at
    ON product_snapshots (fetched_at);

-- Fresh snapshots (refreshed within the last few minutes).
INSERT INTO product_snapshots (sku, name, price_cents, currency, in_stock, fulfillment_center, fetched_at) VALUES
    ('BIN-3001', 'Stackable Storage Bin 12L', 1499, 'USD', TRUE,  'FC-EAST',  NOW() - INTERVAL '2 minutes'),
    ('CRT-9005', 'Rolling Utility Cart 3-Tier', 5299, 'USD', TRUE,  'FC-WEST',  NOW() - INTERVAL '4 minutes');

-- Stale snapshots (well past any reasonable freshness window).
INSERT INTO product_snapshots (sku, name, price_cents, currency, in_stock, fulfillment_center, fetched_at) VALUES
    ('SHELF-7742', 'Adjustable Wire Shelf Unit', 8999, 'USD', TRUE,  'FC-CENTRAL', NOW() - INTERVAL '9 hours'),
    ('BOX-2210',   'Collapsible Fabric Box Set', 2599, 'USD', FALSE, 'FC-EAST',    NOW() - INTERVAL '3 days');

-- Note: SKU 'DRW-5150' is intentionally absent to represent a cache miss.
