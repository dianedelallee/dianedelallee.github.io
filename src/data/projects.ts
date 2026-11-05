export type Project = {
  name: string;
  description: string;
  language: string;
  color: string;
  repo: string;
  link?: { label: string; href: string };
};

// Mirrors the repositories pinned on https://github.com/dianedelallee
export const projects: Project[] = [
  {
    name: 'poste-restante',
    description:
      'How to address a letter to poste restante, country by country: wording, holding period, fees. An interactive map.',
    language: 'HTML',
    color: '#e34c26',
    repo: 'https://github.com/dianedelallee/poste-restante',
    link: { label: 'poste-restante.club', href: 'https://www.poste-restante.club' },
  },
  {
    name: 'RomandieWidget',
    description: 'iOS widget (WidgetKit) showing the next concerts at Le Romandie, Lausanne.',
    language: 'Swift',
    color: '#f05138',
    repo: 'https://github.com/dianedelallee/RomandieWidget',
  },
  {
    name: 'learn_vocab_tab',
    description:
      'Chromium extension: an illustrated vocabulary word every time you open a new tab. Designed for Arc.',
    language: 'JavaScript',
    color: '#f1e05a',
    repo: 'https://github.com/dianedelallee/learn_vocab_tab',
  },
  {
    name: 'artemis',
    description: 'A nice CSS library providing pastel elements to include in your website.',
    language: 'SCSS',
    color: '#c6538c',
    repo: 'https://github.com/dianedelallee/artemis',
    link: { label: 'npm: artemis-css', href: 'https://www.npmjs.com/package/artemis-css' },
  },
];
