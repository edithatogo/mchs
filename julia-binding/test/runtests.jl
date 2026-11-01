using Test
using NationalWeightedActivityUnitWrapper

@testset "command assembly" begin
    adapter = CliFileAdapter(python = "python", cli_module = "nwau_py.cli.main")
    argv = NationalWeightedActivityUnitWrapper._build_argv(
        "acute";
        input_csv = "input.csv",
        output_csv = "output.csv",
        year = 2025,
        params_dir = "archive/sas/2025",
        adapter = adapter,
    )

    @test argv == [
        "python",
        "-m",
        "nwau_py.cli.main",
        "acute",
        "input.csv",
        "--output",
        "output.csv",
        "--params",
        "archive/sas/2025",
        "--year",
        "2025",
    ]
end

@testset "contract command assembly" begin
    adapter = CliFileAdapter(python = "python", cli_module = "nwau_py.cli.main")
    @test NationalWeightedActivityUnitWrapper._build_contract_argv(adapter) == [
        "python",
        "-m",
        "nwau_py.cli.main",
        "interop",
        "contract",
    ]
end

@testset "missing input guard" begin
    @test_throws ArgumentError calculate(
        "acute";
        input_csv = "does-not-exist.csv",
        output_csv = "out.csv",
    )
end

@testset "unsupported command guard" begin
    @test_throws ArgumentError NationalWeightedActivityUnitWrapper._build_argv(
        "made-up";
        input_csv = "input.csv",
        output_csv = "output.csv",
    )
end

@testset "cli result captures success and diagnostics" begin
    script = tempname()
    input_csv = tempname() * ".csv"
    output_csv = tempname() * ".csv"
    write(input_csv, "case_id,value\n1,2\n")
    write(
        script,
        """
        #!/usr/bin/env sh
        set -eu
        test "\$1" = "-m"
        test "\$2" = "nwau_py.cli.main"
        test "\$3" = "acute"
        test "\$5" = "--output"
        cp "\$4" "\$6"
        echo delegated
        echo diagnostic >&2
        """,
    )
    chmod(script, 0o755)

    adapter = CliFileAdapter(python = script, cli_module = "nwau_py.cli.main")
    result = calculate(
        "acute";
        input_csv = input_csv,
        output_csv = output_csv,
        adapter = adapter,
    )

    @test result isa CalculationResult
    @test result.success
    @test result.exit_code == 0
    @test result.output_csv == output_csv
    @test isfile(output_csv)
    @test read(output_csv, String) == read(input_csv, String)
    @test occursin("delegated", result.stdout)
    @test occursin("diagnostic", result.stderr)
end

@testset "service request guard" begin
    adapter = ServiceAdapter("http://127.0.0.1:1")
    @test_throws ArgumentError execute_service_request(
        adapter;
        request_json = "does-not-exist.json",
    )
end

@testset "c-abi acute calculation" begin
    input = NwauAbiEpisodeInput(
        NwauAbiStringView("801A"),
        10.0,
        0.0,
        0.0,
        0,
        0,
        0,
        0,
    )
    ref = NwauAbiReferenceRow(
        NwauAbiStringView("801A"),
        8.0,
        35.0,
        1.0,
        0,
        0,
        0.8654,
        0.2885,
        9.2472,
        0.2642,
        0.0,
    )
    adj = NwauAbiAdjustmentFactors(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    out = calculate_acute_c_abi(input, ref, adj)
    @test out.error_code == 0
    @test isapprox(out.nwau25, 9.2472; atol=1e-4)
end

@testset "c-abi emergency department calculation" begin
    input = NwauAbiEdInput(
        NwauAbiStringView("E0110A"),
        UInt32(3),
        UInt32(1),
        UInt32(2),
        UInt32(2),
        UInt32(0),
        0.0,
        0.0,
        0.0,
    )
    ref = NwauAbiEdReferenceRow(
        NwauAbiStringView("E0110A"),
        0.2837,
    )
    out = calculate_ed_c_abi(input, ref)
    @test out.error_code == 0
    @test isapprox(out.nwau, 0.2837; atol=1e-4)
end

@testset "c-abi mental health admitted calculation" begin
    input = NwauAbiMhInput(
        NwauAbiStringView("101A"),
        5.0,
        UInt8(0),
        UInt8(0),
        UInt8(1),
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        UInt32(0),
    )
    ref = NwauAbiMhAdmittedReferenceRow(
        NwauAbiStringView("101A"),
        UInt32(1),
        2.0,
        10.0,
        0.5,
        0.1,
        1.2345,
        0.08,
    )
    out = calculate_mh_c_abi(input, ref)
    @test out.error_code == 0
    @test isapprox(out.nwau, 1.2345; atol=1e-4)
end

@testset "c-abi outpatients calculation" begin
    input = NwauAbiOutpatientInput(
        NwauAbiStringView("10.01"),
        UInt32(1),
        UInt8(0),
        UInt8(0),
        UInt8(1),
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
    )
    ref = NwauAbiOutpatientReferenceRow(
        NwauAbiStringView("10.01"),
        0.1742,
        1.0,
    )
    out = calculate_outpatients_c_abi(input, ref)
    @test out.error_code == 0
    @test isapprox(out.nwau, 0.1742; atol=1e-4)
end

@testset "c-abi subacute calculation" begin
    input = NwauAbiSubacuteInput(
        NwauAbiStringView("5AA1"),
        10.0,
        UInt8(0),
        UInt8(0),
        UInt8(1),
        65.0,
        UInt8(1),
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        UInt32(0),
    )
    ref = NwauAbiSubacuteReferenceRow(
        NwauAbiStringView("5AA1"),
        UInt8(0),
        3.0,
        20.0,
        0.2,
        0.05,
        1.854,
        0.09,
    )
    out = calculate_subacute_c_abi(input, ref)
    @test out.error_code == 0
    @test isapprox(out.nwau, 1.854; atol=1e-4)
end

@testset "c-abi batch tabular evaluation" begin
    # ED batch table
    ed_table = (
        code = ["E0110A", "E0110B"],
        price_weight = [0.2837, 0.1542],
        classification_option = [3, 3],
        eligibility_option = [1, 1],
        compensable_status = [2, 2],
        dva_status = [2, 2],
    )
    ed_nwau = calculate_batch_c_abi(:ed, ed_table)
    @test length(ed_nwau) == 2
    @test isapprox(ed_nwau[1], 0.2837; atol=1e-4)
    @test isapprox(ed_nwau[2], 0.1542; atol=1e-4)

    # Acute batch table
    acute_table = (
        drg = ["801A"],
        los = [10.0],
        inlier_lower_bound = [8.0],
        inlier_upper_bound = [35.0],
        paediatric_multiplier = [1.0],
        same_day_list_flag = [0],
        bundled_icu_flag = [0],
        same_day_base_weight = [0.8654],
        same_day_per_diem = [0.2885],
        inlier_weight = [9.2472],
        long_stay_per_diem = [0.2642],
        private_service_adjustment = [0.0],
    )
    acute_nwau = calculate_batch_c_abi(:acute, acute_table)
    @test length(acute_nwau) == 1
    @test isapprox(acute_nwau[1], 9.2472; atol=1e-4)

    # Outpatients batch table
    op_table = (
        clinic_code = ["10.01"],
        price_weight = [0.1742],
        data_type = [1],
        inscope_flag = [1],
        paediatric_adjustment = [1.0],
    )
    op_nwau = calculate_batch_c_abi(:outpatients, op_table)
    @test length(op_nwau) == 1
    @test isapprox(op_nwau[1], 0.1742; atol=1e-4)

    # Subacute batch table
    subacute_table = (
        ansnap = ["5AA1"],
        los = [10.0],
        pw_inlier = [1.854],
        inlier_lower_bound = [3.0],
        inlier_upper_bound = [20.0],
        age = [65.0],
    )
    subacute_nwau = calculate_batch_c_abi(:subacute, subacute_table)
    @test length(subacute_nwau) == 1
    @test isapprox(subacute_nwau[1], 1.854; atol=1e-4)

    # Mental Health batch table
    mh_table = (
        amhcc = ["101A"],
        los = [5.0],
        inlier_weight = [1.2345],
        inlier_lower_bound = [2.0],
        inlier_upper_bound = [10.0],
        price_cat = [1],
    )
    mh_nwau = calculate_batch_c_abi(:mh, mh_table)
    @test length(mh_nwau) == 1
    @test isapprox(mh_nwau[1], 1.2345; atol=1e-4)
end
