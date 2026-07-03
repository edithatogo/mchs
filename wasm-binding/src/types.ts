export type JsonPrimitive = string | number | boolean | null;

export type JsonValue = JsonPrimitive | JsonObject | JsonValue[];

export interface JsonObject {
  readonly [key: string]: JsonValue;
}

export interface WasmModuleShape {
  readonly default?: unknown;
  readonly [key: string]: unknown;
}

export interface WasmAdapterConfig<TExports extends object> {
  readonly moduleFactory: () => Promise<unknown> | unknown;
  readonly validateExports: (
    candidate: unknown,
  ) => candidate is TExports;
  readonly onReady?: (exports: Readonly<TExports>) => void | Promise<void>;
}

export interface WasmAdapterHandle<TExports extends object> {
  readonly exports: Readonly<TExports>;
  readonly ready: Promise<Readonly<TExports>>;
}

export interface FutureWasmCalculatorExports {
  readonly version?: string;
  readonly init?: () => Promise<void> | void;
  readonly calculate?: (input: JsonValue) => JsonValue | Promise<JsonValue>;
}

export interface WasmCalculatorExports {
  readonly version?: string;
  readonly init?: () => Promise<void> | void;
  readonly calculate: (input: JsonValue) => JsonValue | Promise<JsonValue>;
}

export interface WasmCalculatorAdapter {
  readonly version?: string;
  readonly ready: Promise<Readonly<WasmCalculatorExports>>;
  readonly calculate: (input: JsonValue) => Promise<JsonValue>;
}
