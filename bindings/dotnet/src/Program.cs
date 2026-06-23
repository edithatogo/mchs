using System.Text.Json;
using System.ComponentModel;
using Mchs.Bindings.DotNet.Interop;

namespace Mchs.Bindings.DotNet;

public static class Program
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        WriteIndented = true,
    };

    public static async Task<int> Main(string[] args)
    {
        if (args.Length == 0 || HasHelpFlag(args))
        {
            PrintUsage();
            return 0;
        }

        if (!BindingCliOptions.TryParse(args, out var options, out var errorMessage))
        {
            if (!string.IsNullOrWhiteSpace(errorMessage))
            {
                Console.Error.WriteLine(errorMessage);
            }

            PrintUsage();
            return 1;
        }

        if (options is null)
        {
            PrintUsage();
            return 1;
        }

        var adapter = new LocalFileInteropAdapter();
        try
        {
            var response = await adapter.ExecuteAsync(options.RequestPath, options.ResponsePath).ConfigureAwait(false);
            Console.WriteLine(JsonSerializer.Serialize(response, JsonOptions));
            return response.Success ? 0 : 1;
        }
        catch (Exception ex) when (ex is FileNotFoundException or InvalidDataException or JsonException or Win32Exception)
        {
            Console.Error.WriteLine(ex.Message);
            return 1;
        }
    }

    private static bool HasHelpFlag(string[] args)
    {
        foreach (var arg in args)
        {
            if (arg is "--help" or "-h")
            {
                return true;
            }
        }

        return false;
    }

    private static void PrintUsage()
    {
        Console.WriteLine("""
        DotNet binding CLI/file adapter

        Usage:
          dotnet run --project bindings/dotnet -- --request <request.json> --response <response.json>

        The request file must contain a BindingRequest JSON document.
        The CLI delegates calculator work to the shared core funding-calculator command.
        Override the command with MCHS_DOTNET_SHARED_CORE_CLI when needed.
        """);
    }
}
