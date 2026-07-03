namespace Mchs.Bindings.DotNet.Models;

public sealed record BindingRequest(
    string InputPath,
    string OutputPath,
    string Operation,
    string? CorrelationId,
    string? PricingYear,
    string? ParamsDirectory,
    IReadOnlyDictionary<string, string>? Metadata);
