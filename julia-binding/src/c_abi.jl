# ============================================================================
# C-ABI DEFINITIONS (Direct In-Process Julia `ccall` Bindings)
# ============================================================================

struct NwauAbiStringView
    ptr::Ptr{Cchar}
    len::Csize_t
end

NwauAbiStringView(s::AbstractString) = NwauAbiStringView(pointer(s), sizeof(s))
NwauAbiStringView() = NwauAbiStringView(C_NULL, 0)

function Base.String(sv::NwauAbiStringView)
    sv.ptr == C_NULL || sv.len == 0 ? "" : unsafe_string(sv.ptr, sv.len)
end

function _find_libnwau_c_abi()
    if haskey(ENV, "LIBNWAU_C_ABI_PATH") && isfile(ENV["LIBNWAU_C_ABI_PATH"])
        return ENV["LIBNWAU_C_ABI_PATH"]
    end
    root = normpath(joinpath(@__DIR__, "..", ".."))
    candidates = [
        joinpath(root, "rust", "target", "debug", "libnwau_c_abi.dylib"),
        joinpath(root, "rust", "target", "release", "libnwau_c_abi.dylib"),
        joinpath(root, "rust", "target", "debug", "libnwau_c_abi.so"),
        joinpath(root, "rust", "target", "release", "libnwau_c_abi.so"),
        joinpath(root, "rust", "target", "debug", "nwau_c_abi.dll"),
        joinpath(root, "rust", "target", "release", "nwau_c_abi.dll"),
    ]
    for c in candidates
        if isfile(c)
            return c
        end
    end
    return "libnwau_c_abi"
end

const _LIB_HANDLES = Dict{String, Ptr{Cvoid}}()

function _get_lib_handle(libpath::String=_find_libnwau_c_abi())
    get!(_LIB_HANDLES, libpath) do
        Libdl.dlopen(libpath)
    end
end

function _get_fn_ptr(sym::Symbol, libpath::String=_find_libnwau_c_abi())
    Libdl.dlsym(_get_lib_handle(libpath), sym)
end

# 1. ACUTE
struct NwauAbiEpisodeInput
    drg::NwauAbiStringView
    los::Cdouble
    icu_hours::Cdouble
    icu_other::Cdouble
    pat_sameday_flag::UInt8
    pat_private_flag::UInt8
    pat_covid_flag::UInt8
    eligible_paed_flag::UInt8
end

struct NwauAbiReferenceRow
    drg::NwauAbiStringView
    inlier_lower_bound::Cdouble
    inlier_upper_bound::Cdouble
    paediatric_multiplier::Cdouble
    same_day_list_flag::UInt8
    bundled_icu_flag::UInt8
    same_day_base_weight::Cdouble
    same_day_per_diem::Cdouble
    inlier_weight::Cdouble
    long_stay_per_diem::Cdouble
    private_service_adjustment::Cdouble
end

struct NwauAbiAdjustmentFactors
    icu_rate::Cdouble
    covid_adjustment::Cdouble
    indigenous_adjustment::Cdouble
    remoteness_adjustment::Cdouble
    treatment_remoteness_adjustment::Cdouble
    radiotherapy_adjustment::Cdouble
    dialysis_adjustment::Cdouble
    private_accommodation_same_day::Cdouble
    private_accommodation_overnight::Cdouble
end

struct NwauAbiEpisodeOutput
    error_code::UInt32
    separation_category::UInt32
    eligible_icu_hours::Cdouble
    los_icu_removed::Cdouble
    w01::Cdouble
    w02::Cdouble
    w03::Cdouble
    w04::Cdouble
    gwau::Cdouble
    private_service_deduction::Cdouble
    private_accommodation_deduction::Cdouble
    nwau25::Cdouble
end

function calculate_acute_c_abi(
    input::NwauAbiEpisodeInput,
    reference::NwauAbiReferenceRow,
    adjustments::NwauAbiAdjustmentFactors;
    libpath=_find_libnwau_c_abi(),
)
    fn = _get_fn_ptr(:nwau_abi_calculate_acute_2025, libpath)
    out = Ref{NwauAbiEpisodeOutput}()
    status = ccall(
        fn,
        UInt32,
        (Ref{NwauAbiEpisodeInput}, Ref{NwauAbiReferenceRow}, Ref{NwauAbiAdjustmentFactors}, Ref{NwauAbiEpisodeOutput}),
        input,
        reference,
        adjustments,
        out,
    )
    if status != 0
        error("nwau_abi_calculate_acute_2025 failed with status code $status")
    end
    return out[]
end

# 2. EMERGENCY DEPARTMENT (ED)
struct NwauAbiEdInput
    code::NwauAbiStringView
    classification_option::UInt32
    eligibility_option::UInt32
    compensable_status::UInt32
    dva_status::UInt32
    funding_source::UInt32
    indigenous_adjustment::Cdouble
    remoteness_adjustment::Cdouble
    treatment_remoteness_adjustment::Cdouble
end

struct NwauAbiEdReferenceRow
    code::NwauAbiStringView
    price_weight::Cdouble
end

struct NwauAbiEdOutput
    error_code::UInt32
    w01::Cdouble
    gwau::Cdouble
    nwau::Cdouble
end

function calculate_ed_c_abi(
    input::NwauAbiEdInput,
    reference::NwauAbiEdReferenceRow;
    libpath=_find_libnwau_c_abi(),
)
    fn = _get_fn_ptr(:nwau_abi_calculate_ed, libpath)
    out = Ref{NwauAbiEdOutput}()
    status = ccall(
        fn,
        UInt32,
        (Ref{NwauAbiEdInput}, Ref{NwauAbiEdReferenceRow}, Ref{NwauAbiEdOutput}),
        input,
        reference,
        out,
    )
    if status != 0
        error("nwau_abi_calculate_ed failed with status code $status")
    end
    return out[]
end

# 3. MENTAL HEALTH
struct NwauAbiMhInput
    amhcc::NwauAbiStringView
    los::Cdouble
    pat_sameday_flag::UInt8
    pat_private_flag::UInt8
    state::UInt8
    sc_pat_pub::Cdouble
    sc_nopat_pub::Cdouble
    specialist_paediatric_multiplier::Cdouble
    indigenous_adjustment::Cdouble
    remoteness_adjustment::Cdouble
    treatment_remoteness_adjustment::Cdouble
    private_serv_rate_national::Cdouble
    private_serv_rate_state::Cdouble
    private_accomm_sameday::Cdouble
    private_accomm_overnight::Cdouble
    ppsa_option::UInt32
end

struct NwauAbiMhAdmittedReferenceRow
    amhcc::NwauAbiStringView
    price_cat::UInt32
    inlier_lower_bound::Cdouble
    inlier_upper_bound::Cdouble
    sso_base_weight::Cdouble
    sso_per_diem::Cdouble
    inlier_weight::Cdouble
    lso_per_diem::Cdouble
end

struct NwauAbiMhOutput
    error_code::UInt32
    substream::UInt32
    separation_category::UInt32
    w01::Cdouble
    gwau::Cdouble
    private_service_deduction::Cdouble
    private_accommodation_deduction::Cdouble
    nwau::Cdouble
end

function calculate_mh_c_abi(
    input::NwauAbiMhInput,
    reference::NwauAbiMhAdmittedReferenceRow;
    libpath=_find_libnwau_c_abi(),
)
    fn = _get_fn_ptr(:nwau_abi_calculate_mh, libpath)
    out = Ref{NwauAbiMhOutput}()
    status = ccall(
        fn,
        UInt32,
        (Ref{NwauAbiMhInput}, Ref{NwauAbiMhAdmittedReferenceRow}, Ref{NwauAbiMhOutput}),
        input,
        reference,
        out,
    )
    if status != 0
        error("nwau_abi_calculate_mh failed with status code $status")
    end
    return out[]
end

# 4. OUTPATIENTS
struct NwauAbiOutpatientInput
    clinic_code::NwauAbiStringView
    data_type::UInt32
    multiprovider_flag::UInt8
    eligible_paediatric_flag::UInt8
    inscope_flag::UInt8
    group_event_count::Cdouble
    indiv_event_count::Cdouble
    multidisciplinary_event_count::Cdouble
    indigenous_adjustment::Cdouble
    remoteness_adjustment::Cdouble
    treatment_remoteness_adjustment::Cdouble
    multiprovider_adjustment::Cdouble
    paediatric_adjustment::Cdouble
end

struct NwauAbiOutpatientReferenceRow
    clinic_code::NwauAbiStringView
    price_weight::Cdouble
    paediatric_adjustment::Cdouble
end

struct NwauAbiOutpatientOutput
    error_code::UInt32
    w01::Cdouble
    gwau::Cdouble
    nwau::Cdouble
end

function calculate_outpatients_c_abi(
    input::NwauAbiOutpatientInput,
    reference::NwauAbiOutpatientReferenceRow;
    libpath=_find_libnwau_c_abi(),
)
    fn = _get_fn_ptr(:nwau_abi_calculate_outpatients, libpath)
    out = Ref{NwauAbiOutpatientOutput}()
    status = ccall(
        fn,
        UInt32,
        (Ref{NwauAbiOutpatientInput}, Ref{NwauAbiOutpatientReferenceRow}, Ref{NwauAbiOutpatientOutput}),
        input,
        reference,
        out,
    )
    if status != 0
        error("nwau_abi_calculate_outpatients failed with status code $status")
    end
    return out[]
end

# 5. SUBACUTE
struct NwauAbiSubacuteInput
    ansnap::NwauAbiStringView
    los::Cdouble
    pat_sameday_flag::UInt8
    pat_private_flag::UInt8
    pat_public_flag::UInt8
    age::Cdouble
    state::UInt8
    indigenous_adjustment::Cdouble
    remoteness_adjustment::Cdouble
    treatment_remoteness_adjustment::Cdouble
    radiotherapy_adjustment::Cdouble
    dialysis_adjustment::Cdouble
    private_serv_rate_national::Cdouble
    private_serv_rate_state::Cdouble
    private_accomm_sameday::Cdouble
    private_accomm_overnight::Cdouble
    ppsa_option::UInt32
end

struct NwauAbiSubacuteReferenceRow
    ansnap::NwauAbiStringView
    sameday_list_flag::UInt8
    inlier_lower_bound::Cdouble
    inlier_upper_bound::Cdouble
    pw_sameday::Cdouble
    pw_sso_perdiem::Cdouble
    pw_inlier::Cdouble
    pw_lso_perdiem::Cdouble
end

struct NwauAbiSubacuteOutput
    error_code::UInt32
    separation_category::UInt32
    w01::Cdouble
    gwau::Cdouble
    private_service_deduction::Cdouble
    private_accommodation_deduction::Cdouble
    nwau::Cdouble
end

function calculate_subacute_c_abi(
    input::NwauAbiSubacuteInput,
    reference::NwauAbiSubacuteReferenceRow;
    libpath=_find_libnwau_c_abi(),
)
    fn = _get_fn_ptr(:nwau_abi_calculate_subacute, libpath)
    out = Ref{NwauAbiSubacuteOutput}()
    status = ccall(
        fn,
        UInt32,
        (Ref{NwauAbiSubacuteInput}, Ref{NwauAbiSubacuteReferenceRow}, Ref{NwauAbiSubacuteOutput}),
        input,
        reference,
        out,
    )
    if status != 0
        error("nwau_abi_calculate_subacute failed with status code $status")
    end
    return out[]
end

# ============================================================================
# MEMORY-MAPPED / VECTORIZED BATCH VALUATION FOR JULIA TABLES / DATAFRAMES
# ============================================================================

"""
    calculate_batch_c_abi(stream, table; libpath)

Evaluate NWAU in a zero-allocation, vectorized loop using in-process C-ABI calls directly
from Julia column vectors (supporting DataFrames, Arrow.Table, or NamedTuples).
"""
function calculate_batch_c_abi(
    stream::Symbol,
    table;
    libpath=_find_libnwau_c_abi(),
)
    if stream === :ed
        n = length(table.price_weight)
        res = Vector{Float64}(undef, n)
        for i in 1:n
            code_str = hasproperty(table, :code) ? string(table.code[i]) : ""
            input = NwauAbiEdInput(
                NwauAbiStringView(code_str),
                hasproperty(table, :classification_option) ? UInt32(table.classification_option[i]) : UInt32(3),
                hasproperty(table, :eligibility_option) ? UInt32(table.eligibility_option[i]) : UInt32(1),
                hasproperty(table, :compensable_status) ? UInt32(table.compensable_status[i]) : UInt32(2),
                hasproperty(table, :dva_status) ? UInt32(table.dva_status[i]) : UInt32(2),
                hasproperty(table, :funding_source) ? UInt32(table.funding_source[i]) : UInt32(0),
                hasproperty(table, :indigenous_adjustment) ? Float64(table.indigenous_adjustment[i]) : 0.0,
                hasproperty(table, :remoteness_adjustment) ? Float64(table.remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :treatment_remoteness_adjustment) ? Float64(table.treatment_remoteness_adjustment[i]) : 0.0,
            )
            ref = NwauAbiEdReferenceRow(
                NwauAbiStringView(code_str),
                Float64(table.price_weight[i]),
            )
            out = calculate_ed_c_abi(input, ref; libpath=libpath)
            res[i] = out.nwau
        end
        return res
    elseif stream === :acute
        n = length(table.los)
        res = Vector{Float64}(undef, n)
        for i in 1:n
            drg_str = hasproperty(table, :drg) ? string(table.drg[i]) : ""
            input = NwauAbiEpisodeInput(
                NwauAbiStringView(drg_str),
                Float64(table.los[i]),
                hasproperty(table, :icu_hours) ? Float64(table.icu_hours[i]) : 0.0,
                hasproperty(table, :icu_other) ? Float64(table.icu_other[i]) : 0.0,
                hasproperty(table, :pat_sameday_flag) ? UInt8(table.pat_sameday_flag[i]) : UInt8(0),
                hasproperty(table, :pat_private_flag) ? UInt8(table.pat_private_flag[i]) : UInt8(0),
                hasproperty(table, :pat_covid_flag) ? UInt8(table.pat_covid_flag[i]) : UInt8(0),
                hasproperty(table, :eligible_paed_flag) ? UInt8(table.eligible_paed_flag[i]) : UInt8(0),
            )
            ref = NwauAbiReferenceRow(
                NwauAbiStringView(drg_str),
                hasproperty(table, :inlier_lower_bound) ? Float64(table.inlier_lower_bound[i]) : 0.0,
                hasproperty(table, :inlier_upper_bound) ? Float64(table.inlier_upper_bound[i]) : 0.0,
                hasproperty(table, :paediatric_multiplier) ? Float64(table.paediatric_multiplier[i]) : 1.0,
                hasproperty(table, :same_day_list_flag) ? UInt8(table.same_day_list_flag[i]) : UInt8(0),
                hasproperty(table, :bundled_icu_flag) ? UInt8(table.bundled_icu_flag[i]) : UInt8(0),
                hasproperty(table, :same_day_base_weight) ? Float64(table.same_day_base_weight[i]) : 0.0,
                hasproperty(table, :same_day_per_diem) ? Float64(table.same_day_per_diem[i]) : 0.0,
                hasproperty(table, :inlier_weight) ? Float64(table.inlier_weight[i]) : 0.0,
                hasproperty(table, :long_stay_per_diem) ? Float64(table.long_stay_per_diem[i]) : 0.0,
                hasproperty(table, :private_service_adjustment) ? Float64(table.private_service_adjustment[i]) : 0.0,
            )
            adj = NwauAbiAdjustmentFactors(
                hasproperty(table, :icu_rate) ? Float64(table.icu_rate[i]) : 0.0,
                hasproperty(table, :covid_adjustment) ? Float64(table.covid_adjustment[i]) : 0.0,
                hasproperty(table, :indigenous_adjustment) ? Float64(table.indigenous_adjustment[i]) : 0.0,
                hasproperty(table, :remoteness_adjustment) ? Float64(table.remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :treatment_remoteness_adjustment) ? Float64(table.treatment_remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :radiotherapy_adjustment) ? Float64(table.radiotherapy_adjustment[i]) : 0.0,
                hasproperty(table, :dialysis_adjustment) ? Float64(table.dialysis_adjustment[i]) : 0.0,
                hasproperty(table, :private_accommodation_same_day) ? Float64(table.private_accommodation_same_day[i]) : 0.0,
                hasproperty(table, :private_accommodation_overnight) ? Float64(table.private_accommodation_overnight[i]) : 0.0,
            )
            out = calculate_acute_c_abi(input, ref, adj; libpath=libpath)
            res[i] = out.nwau25
        end
        return res
    elseif stream === :outpatients
        n = length(table.price_weight)
        res = Vector{Float64}(undef, n)
        for i in 1:n
            clinic_str = hasproperty(table, :clinic_code) ? string(table.clinic_code[i]) : ""
            input = NwauAbiOutpatientInput(
                NwauAbiStringView(clinic_str),
                hasproperty(table, :data_type) ? UInt32(table.data_type[i]) : UInt32(0),
                hasproperty(table, :multiprovider_flag) ? UInt8(table.multiprovider_flag[i]) : UInt8(0),
                hasproperty(table, :eligible_paediatric_flag) ? UInt8(table.eligible_paediatric_flag[i]) : UInt8(0),
                hasproperty(table, :inscope_flag) ? UInt8(table.inscope_flag[i]) : UInt8(1),
                hasproperty(table, :group_event_count) ? Float64(table.group_event_count[i]) : 0.0,
                hasproperty(table, :indiv_event_count) ? Float64(table.indiv_event_count[i]) : 1.0,
                hasproperty(table, :multidisciplinary_event_count) ? Float64(table.multidisciplinary_event_count[i]) : 0.0,
                hasproperty(table, :indigenous_adjustment) ? Float64(table.indigenous_adjustment[i]) : 0.0,
                hasproperty(table, :remoteness_adjustment) ? Float64(table.remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :treatment_remoteness_adjustment) ? Float64(table.treatment_remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :multiprovider_adjustment) ? Float64(table.multiprovider_adjustment[i]) : 0.0,
                hasproperty(table, :paediatric_adjustment) ? Float64(table.paediatric_adjustment[i]) : 0.0,
            )
            ref = NwauAbiOutpatientReferenceRow(
                NwauAbiStringView(clinic_str),
                Float64(table.price_weight[i]),
                hasproperty(table, :paediatric_adjustment) ? Float64(table.paediatric_adjustment[i]) : 0.0,
            )
            out = calculate_outpatients_c_abi(input, ref; libpath=libpath)
            res[i] = out.nwau
        end
        return res
    elseif stream === :subacute
        n = length(table.ansnap)
        res = Vector{Float64}(undef, n)
        for i in 1:n
            ansnap_str = string(table.ansnap[i])
            input = NwauAbiSubacuteInput(
                NwauAbiStringView(ansnap_str),
                Float64(table.los[i]),
                hasproperty(table, :pat_sameday_flag) ? UInt8(table.pat_sameday_flag[i]) : UInt8(0),
                hasproperty(table, :pat_private_flag) ? UInt8(table.pat_private_flag[i]) : UInt8(0),
                hasproperty(table, :pat_public_flag) ? UInt8(table.pat_public_flag[i]) : UInt8(1),
                hasproperty(table, :age) ? Float64(table.age[i]) : 50.0,
                hasproperty(table, :state) ? UInt8(table.state[i]) : UInt8(1),
                hasproperty(table, :indigenous_adjustment) ? Float64(table.indigenous_adjustment[i]) : 0.0,
                hasproperty(table, :remoteness_adjustment) ? Float64(table.remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :treatment_remoteness_adjustment) ? Float64(table.treatment_remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :radiotherapy_adjustment) ? Float64(table.radiotherapy_adjustment[i]) : 0.0,
                hasproperty(table, :dialysis_adjustment) ? Float64(table.dialysis_adjustment[i]) : 0.0,
                hasproperty(table, :private_serv_rate_national) ? Float64(table.private_serv_rate_national[i]) : 0.0,
                hasproperty(table, :private_serv_rate_state) ? Float64(table.private_serv_rate_state[i]) : 0.0,
                hasproperty(table, :private_accomm_sameday) ? Float64(table.private_accomm_sameday[i]) : 0.0,
                hasproperty(table, :private_accomm_overnight) ? Float64(table.private_accomm_overnight[i]) : 0.0,
                hasproperty(table, :ppsa_option) ? UInt32(table.ppsa_option[i]) : UInt32(0),
            )
            ref = NwauAbiSubacuteReferenceRow(
                NwauAbiStringView(ansnap_str),
                hasproperty(table, :sameday_list_flag) ? UInt8(table.sameday_list_flag[i]) : UInt8(0),
                hasproperty(table, :inlier_lower_bound) ? Float64(table.inlier_lower_bound[i]) : 0.0,
                hasproperty(table, :inlier_upper_bound) ? Float64(table.inlier_upper_bound[i]) : 0.0,
                hasproperty(table, :pw_sameday) ? Float64(table.pw_sameday[i]) : 0.0,
                hasproperty(table, :pw_sso_perdiem) ? Float64(table.pw_sso_perdiem[i]) : 0.0,
                hasproperty(table, :pw_inlier) ? Float64(table.pw_inlier[i]) : 0.0,
                hasproperty(table, :pw_lso_perdiem) ? Float64(table.pw_lso_perdiem[i]) : 0.0,
            )
            out = calculate_subacute_c_abi(input, ref; libpath=libpath)
            res[i] = out.nwau
        end
        return res
    elseif stream === :mh
        n = length(table.amhcc)
        res = Vector{Float64}(undef, n)
        for i in 1:n
            amhcc_str = string(table.amhcc[i])
            input = NwauAbiMhInput(
                NwauAbiStringView(amhcc_str),
                Float64(table.los[i]),
                hasproperty(table, :pat_sameday_flag) ? UInt8(table.pat_sameday_flag[i]) : UInt8(0),
                hasproperty(table, :pat_private_flag) ? UInt8(table.pat_private_flag[i]) : UInt8(0),
                hasproperty(table, :state) ? UInt8(table.state[i]) : UInt8(1),
                hasproperty(table, :sc_pat_pub) ? Float64(table.sc_pat_pub[i]) : 0.0,
                hasproperty(table, :sc_nopat_pub) ? Float64(table.sc_nopat_pub[i]) : 0.0,
                hasproperty(table, :specialist_paediatric_multiplier) ? Float64(table.specialist_paediatric_multiplier[i]) : 1.0,
                hasproperty(table, :indigenous_adjustment) ? Float64(table.indigenous_adjustment[i]) : 0.0,
                hasproperty(table, :remoteness_adjustment) ? Float64(table.remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :treatment_remoteness_adjustment) ? Float64(table.treatment_remoteness_adjustment[i]) : 0.0,
                hasproperty(table, :private_serv_rate_national) ? Float64(table.private_serv_rate_national[i]) : 0.0,
                hasproperty(table, :private_serv_rate_state) ? Float64(table.private_serv_rate_state[i]) : 0.0,
                hasproperty(table, :private_accomm_sameday) ? Float64(table.private_accomm_sameday[i]) : 0.0,
                hasproperty(table, :private_accomm_overnight) ? Float64(table.private_accomm_overnight[i]) : 0.0,
                hasproperty(table, :ppsa_option) ? UInt32(table.ppsa_option[i]) : UInt32(0),
            )
            ref = NwauAbiMhAdmittedReferenceRow(
                NwauAbiStringView(amhcc_str),
                hasproperty(table, :price_cat) ? UInt32(table.price_cat[i]) : UInt32(1),
                hasproperty(table, :inlier_lower_bound) ? Float64(table.inlier_lower_bound[i]) : 0.0,
                hasproperty(table, :inlier_upper_bound) ? Float64(table.inlier_upper_bound[i]) : 0.0,
                hasproperty(table, :sso_base_weight) ? Float64(table.sso_base_weight[i]) : 0.0,
                hasproperty(table, :sso_per_diem) ? Float64(table.sso_per_diem[i]) : 0.0,
                hasproperty(table, :inlier_weight) ? Float64(table.inlier_weight[i]) : 0.0,
                hasproperty(table, :lso_per_diem) ? Float64(table.lso_per_diem[i]) : 0.0,
            )
            out = calculate_mh_c_abi(input, ref; libpath=libpath)
            res[i] = out.nwau
        end
        return res
    else
        error("Unsupported batch valuation stream: $stream")
    end
end
