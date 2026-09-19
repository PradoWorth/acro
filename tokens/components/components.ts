/* Gerado por src/gerar_tokens.py a partir de site.css.
   Não edite à mão: a fonte da verdade é o :root do site. */
export const components = {
  ctaGrad: 'linear-gradient(90deg, #1c585d, #118372)',
  ctaHover: 'linear-gradient(90deg, #408415, #687d16)',
  band: '64px',
  rButton: '40px',
  rCard: '16px',
  rInput: '6px',
  rTag: '100px',
  shadowButton: 'rgba(0, 0, 0, .2) 0 1px 2px 0, rgba(0, 0, 0, .08) 0 6px 16px 0',
} as const;

export type ComponentsToken = keyof typeof components;
