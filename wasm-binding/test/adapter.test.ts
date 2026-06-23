import { describe, expect, it } from 'vitest';

import {
  createWasmAdapter,
  createWasmCalculatorAdapter,
  isWasmCalculatorExports,
  WasmAdapterError,
} from '../src/index.js';

describe('createWasmAdapter', () => {
  it('unwraps a wasm-pack-style default initializer and freezes the boundary', async () => {
    const handle = await createWasmAdapter({
      moduleFactory: () => ({
        default: () => ({
          version: '0.0.0',
          calculate: (payload: unknown) => payload,
        }),
      }),
      validateExports: (
        candidate,
      ): candidate is {
        readonly version: string;
        readonly calculate: (payload: unknown) => unknown;
      } => {
        if (typeof candidate !== 'object' || candidate === null) {
          return false;
        }

        const record = candidate as Record<string, unknown>;
        return (
          typeof record.version === 'string' &&
          typeof record.calculate === 'function'
        );
      },
    });

    expect(handle.exports.version).toBe('0.0.0');
    await expect(handle.ready).resolves.toMatchObject({ version: '0.0.0' });
  });

  it('fails closed when the module surface does not match', async () => {
    await expect(
      createWasmAdapter({
        moduleFactory: () => ({ default: () => ({}) }),
        validateExports: (_candidate): _candidate is never => false,
      }),
    ).rejects.toBeInstanceOf(WasmAdapterError);
  });

  it('adapts wasm-pack modules by initializing default glue and using named exports', async () => {
    const calls: string[] = [];
    const adapter = await createWasmCalculatorAdapter(() => ({
      default: () => {
        calls.push('wasm-pack-init');
      },
      init: () => {
        calls.push('core-init');
      },
      version: '0.1.0',
      calculate: (payload: unknown) => ({
        source: 'rust-wasm',
        payload,
      }),
    }));

    await expect(adapter.ready).resolves.toMatchObject({ version: '0.1.0' });
    await expect(adapter.calculate({ case: 'synthetic' })).resolves.toEqual({
      source: 'rust-wasm',
      payload: { case: 'synthetic' },
    });
    expect(calls).toEqual(['wasm-pack-init', 'core-init']);
  });

  it('rejects calculator exports without a callable calculate function', () => {
    expect(isWasmCalculatorExports({ version: '0.1.0' })).toBe(false);
    expect(
      isWasmCalculatorExports({
        version: '0.1.0',
        init: 'not-callable',
        calculate: (payload: unknown) => payload,
      }),
    ).toBe(false);
  });
});
