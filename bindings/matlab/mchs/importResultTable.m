function result = importResultTable(outputPath, options)
%IMPORTRESULTTABLE Read a shared-core CSV or Parquet result into MATLAB.
arguments
    outputPath (1,1) string
    options.Format (1,1) string = "auto"
    options.PreviewRows (1,1) double {mustBeNonnegative} = inf
end

format = resolveFormat(outputPath, options.Format);
if ~isfile(outputPath)
    error("mchs:FileImportFailed", "Output file does not exist: %s", outputPath);
end

switch format
    case "csv"
        tableData = readtable(outputPath);
    case "parquet"
        tableData = parquetread(outputPath);
    otherwise
        error("mchs:UnsupportedFormat", "Unsupported output format: %s", format);
end

if isfinite(options.PreviewRows)
    rowLimit = min(height(tableData), options.PreviewRows);
    tableData = tableData(1:rowLimit, :);
end

result = tableData;
end

function format = resolveFormat(outputPath, requestedFormat)
format = lower(string(requestedFormat));
if format ~= "auto"
    return
end

[~, ~, ext] = fileparts(outputPath);
switch lower(string(ext))
    case ".csv"
        format = "csv";
    case ".parquet"
        format = "parquet";
    otherwise
        format = "unknown";
end
end
