using System.Diagnostics;
using System.Text;
using System.Text.Json;
using Mchs.Bindings.DotNet.Models;

namespace Mchs.Bindings.DotNet.Interop;

public sealed class LocalFileInteropAdapter : IBindingInteropAdapter
{
    public const string SharedCoreCliEnvironmentVariable = "MCHS_DOTNET_SHARED_CORE_CLI";
    public const string FileRootEnvironmentVariable = "MCHS_DOTNET_FILE_ROOT";

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
    };

    private static readonly HashSet<string> FileBackedOperations = new(StringComparer.Ordinal)
    {
        "acute",
        "ed",
        "non-admitted",
    };

    private readonly string fileRoot;

    public LocalFileInteropAdapter()
        : this(Environment.GetEnvironmentVariable(FileRootEnvironmentVariable))
    {
    }

    public LocalFileInteropAdapter(string? fileRoot)
    {
        this.fileRoot = ResolveRoot(fileRoot);
    }

    public async Task<BindingResponse> ExecuteAsync(
        string requestPath,
        string responsePath,
        CancellationToken cancellationToken = default)
    {
        var resolvedRequestPath = ResolveExistingFilePath(fileRoot, requestPath, "request");
        var resolvedResponsePath = ResolveWritableFilePath(fileRoot, responsePath, "response");
        var request = await ReadRequestAsync(resolvedRequestPath, cancellationToken).ConfigureAwait(false);
        request = ResolveRequestPaths(request);
        var command = SharedCoreCommand.FromEnvironment();

        var response = await ExecuteSharedCoreCliAsync(
            request,
            command,
            cancellationToken).ConfigureAwait(false);

        await WriteResponseAsync(resolvedResponsePath, response, cancellationToken).ConfigureAwait(false);
        return response;
    }

    private static async Task<BindingRequest> ReadRequestAsync(
        string requestPath,
        CancellationToken cancellationToken)
    {
        if (!File.Exists(requestPath))
        {
            throw new FileNotFoundException("Request file not found.", requestPath);
        }

        await using var stream = File.OpenRead(requestPath);
        var request = await JsonSerializer.DeserializeAsync<BindingRequest>(
            stream,
            JsonOptions,
            cancellationToken).ConfigureAwait(false);

        if (request is null)
        {
            throw new InvalidDataException("Request file did not contain a valid BindingRequest document.");
        }

        ValidateRequestShape(request);
        return request;
    }

    private BindingRequest ResolveRequestPaths(BindingRequest request)
    {
        var outputPath = ResolveWritableFilePath(fileRoot, request.OutputPath, "request outputPath");
        var inputPath = request.InputPath;
        var paramsDirectory = request.ParamsDirectory;

        if (FileBackedOperations.Contains(request.Operation))
        {
            inputPath = ResolveExistingFilePath(fileRoot, request.InputPath, "request inputPath");
        }

        if (!string.IsNullOrWhiteSpace(request.ParamsDirectory))
        {
            paramsDirectory = ResolveExistingDirectoryPath(fileRoot, request.ParamsDirectory, "request paramsDirectory");
        }

        return request with
        {
            InputPath = inputPath,
            OutputPath = outputPath,
            ParamsDirectory = paramsDirectory,
        };
    }

    private static void ValidateRequestShape(BindingRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Operation))
        {
            throw new InvalidDataException("Request operation is required.");
        }

        if (string.IsNullOrWhiteSpace(request.OutputPath))
        {
            throw new InvalidDataException("Request outputPath is required.");
        }

        if (FileBackedOperations.Contains(request.Operation))
        {
            if (string.IsNullOrWhiteSpace(request.InputPath))
            {
                throw new InvalidDataException("Request inputPath is required for calculator operations.");
            }

            return;
        }

        if (request.Operation != "interop contract")
        {
            throw new InvalidDataException(
                "Unsupported operation. Expected acute, ed, non-admitted, or interop contract.");
        }
    }

    private static string ResolveRoot(string? configuredRoot)
    {
        var root = string.IsNullOrWhiteSpace(configuredRoot)
            ? Directory.GetCurrentDirectory()
            : configuredRoot;
        var fullRoot = Path.GetFullPath(root);
        if (!Directory.Exists(fullRoot))
        {
            throw new DirectoryNotFoundException($"Configured .NET binding file root not found: {fullRoot}");
        }

        return new DirectoryInfo(fullRoot).ResolveLinkTarget(returnFinalTarget: true)?.FullName
            ?? fullRoot;
    }

    private static string ResolveExistingFilePath(string root, string path, string label)
    {
        var resolved = ResolvePathWithinRoot(root, path, label);
        if (!File.Exists(resolved))
        {
            throw new FileNotFoundException($"{label} file not found.", resolved);
        }

        var target = new FileInfo(resolved).ResolveLinkTarget(returnFinalTarget: true)?.FullName;
        return target is null ? resolved : EnsurePathWithinRoot(root, target, label);
    }

    private static string ResolveExistingDirectoryPath(string root, string path, string label)
    {
        var resolved = ResolvePathWithinRoot(root, path, label);
        if (!Directory.Exists(resolved))
        {
            throw new DirectoryNotFoundException($"{label} directory not found: {resolved}");
        }

        var target = new DirectoryInfo(resolved).ResolveLinkTarget(returnFinalTarget: true)?.FullName;
        return target is null ? resolved : EnsurePathWithinRoot(root, target, label);
    }

    private static string ResolveWritableFilePath(string root, string path, string label)
    {
        var resolved = ResolvePathWithinRoot(root, path, label);
        if (File.Exists(resolved))
        {
            var target = new FileInfo(resolved).ResolveLinkTarget(returnFinalTarget: true)?.FullName;
            return target is null ? resolved : EnsurePathWithinRoot(root, target, label);
        }

        var parent = Path.GetDirectoryName(resolved);
        if (string.IsNullOrWhiteSpace(parent))
        {
            throw new InvalidDataException($"{label} must include a parent directory.");
        }

        var existingParent = Directory.Exists(parent)
            ? parent
            : Path.GetDirectoryName(parent);
        if (string.IsNullOrWhiteSpace(existingParent) || !Directory.Exists(existingParent))
        {
            throw new DirectoryNotFoundException($"{label} parent directory not found: {parent}");
        }

        var realParent = new DirectoryInfo(existingParent).ResolveLinkTarget(returnFinalTarget: true)?.FullName
            ?? existingParent;
        EnsurePathWithinRoot(root, realParent, label);
        return resolved;
    }

    private static string ResolvePathWithinRoot(string root, string path, string label)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            throw new InvalidDataException($"{label} path is required.");
        }

        var candidate = Path.IsPathRooted(path)
            ? Path.GetFullPath(path)
            : Path.GetFullPath(Path.Combine(root, path));
        return EnsurePathWithinRoot(root, candidate, label);
    }

    private static string EnsurePathWithinRoot(string root, string path, string label)
    {
        var relative = Path.GetRelativePath(root, path);
        if (relative == "."
            || (!relative.StartsWith("..", StringComparison.Ordinal)
                && !Path.IsPathRooted(relative)))
        {
            return path;
        }

        throw new InvalidDataException($"{label} path escapes configured .NET binding file root.");
    }

    private static async Task<BindingResponse> ExecuteSharedCoreCliAsync(
        BindingRequest request,
        SharedCoreCommand command,
        CancellationToken cancellationToken)
    {
        var outputDirectory = Path.GetDirectoryName(request.OutputPath);
        if (!string.IsNullOrWhiteSpace(outputDirectory))
        {
            Directory.CreateDirectory(outputDirectory);
        }

        var processStartInfo = new ProcessStartInfo
        {
            FileName = command.Executable,
            UseShellExecute = false,
            RedirectStandardError = true,
            RedirectStandardOutput = true,
        };

        foreach (var argument in command.BaseArguments)
        {
            processStartInfo.ArgumentList.Add(argument);
        }

        foreach (var argument in BuildCliArguments(request))
        {
            processStartInfo.ArgumentList.Add(argument);
        }

        using var process = Process.Start(processStartInfo)
            ?? throw new InvalidOperationException("Could not start the shared core CLI process.");

        var stdoutTask = process.StandardOutput.ReadToEndAsync(cancellationToken);
        var stderrTask = process.StandardError.ReadToEndAsync(cancellationToken);

        await process.WaitForExitAsync(cancellationToken).ConfigureAwait(false);

        var stdout = await stdoutTask.ConfigureAwait(false);
        var stderr = await stderrTask.ConfigureAwait(false);

        if (request.Operation == "interop contract" && process.ExitCode == 0)
        {
            await File.WriteAllTextAsync(request.OutputPath, stdout, cancellationToken)
                .ConfigureAwait(false);
        }

        var diagnostics = SplitDiagnostics(stderr);
        var warnings = BuildWarnings(request, process.ExitCode, stdout);
        var success = process.ExitCode == 0;

        return new BindingResponse(
            Success: success,
            Status: success ? "delegated-to-shared-core" : "shared-core-cli-failed",
            Operation: request.Operation,
            InputPath: request.InputPath,
            OutputPath: request.OutputPath,
            Message: success
                ? "DotNet binding delegated execution to the shared core CLI."
                : "Shared core CLI returned a non-zero exit code.",
            ExitCode: process.ExitCode,
            CliCommand: command.Describe(BuildCliArguments(request)),
            CorrelationId: request.CorrelationId,
            Diagnostics: diagnostics,
            Warnings: warnings);
    }

    private static IEnumerable<string> BuildCliArguments(BindingRequest request)
    {
        if (request.Operation == "interop contract")
        {
            yield return "interop";
            yield return "contract";
            yield break;
        }

        yield return request.Operation;
        yield return request.InputPath;
        yield return "--output";
        yield return request.OutputPath;

        if (!string.IsNullOrWhiteSpace(request.PricingYear))
        {
            yield return "--year";
            yield return request.PricingYear;
        }

        if (!string.IsNullOrWhiteSpace(request.ParamsDirectory))
        {
            yield return "--params";
            yield return request.ParamsDirectory;
        }
    }

    private static async Task WriteResponseAsync(
        string responsePath,
        BindingResponse response,
        CancellationToken cancellationToken)
    {
        var directory = Path.GetDirectoryName(responsePath);
        if (!string.IsNullOrWhiteSpace(directory))
        {
            Directory.CreateDirectory(directory);
        }

        await using var stream = File.Create(responsePath);
        await JsonSerializer.SerializeAsync(stream, response, JsonOptions, cancellationToken)
            .ConfigureAwait(false);
    }

    private static IReadOnlyList<string> SplitDiagnostics(string stderr)
    {
        return stderr
            .Split(Environment.NewLine, StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
    }

    private static IReadOnlyList<string> BuildWarnings(
        BindingRequest request,
        int exitCode,
        string stdout)
    {
        var warnings = new List<string>
        {
            "Formula logic is delegated to the shared core CLI; the .NET binding only validates and transports files.",
        };

        if (request.Metadata is null || request.Metadata.Count == 0)
        {
            warnings.Add("Request metadata was empty.");
        }

        if (exitCode != 0 && !string.IsNullOrWhiteSpace(stdout))
        {
            warnings.Add("Shared core CLI emitted stdout despite failing; inspect diagnostics and output artifacts.");
        }

        return warnings;
    }

    private sealed record SharedCoreCommand(string Executable, IReadOnlyList<string> BaseArguments)
    {
        public static SharedCoreCommand FromEnvironment()
        {
            var configured = Environment.GetEnvironmentVariable(SharedCoreCliEnvironmentVariable);
            if (string.IsNullOrWhiteSpace(configured))
            {
                return new SharedCoreCommand("funding-calculator", Array.Empty<string>());
            }

            var tokens = SplitCommand(configured);
            if (tokens.Count == 0)
            {
                return new SharedCoreCommand("funding-calculator", Array.Empty<string>());
            }

            return new SharedCoreCommand(tokens[0], tokens.Skip(1).ToArray());
        }

        public string Describe(IEnumerable<string> operationArguments)
        {
            return string.Join(
                " ",
                new[] { Executable }
                    .Concat(BaseArguments)
                    .Concat(operationArguments)
                    .Select(QuoteForDisplay));
        }

        private static IReadOnlyList<string> SplitCommand(string command)
        {
            var tokens = new List<string>();
            var current = new StringBuilder();
            var quote = '\0';

            foreach (var character in command)
            {
                if (quote == '\0' && char.IsWhiteSpace(character))
                {
                    if (current.Length > 0)
                    {
                        tokens.Add(current.ToString());
                        current.Clear();
                    }

                    continue;
                }

                if ((character == '"' || character == '\'') && (quote == '\0' || quote == character))
                {
                    quote = quote == '\0' ? character : '\0';
                    continue;
                }

                current.Append(character);
            }

            if (quote != '\0')
            {
                throw new InvalidDataException(
                    $"{SharedCoreCliEnvironmentVariable} contains an unterminated quoted argument.");
            }

            if (current.Length > 0)
            {
                tokens.Add(current.ToString());
            }

            return tokens;
        }

        private static string QuoteForDisplay(string argument)
        {
            if (argument.Length == 0 || argument.Any(char.IsWhiteSpace))
            {
                return $"\"{argument.Replace("\"", "\\\"", StringComparison.Ordinal)}\"";
            }

            return argument;
        }
    }
}
