from typing import List

import alembic.config

from db.session import get_session
from db.seeds import (
    aux_origins,
    aux_event_types,
    dim_clients,
    dim_calendar,
    dim_business_units,
    dim_productive_units,
    fact_productive_unit_blocks,
    dim_professional_groups,
    aux_productive_family_cleaning_times,
    fact_events,
    fact_surgical_event_details,
)
from models.origins import AuxOrigin


def seed_entities(model, entities: List, entity_name: str = "an entity"):
    with get_session() as db:
        db.add_all(entities_to_create)
        print(
            f"✨ Created {len(entities_to_create)} of {len(entities)} \
{entity_name} in {model.__tablename__} \
({len(pre_existing_entity_codes)} already existed)"
        )


# ensure migrations are up to date
alembic.config.main(argv=["upgrade", "head"])

# seed data
seed_entities(AuxOrigin, aux_origins.get_entities(), "origins")
