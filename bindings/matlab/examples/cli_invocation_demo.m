%% CLI invocation demo - MATLAB interop adapter
%
% This file demonstrates the CLI-invocation pattern for calling an external
% shared-core calculator from MATLAB. It is a synthetic example and does not
% contain calculation routines.
%
% Prerequisites:
%   - The shared-core CLI (mchs-calc) must be installed and on PATH.
%   - MATLAB R2019b or later (for readtable on CSV output).
%
% Set calculator parameters
calculator_id = 'nwau';
pricing_year = '2026';
output_file = 'results.csv';

run = invokeCli("mchs-calc", ...
    "CalculatorId", calculator_id, ...
    "PricingYear", pricing_year, ...
    "OutputPath", output_file);

% Load results into MATLAB
results = importResultTable(run.outputPath);

% Display summary
fprintf('Loaded %d rows from %s\n', height(results), output_file);
disp(results(1:min(5, height(results)), :));

%% Notes
% - The CLI does not write .mat files. Use matlab.save() after loading CSV.
% - On Windows, provide the full path to mchs-calc or ensure it is on PATH.
% - This is a transport-only example. No funding formulas or calculation
%   routines are present.
