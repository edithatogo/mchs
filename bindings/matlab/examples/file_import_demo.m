%% File import demo - MATLAB interop adapter
%
% This file demonstrates the file-import pattern for reading shared-core
% calculator outputs into MATLAB. It is a synthetic example and does not
% contain calculation routines.
%
% Prerequisites:
%   - A pre-computed CSV or Parquet file from the shared-core CLI.
%   - MATLAB R2019b or later (R2020b+ for parquetread).
%
% --- CSV import (primary mode) ---
csv_file = 'results.csv';
if exist(csv_file, 'file')
    validation = validateInput(csv_file);
    if ~validation.success
        error('CSV boundary validation failed: %s', validation.errors(1).message);
    end
    results_csv = importResultTable(csv_file);
    fprintf('Loaded %d rows from CSV: %s\n', height(results_csv), csv_file);
    disp(results_csv(1:min(5, height(results_csv)), :));
else
    fprintf('CSV file not found: %s\n', csv_file);
    fprintf('Generate it first with: mchs-calc --output %s\n', csv_file);
end

% --- Parquet import (alternative) ---
parquet_file = 'results.parquet';
if exist(parquet_file, 'file')
    try
        results_pq = parquetread(parquet_file);
        fprintf('Loaded %d rows from Parquet: %s\n', height(results_pq), parquet_file);
    catch ME
        fprintf('Parquet read failed (toolbox may be missing): %s\n', ME.message);
    end
end

%% Notes
% - CSV is the recommended portable format for MATLAB compatibility.
% - Parquet requires MATLAB R2019b+ with the Parquet support files.
% - Use matlab.save() to convert to .mat for downstream MATLAB consumers.
% - This is a transport-only example. No funding formulas or calculation
%   routines are present.
