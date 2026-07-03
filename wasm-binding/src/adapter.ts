import type {
  JsonValue,
  WasmAdapterConfig,
  WasmAdapterHandle,
  WasmCalculatorAdapter,
  WasmCalculatorExports,
  WasmModuleShape,
} from './types.js';

export class WasmAdapterError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = 'WasmAdapterError';
  }
}

export async function createWasmAdapter<TExports extends object>(
  config: WasmAdapterConfig<TExports>,
): Promise<WasmAdapterHandle<TExports>> {
  const module = await config.moduleFactory();
  const resolvedModule = await unwrapDefaultExport(module);

  if (!config.validateExports(resolvedModule)) {
    throw new WasmAdapterError('WASM module exports do not match the adapter contract.');
  }

  const frozenExports = Object.freeze({ ...resolvedModule }) as Readonly<TExports>;
  const ready = (async () => {
    if (config.onReady) {
      await config.onReady(frozenExports);
    }

    return frozenExports;
  })();

  return {
    exports: frozenExports,
    ready,
  };
}

export async function createWasmCalculatorAdapter(
  moduleFactory: WasmAdapterConfig<WasmCalculatorExports>['moduleFactory'],
): Promise<WasmCalculatorAdapter> {
  const handle = await createWasmAdapter<WasmCalculatorExports>({
    moduleFactory,
    validateExports: isWasmCalculatorExports,
    onReady: async (exports) => {
      if (exports.init) {
        await exports.init();
      }
    },
  });

  const adapter: WasmCalculatorAdapter = {
    ready: handle.ready,
    calculate: async (input: JsonValue) => {
      const exports = await handle.ready;
      return await exports.calculate(input);
    },
  };

  if (handle.exports.version !== undefined) {
    return {
      ...adapter,
      version: handle.exports.version,
    };
  }

  return adapter;
}

export function isWasmCalculatorExports(
  candidate: unknown,
): candidate is WasmCalculatorExports {
  if (!isRecord(candidate)) {
    return false;
  }

  const { calculate, init, version } = candidate;
  return (
    typeof calculate === 'function' &&
    (init === undefined || typeof init === 'function') &&
    (version === undefined || typeof version === 'string')
  );
}

async function unwrapDefaultExport(module: unknown): Promise<unknown> {
  if (!isWasmModuleShape(module)) {
    return module;
  }

  const defaultExport = module.default;
  if (typeof defaultExport === 'function') {
    const initialized = await defaultExport();
    if (isRecord(initialized) && Object.keys(initialized).length > 0) {
      return initialized;
    }

    return withoutDefaultExport(module);
  }

  if (defaultExport && typeof defaultExport === 'object') {
    return defaultExport;
  }

  return module;
}

function isWasmModuleShape(candidate: unknown): candidate is WasmModuleShape {
  return isRecord(candidate);
}

function withoutDefaultExport(
  module: WasmModuleShape,
): Record<string, unknown> {
  const { default: _default, ...exports } = module;
  return exports;
}

function isRecord(candidate: unknown): candidate is Record<string, unknown> {
  return typeof candidate === 'object' && candidate !== null;
}
