from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class TestDailyBase(SQLModel):
    linac_id: uuid.UUID = Field(foreign_key="linac.id")
    date: datetime
    sec_interlocks_displaye_on_monitor: bool = False
    sec_door_lights_operational: bool = False
    sec_radiation_sound_indicator_operational: bool = False
    sec_tv_montor_display: bool = False
    sec_um_nterruption: bool = False
    sec_interlocks_collision_mvd_portal: bool = False
    ess_door_operational: bool = False
    ess_console_operational: bool = False
    mec_rangefinder_tolerance_2mm_isocenter: bool = False
    mec_lasers_tolerance_2mm_isocenter: bool = False
    mec_collimator_rotation_axis_tolerance_2mm: bool = False
    mec_mlc_star_pattern: bool = False
    mec_measured_field_value_50x50mm: bool = False
    mec_measured_field_value_100x100mm: bool = False
    mec_measured_field_value_300x300mm: bool = False
    qa_photons_x6: str
    qa_electrons_e6: str
    qa_electrons_e9: str
    qa_electrons_e12: str
    qa_electrons_e15: str
    realized_by_id: uuid.UUID = Field(foreign_key="user.id")
    reviewed_by_id: uuid.UUID = Field(foreign_key="user.id")
    observation: str

class TestDaily(TestDailyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

