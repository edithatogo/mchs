function result = invokeCli(cliPath, options)
%INVOKECLI Call an external MCHS CLI and return boundary diagnostics.
arguments
    cliPath (1,1) string
    options.CalculatorId (1,1) string
    options.PricingYear (1,1) string
    options.InputPath (1,1) string = ""
    options.OutputPath (1,1) string = ""
    options.ExtraArgs (1,:) string = string.empty(1, 0)
end

startedAt = datetime("now", "TimeZone", "UTC", "Format", "yyyy-MM-dd'T'HH:mm:ss'Z'");
command = buildCommand(cliPath, options);
[exitCode, stdoutText] = system(command);

checks = struct("id", {}, "status", {}, "message", {});
checks(end + 1) = makeCheck("cli_command_built", "pass", "CLI command was built.");

errors = struct("code", {}, "message", {});
if exitCode == 0
    checks(end + 1) = makeCheck("cli_invocation_completed", "pass", "CLI invocation completed.");
    status = "pass";
else
    checks(end + 1) = makeCheck("cli_invocation_completed", "fail", "CLI invocation failed.");
    errors(end + 1) = makeError("MATLAB_INTEROP_CLI_UNAVAILABLE", stdoutText);
    status = "fail";
end

if strlength(options.OutputPath) > 0
    if isfile(options.OutputPath)
        checks(end + 1) = makeCheck("output_file_created", "pass", "Output file exists.");
    else
        checks(end + 1) = makeCheck("output_file_created", "fail", "Output file was not created.");
        errors(end + 1) = makeError("MATLAB_INTEROP_FILE_IMPORT_FAILED", "Expected output file was not found.");
        status = "fail";
    end
end

passed = sum(string({checks.status}) == "pass");
failed = sum(string({checks.status}) == "fail");
result = struct( ...
    "schemaVersion", "1.0", ...
    "mode", "cli-invocation", ...
    "status", status, ...
    "success", status == "pass", ...
    "command", command, ...
    "exitCode", exitCode, ...
    "stdout", stdoutText, ...
    "outputPath", options.OutputPath, ...
    "checks", checks, ...
    "summary", struct("passed", passed, "failed", failed, "blocked", 0), ...
    "errors", errors, ...
    "provenance", struct( ...
        "calculatorId", options.CalculatorId, ...
        "pricingYear", options.PricingYear, ...
        "invokedAt", string(startedAt), ...
        "boundary", "matlab-cli-invocation" ...
    ) ...
);
end

function command = buildCommand(cliPath, options)
parts = [
    shellQuote(cliPath), ...
    "--calculator", shellQuote(options.CalculatorId), ...
    "--pricing-year", shellQuote(options.PricingYear)
];

if strlength(options.InputPath) > 0
    parts = [parts, "--input", shellQuote(options.InputPath)];
end

if strlength(options.OutputPath) > 0
    parts = [parts, "--output", shellQuote(options.OutputPath)];
end

for idx = 1:numel(options.ExtraArgs)
    parts = [parts, shellQuote(options.ExtraArgs(idx))]; %#ok<AGROW>
end

command = strjoin(parts, " ");
end

function quoted = shellQuote(value)
value = string(value);
if ispc
    quoted = """" + replace(value, """", "\""") + """";
else
    quoted = "'" + replace(value, "'", "'\''") + "'";
end
end

function check = makeCheck(id, status, message)
check = struct("id", id, "status", status, "message", message);
end

function errorRecord = makeError(code, message)
errorRecord = struct("code", code, "message", message);
end
