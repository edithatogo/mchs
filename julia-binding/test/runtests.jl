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
