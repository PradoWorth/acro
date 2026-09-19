/* Gerado por src/gerar_tokens.py a partir de site.css.
   Não edite à mão: a fonte da verdade é o :root do site. */
export const primitive = {
  petrolDeep: '#0b504c',
  iris: '#149d88',
  softIris: '#228cb5',
  cobalt: '#317ae2',
  cobaltLift: '#317ae2',
  irisOnDark: '#8acec4',
  studioSlate: '#262b31',
  obsidian: '#030b12',
  white: '#ffffff',
  cloud: '#f1f5f9',
  mist: '#e0e5e9',
  graphite: '#a0a5a8',
  iron: '#596269',
  noir: '#000000',
  cobaltInk: '#255caa',
  softIrisInk: '#186582',
  sans: '"Inter", ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  display: '"Manrope", ui-sans-serif, "Segoe UI", Roboto, system-ui, sans-serif',
  petrol: 'var(--iris)',
  petrolSoft: 'var(--soft-iris)',
  brass: 'var(--iris)',
  brassInk: 'var(--accent-ink)',
} as const;

export type PrimitiveToken = keyof typeof primitive;
