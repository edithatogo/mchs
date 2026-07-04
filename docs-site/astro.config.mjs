import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightLinksValidator from 'starlight-links-validator';
import starlightVersions from 'starlight-versions';

const repository = process.env.GITHUB_REPOSITORY ?? 'edithatogo/microcosting_healthservices';
const [owner, repo] = repository.split('/');
const siteUrl =
  process.env.SITE_URL ?? `https://${owner}.github.io/${repo}/`;
const siteBase = process.env.SITE_BASE ?? `/${repo}/`;

export default defineConfig({
  site: siteUrl,
  base: siteBase,
  integrations: [
    starlightLinksValidator(),
    starlight({
      title: 'Microcosting Health Services',
      description:
        'Versioned IHACPA calculator docs, archive coverage, and delivery guidance.',
      logo: {
        src: './src/assets/logo.svg',
      },
      customCss: ['./src/styles/custom.css'],
      social: [
        {
          icon: 'github',
          label: 'GitHub',
          href: 'https://github.com/edithatogo/microcosting_healthservices',
        },
      ],
      editLink: {
        baseUrl:
          'https://github.com/edithatogo/microcosting_healthservices/edit/master/docs-site/',
      },
      sidebar: [
        {
          label: 'Overview',
          items: ['index', 'versions', 'versions/2025', 'migration/legacy-docs'],
        },
        {
          label: 'Tutorials',
          items: [
            {
              label: 'Costing Studies',
              items: [
                'tutorials/costing-study-nwau-nep',
                'tutorials/costing-study-cost-vs-price',
                'tutorials/costing-study-stream-benchmarking',
                'tutorials/mimic-iv-demo-worked-example',
              ],
            },
            {
              label: 'Integration Guides',
              items: [
                'tutorials/cli-file-interop',
                'tutorials/c-abi-consumers',
                'tutorials/typescript-wasm-browser-demo',
                'tutorials/julia-dataframes-arrow-costing-study',
                'tutorials/r-markdown-quarto-costing-study',
              ],
            },
          ],
        },
        {
          label: 'Reference',
          items: [
            'reference/calculators',
            'reference/glossary',
          ],
        },
        {
          label: 'Governance',
          items: [
            {
              label: 'Project',
              items: [
                'governance/product',
                'governance/tech-stack',
                'governance/workflow',
                'governance/validation-vocabulary',
                'governance/data-governance',
              ],
            },
            {
              label: 'Pipelines & Data',
              items: [
                'governance/formula-parameter-bundle-pipeline',
                'governance/ihacpa-source-scanner',
                'governance/reference-data-manifests',
                'governance/pricing-year-validation-gates',
                'governance/pricing-year-diff-tooling',
                'governance/coding-set-version-registry',
                'governance/ar-drg-icd-achi-acs-mapping-registry',
              ],
            },
            {
              label: 'Coverage & Contracts',
              items: [
                'governance/calculator-coverage',
                'governance/public-calculator-contract',
                'governance/source-archive',
                'governance/reference-generation',
                'governance/public-readiness',
              ],
            },
            {
              label: 'Bindings',
              items: [
                'governance/rust-core-architecture',
                'governance/polyglot-rust-core-roadmap',
                'governance/go-binding',
                'governance/kotlin-native-binding',
                'governance/csharp-dotnet-binding',
                'governance/web-and-power-platform-delivery',
                'governance/streamlit-delivery',
                'governance/downstream-packaging-plans',
              ],
            },
            {
              label: 'Operations',
              items: [
                'governance/release-policy',
                'governance/supply-chain-controls',
                'governance/starlight-extensions',
              ],
            },
          ],
        },
      ],
      plugins: [
        starlightVersions({
          versions: [
            {
              slug: '2025',
              label: '2025',
            },
            {
              slug: '2026',
              label: '2026',
            },
          ],
        }),
      ],
    }),
  ],
});
