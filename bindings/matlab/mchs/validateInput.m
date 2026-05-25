function result = validateInput(inputPath, options)
%VALIDATEINPUT Inspect a file-boundary input before calling the external CLI.
arguments
    inputPath (1,1) string
    options.RequiredColumns (1,:) string = string.empty(1, 0)
    options.Format (1,1) string = "auto"
end

startedAt = datetime("now", "TimeZone", "UTC", "Format", "yyyy-MM-dd'T'HH:mm:ss'Z'");
checks = struct("id", {}, "status", {}, "message", {});
errors = struct("code", {}, "message", {});

if strlength(inputPath) == 0
    checks(end + 1) = makeCheck("input_path_declared", "fail", "Input path is empty.");
    errors(end + 1) = makeError("MATLAB_INTEROP_SCHEMA_MISMATCH", "Input path is required.");
    result = makeResult("fail", inputPath, "", checks, errors, startedAt);
    return
end

if ~isfile(inputPath)
    checks(end + 1) = makeCheck("input_file_exists", "fail", "Input file does not exist.");
    errors(end + 1) = makeError("MATLAB_INTEROP_FILE_IMPORT_FAILED", "Input file was not found.");
    result = makeResult("fail", inputPath, "", checks, errors, startedAt);
    return
end

checks(end + 1) = makeCheck("input_file_exists", "pass", "Input file exists.");
format = resolveFormat(inputPath, options.Format);
if ~any(format == ["csv", "parquet"])
    checks(end + 1) = makeCheck("input_format_supported", "fail", "Only CSV and Parquet file boundaries are supported.");
    errors(end + 1) = makeError("MATLAB_INTEROP_FILE_IMPORT_FAILED", "Unsupported input format.");
    result = makeResult("fail", inputPath, format, checks, errors, startedAt);
    return
end

checks(end + 1) = makeCheck("input_format_supported", "pass", "Input format is supported.");

try
    preview = importResultTable(inputPath, "Format", format, "PreviewRows", 0);
    columnNames = string(preview.VariableNames);
    missingColumns = setdiff(options.RequiredColumns, columnNames, "stable");
    if isempty(missingColumns)
        checks(end + 1) = makeCheck("required_columns_present", "pass", "Required columns are present.");
    else
        checks(end + 1) = makeCheck("required_columns_present", "fail", "Required columns are missing.");
        errors(end + 1) = makeError("MATLAB_INTEROP_SCHEMA_MISMATCH", ...
            "Missing required columns: " + strjoin(missingColumns, ", "));
    end
catch ME
    checks(end + 1) = makeCheck("file_boundary_readable", "fail", "File could not be read by MATLAB.");
    errors(end + 1) = makeError("MATLAB_INTEROP_FILE_IMPORT_FAILED", ME.message);
end

if isempty(errors)
    status = "pass";
else
    status = "fail";
end

result = makeResult(status, inputPath, format, checks, errors, startedAt);
end

function format = resolveFormat(inputPath, requestedFormat)
format = lower(string(requestedFormat));
if format ~= "auto"
    return
end

[~, ~, ext] = fileparts(inputPath);
switch lower(string(ext))
    case ".csv"
        format = "csv";
    case ".parquet"
        format = "parquet";
    otherwise
        format = "unknown";
end
end

function result = makeResult(status, inputPath, format, checks, errors, startedAt)
passed = sum(string({checks.status}) == "pass");
failed = sum(string({checks.status}) == "fail");
result = struct( ...
    "schemaVersion", "1.0", ...
    "mode", "file-import", ...
    "status", status, ...
    "success", status == "pass", ...
    "inputPath", inputPath, ...
    "format", format, ...
    "checks", checks, ...
    "summary", struct("passed", passed, "failed", failed, "blocked", 0), ...
    "errors", errors, ...
    "provenance", struct( ...
        "sourcePath", inputPath, ...
        "validatedAt", string(startedAt), ...
        "boundary", "matlab-file-import" ...
    ) ...
);
end

function check = makeCheck(id, status, message)
check = struct("id", id, "status", status, "message", message);
end

function errorRecord = makeError(code, message)
errorRecord = struct("code", code, "message", message);
end
