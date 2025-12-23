"""Constants for seeder package."""

MODEL_MAPPING={
    "policies": "1_policies",
    "roles": "2_roles",
    "permissions": "3_permissions",
}

# Seeding order 
SEED_ORDER = ["policies", "roles", "permissions"]