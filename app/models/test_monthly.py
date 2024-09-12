from sqlmodel import SQLModel, Field
from datetime import datetime


class TestMonthlyBase(SQLModel):
    linac_id: int | None = Field(foreign_key="linac.id")
    date: datetime
    sec_verification_of_interlocks_and_treatment_accessories_working: bool = False
    sec_fixation_of_stretcher_movements_working: bool = False
    sec_electric_power_cut_off_buttons_working: bool = False
    mec_mechanical_isocenter_2mm: bool = False
    mec_arm_angle_indicators_1st: bool = False
    mec_collimator_angle_indicators_1st: bool = False
    mec_telemeter_in_isocenter_and_linearity_2mm: bool = False
    mec_lasers_2mm: bool = False
    mec_collimator_rotation_2mm: bool = False
    mec_symmetry_parallelism_and_orthogonality_field_sizes_2mm: bool = False
    mec_coincidence_of_light_and_radiation_fields_plaque_3mm: bool = False
    mec_horizontality_and_verticality_of_the_stretcher_2mm: bool = False
    mec_verticality_of_the_light_axis_2mm: bool = False
    mec_pedestal_rotation_axis_1mm: bool = False
    mec_picket_fence_test_2mm: bool = False
    mec_sheet_speed_0_5_cm_s: bool = False
    mec_sliding_window_test_0_35_cm: bool = False
    mec_mlc_field_sizes_2mm: bool = False
    kv_and_mv_collision_interlocks_working: bool = False
    kv_and_mv_mechanical_qa_working: bool = False
    kv_and_mv_positioning_repositioning_less_than_2_mm: bool = False
    kv_and_mv_img_and_tto_match_4_gantry_angles_less_than_2_mm: bool = False
    kv_and_mv_scaling_less_than_2_mm: bool = False
    kv_and_mv_baseline_spatial_resolution: bool = False
    kv_and_mv_baseline_contrast: bool = False
    kv_and_mv_baseline_noise_and_uniformity: bool = False
    kv_and_mv_full_range_of_travel_ssd_annual_plus_minus_5_mm: bool = False
    cone_beam_ct_kv_img_cone_beam_ct_kv_and_tto_match_less_than_2mm: bool = False
    cone_beam_ct_kv_positioning_repositioning_less_than_2mm: bool = False
    cone_beam_ct_kv_geometric_distortion_1_mm: bool = False
    cone_beam_ct_kv_baseline_spatial_resolution: bool = False
    cone_beam_ct_kv_baseline_contrast: bool = False
    cone_beam_ct_kv_baseline_noise_and_uniformity: bool = False
    cone_beam_ct_kv_baseline_hu_constancy: bool = False
    realized_by_id: int | None = Field(foreign_key="user.id")
    observation: str

class TestMonthly(TestMonthlyBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

