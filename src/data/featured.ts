export type Frame = { base: string; href: string; label: string; frame: string };

// Photos shown on the home page gallery.
// To swap in new picks: drop `name.avif` + `name.webp` in public/images/ and point `base` at it (without extension).
export const featured: Frame[] = [
  { base: '/images/works/street/main', href: '/street/', label: 'Street', frame: '01' },
  { base: '/images/works/rave/main', href: '/rave/', label: 'Rave', frame: '02' },
  { base: '/images/works/nature/main', href: '/nature/', label: 'Nature', frame: '03' },
  { base: '/images/works/architecture/main', href: '/architecture/', label: 'Architecture', frame: '04' },
  { base: '/images/works/fin_de_soiree/main', href: '/fin_de_soiree/', label: 'Fin de soirée', frame: '05' },
  { base: '/images/works/almost_there/main', href: '/almost_there/', label: 'Almost there', frame: '06' },
];

export const instagram = { handle: '@fixie_des_alpes', href: 'https://www.instagram.com/fixie_des_alpes/' };
