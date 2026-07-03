module NationalWeightedActivityUnitWrapper

using Downloads

export CliFileAdapter,
    ServiceAdapter,
    CalculationResult,
    ServiceResult,
    calculate,
    calculate_acute,
    calculate_ed,
    calculate_non_admitted,
    interop_contract,
    execute_service_request

const DEFAULT_PYTHON = get(ENV, "NWAU_PYTHON", "python3")
const DEFAULT_MODULE = get(ENV, "NWAU_MODULE", "nwau_py.cli.main")
const SUPPORTED_FILE_COMMANDS = Set(["acute", "ed", "non-admitted"])

"""
    CliFileAdapter(; python, cli_module)

Boundary adapter for the shared CLI/file contract. It only owns process
execution and file handoff; formula logic remains in the shared core.
"""
struct CliFileAdapter
    python::String
    cli_module::String
end

CliFileAdapter(; python::AbstractString=DEFAULT_PYTHON, cli_module::AbstractString=DEFAULT_MODULE) =
    CliFileAdapter(String(python), String(cli_module))

"""
    ServiceAdapter(url; timeout=30)

Transport-only adapter for service-backed binding experiments. Request and
response bodies are opaque JSON files so Julia does not duplicate domain logic.
"""
struct ServiceAdapter
    url::String
    timeout::Real
end

ServiceAdapter(url::AbstractString; timeout::Real=30) = ServiceAdapter(String(url), timeout)

struct CalculationResult
    success::Bool
    exit_code::Int
    command::Vector{String}
    input_csv::String
    output_csv::String
    stdout::String
    stderr::String
end

struct ServiceResult
    success::Bool
    status::Int
    request_json::String
    response_json::String
end

function _build_argv(
    subcommand::AbstractString;
    input_csv::AbstractString,
    output_csv::AbstractString,
    year::Union{Nothing,AbstractString,Integer}=nothing,
    params_dir::Union{Nothing,AbstractString}=nothing,
    adapter::CliFileAdapter=CliFileAdapter(),
)
    _validate_file_command(subcommand)
    argv = String[
        adapter.python,
        "-m",
        adapter.cli_module,
        subcommand,
        input_csv,
        "--output",
        output_csv,
    ]
    if params_dir !== nothing
        push!(argv, "--params", String(params_dir))
    end
    if year !== nothing
        push!(argv, "--year", string(year))
    end
    return argv
end

function _build_contract_argv(adapter::CliFileAdapter=CliFileAdapter())
    return String[adapter.python, "-m", adapter.cli_module, "interop", "contract"]
end

function _validate_file_command(subcommand::AbstractString)
    command = String(subcommand)
    if !(command in SUPPORTED_FILE_COMMANDS)
        supported = join(sort(collect(SUPPORTED_FILE_COMMANDS)), ", ")
        throw(ArgumentError("unsupported calculator command: $command; expected one of: $supported"))
    end
    return command
end

function _resolve_output_path(output_csv::Union{Nothing,AbstractString})
    if output_csv === nothing
        return tempname() * ".csv"
    end
    return String(output_csv)
end

function _ensure_parent_dir(path::AbstractString)
    parent = dirname(String(path))
    if !isempty(parent)
        mkpath(parent)
    end
end

function _read_or_empty(path::AbstractString)
    if isfile(path)
        return read(path, String)
    end
    return ""
end

function _run_boundary_command(argv::Vector{String}; input_csv::AbstractString="", output_csv::AbstractString="")
    stdout_path = tempname()
    stderr_path = tempname()
    process = run(
        pipeline(ignorestatus(Cmd(argv)); stdout=stdout_path, stderr=stderr_path),
        wait=true,
    )
    stdout = _read_or_empty(stdout_path)
    stderr = _read_or_empty(stderr_path)
    rm(stdout_path; force=true)
    rm(stderr_path; force=true)

    return CalculationResult(
        process.exitcode == 0,
        process.exitcode,
        copy(argv),
        String(input_csv),
        String(output_csv),
        stdout,
        stderr,
    )
end

function _require_success(result::CalculationResult)
    if !result.success
        detail = isempty(strip(result.stderr)) ? strip(result.stdout) : strip(result.stderr)
        if isempty(detail)
            detail = "shared core CLI exited with code $(result.exit_code)"
        end
        throw(ErrorException(detail))
    end
    return result
end

function calculate(
    subcommand::AbstractString;
    input_csv::AbstractString,
    output_csv::Union{Nothing,AbstractString}=nothing,
    year::Union{Nothing,AbstractString,Integer}=nothing,
    params_dir::Union{Nothing,AbstractString}=nothing,
    adapter::CliFileAdapter=CliFileAdapter(),
    check::Bool=true,
)
    _validate_file_command(subcommand)
    input_path = abspath(String(input_csv))
    isfile(input_path) || throw(ArgumentError("input CSV not found: $input_path"))

    output_path = _resolve_output_path(output_csv)
    _ensure_parent_dir(output_path)

    argv = _build_argv(
        subcommand;
        input_csv=input_path,
        output_csv=output_path,
        year=year,
        params_dir=params_dir,
        adapter=adapter,
    )
    result = _run_boundary_command(argv; input_csv=input_path, output_csv=output_path)
    if check
        _require_success(result)
    end
    return result
end

function calculate_acute(; kwargs...)
    return calculate("acute"; kwargs...)
end

function calculate_acute(input_csv::AbstractString; kwargs...)
    return calculate("acute"; input_csv=input_csv, kwargs...)
end

function calculate_ed(; kwargs...)
    return calculate("ed"; kwargs...)
end

function calculate_ed(input_csv::AbstractString; kwargs...)
    return calculate("ed"; input_csv=input_csv, kwargs...)
end

function calculate_non_admitted(; kwargs...)
    return calculate("non-admitted"; kwargs...)
end

function calculate_non_admitted(input_csv::AbstractString; kwargs...)
    return calculate("non-admitted"; input_csv=input_csv, kwargs...)
end

function interop_contract(;
    output_json::Union{Nothing,AbstractString}=nothing,
    adapter::CliFileAdapter=CliFileAdapter(),
    check::Bool=true,
)
    argv = _build_contract_argv(adapter)
    result = _run_boundary_command(argv)
    if check
        _require_success(result)
    end
    if output_json !== nothing
        output_path = String(output_json)
        _ensure_parent_dir(output_path)
        write(output_path, result.stdout)
    end
    return result
end

function execute_service_request(
    adapter::ServiceAdapter;
    request_json::AbstractString,
    response_json::Union{Nothing,AbstractString}=nothing,
    headers::Vector{Pair{String,String}}=Pair{String,String}[],
)
    request_path = abspath(String(request_json))
    isfile(request_path) || throw(ArgumentError("service request JSON not found: $request_path"))

    response_path = response_json === nothing ? tempname() * ".json" : String(response_json)
    _ensure_parent_dir(response_path)

    request_body = read(request_path, String)
    merged_headers = Pair{String,String}[
        "Content-Type" => "application/json",
        "Accept" => "application/json",
    ]
    append!(merged_headers, headers)

    response = Downloads.request(
        adapter.url;
        method="POST",
        headers=merged_headers,
        input=IOBuffer(request_body),
        output=response_path,
        timeout=adapter.timeout,
        throw=false,
    )

    return ServiceResult(
        200 <= response.status < 300,
        response.status,
        request_path,
        response_path,
    )
end

end
